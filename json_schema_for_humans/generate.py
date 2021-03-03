import copy
import json
import logging
import os
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, TextIO, Tuple, Type, Union, cast, Iterator

import click
import htmlmin
import jinja2
from jinja2.ext import loopcontrols
from urllib.parse import quote_plus
import markdown2
import requests
import yaml
from dataclasses_json import dataclass_json
from jinja2 import FileSystemLoader
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.javascript import JavascriptLexer
from pytz import reference

TEMPLATE_FILE_NAME = "base.html"
CSS_FILE_NAME = "schema_doc.css"
JS_FILE_NAME = "schema_doc.min.js"

DEFAULT_PATTERN = r"(\[Default - `([^`]+)`\])"
DEPRECATED_PATTERN = r"\[Deprecated"

TYPE_ARRAY = "array"
TYPE_BOOLEAN = "boolean"
TYPE_CONST = "const"
TYPE_ENUM = "enum"
TYPE_INTEGER = "integer"
TYPE_NUMBER = "number"
TYPE_OBJECT = "object"
TYPE_STRING = "string"

KW_REQUIRED = "required"
KW_TITLE = "title"
KW_CONTAINS = "contains"
KW_ITEMS = "items"
KW_UNIQUE_ITEMS = "uniqueItems"
KW_ADDITIONAL_ITEMS = "additionalItems"
KW_MAX_ITEMS = "maxItems"
KW_MIN_ITEMS = "minItems"
KW_MAX_LENGTH = "maxLength"
KW_MIN_LENGTH = "minLength"
KW_PATTERN = "pattern"
KW_CONST = "const"
KW_ENUM = "enum"
KW_ELSE = "else"
KW_THEN = "then"
KW_IF = "if"
KW_NOT = "not"
KW_ONE_OF = "oneOf"
KW_ANY_OF = "anyOf"
KW_ALL_OF = "allOf"
KW_PROPERTIES = "properties"
KW_PATTERN_PROPERTIES = "patternProperties"
KW_ADDITIONAL_PROPERTIES = "additionalProperties"

DESCRIPTION = "description"
DEFAULT = "default"
EXAMPLES = "examples"
ITEMS = "items"
TYPE = "type"
REF = "$ref"

MULTIPLE_OF = "multipleOf"
MAXIMUM = "maximum"
EXCLUSIVE_MAXIMUM = "exclusiveMaximum"
MINIMUM = "minimum"
EXCLUSIVE_MINIMUM = "exclusiveMinimum"

SHORT_DESCRIPTION_NUMBER_OF_LINES = 8

CONFIG_DEPRECATION_MESSAGE = (
    "JSON Schema for humans: Please supply a GenerationConfiguration object instead of individual options"
)

circular_references: Dict["SchemaNode", bool] = {}


@dataclass_json
@dataclass
class GenerationConfiguration:
    """Configuration for generating documentation for a schema"""

    minify: bool = True
    description_is_markdown: bool = True
    deprecated_from_description: bool = False
    show_breadcrumbs: bool = True
    collapse_long_descriptions: bool = True
    default_from_description: bool = False
    expand_buttons: bool = False
    copy_css: bool = True
    copy_js: bool = True
    link_to_reused_ref: bool = True
    recursive_detection_depth: int = 25
    templates_directory: str = os.path.join(os.path.dirname(__file__), "templates")
    template_name: str = "js"
    # markdown2 extra parameters can be added here: https://github.com/trentm/python-markdown2/wiki/Extras
    markdown_options: Any = field(
        default_factory=lambda: {
            "break-on-newline": True,
            "fenced-code-blocks": {"cssclass": "highlight jumbotron"},
            "tables": None,
        }
    )
    template_md_options: Dict[str, Any] = field(default_factory=lambda: {"badge_as_image": False})


class SchemaNode:
    """
    Represents a part of a JSON schema with additional metadata to help with documentation
    """

    def __init__(
        self,
        depth: int,
        file: str,
        path_to_element: List[Union[str, int]],
        html_id: str,
        breadcrumb_name: str = "",
        ref_path="",
        parent: "SchemaNode" = None,
        parent_key: str = None,
        literal: Union[str, int, bool] = None,
        keywords: Dict[str, Union["SchemaNode", str, List[str]]] = None,
        array_items: List["SchemaNode"] = None,
        links_to: "SchemaNode" = None,
        refers_to: "SchemaNode" = None,
        is_displayed: bool = True,
    ):
        """

        :param depth: Number of levels from the root of the schema to this node.
        :param file: Real path to the schema file
        :param path_to_element: Path from the root of the schema to the current element
        :param html_id: HTML ID for the current element. Used for anchor links.
        :param parent: The parent node of which the current node is an array item or keyword
        :param parent_key: If the node is under a keyword of the parent node, that keyword
            Example:
            In the following context
            {
                "patternProperties": {
                    ".*": {
                        "type": string
                    }
                }
            }

            For the node
            {
                "type": string
            }
            The parent_key is ".*"

            For the node
            {
                ".*": {
                    "type": string
                }
            }
            The parent key is "patternProperties"

        :param ref_path: Path of a reference to this element, if any (usually "#/definitions/A name")
        :param literal: If the schema is neither a dict nor an array, it will be kept here
                        Useful for things like description, types, const, enum, etc.
        :param keywords: If the schema is a dict, this will be filled. Otherwise, this stays empty
        :param array_items: If the schema is an array, this will be filled. Otherwise, this stays empty
        :param links_to: If the same node is documented elsewhere, the other SchemaNode that documents it
        :param refers_to: If there is a $ref, this should contain the SchemaNode object for it
        :param is_displayed: Instructs the templates if this part should be fully documented.
                             If false, the description and a link to the referenced element will be generated instead.
                             If false, refers_to needs to be set
        """
        self.depth = depth
        self.file = file
        self.path_to_element = path_to_element
        self.html_id = html_id or "_".join(path_to_element) or "root"
        self.breadcrumb_name = breadcrumb_name
        self.parent = parent
        self.parent_key = parent_key
        self.ref_path = ref_path
        self.literal = literal
        self.keywords = keywords or {}
        self.array_items = array_items or []
        self.links_to = links_to
        self.refers_to = refers_to
        self.is_displayed = is_displayed
        self._refers_to_merged = None
        self.properties: Dict[str, "SchemaNode"] = {}
        self.additional_properties: Optional["SchemaNode"] = None
        # If True, it means additionalProperties is there and false. If False, additionalProperties is either not set
        # or is set but is not false (depends on self.additional_properties)
        self.no_additional_properties: bool = False
        self.pattern_properties: Dict[str, "SchemaNode"] = {}

    @property
    def explicit_no_additional_properties(self) -> bool:
        """Return True if additionalProperties is set and false (to differentiate from not set)"""
        return bool(
            (self.properties or self.pattern_properties)
            and self.no_additional_properties
            and not self.additional_properties
        )

    @property
    def definition_name(self) -> str:
        """The text to display when this node is the title of a section or tab"""
        if self.is_property and self.property_name:
            return self.property_name
        if self.title:
            return self.title
        if self.ref_path:
            return self.ref_path.split("/")[-1]
        return ""

    @property
    def link_name(self) -> str:
        """The text to display when linking to this node from somewhere else in the schema"""
        return self.definition_name or self.html_id

    @property
    def name_for_breadcrumbs(self) -> str:
        return self.definition_name or self.breadcrumb_name

    @property
    def is_property(self) -> bool:
        return bool(self.parent and self.property_name in self.parent.properties.keys())

    @property
    def is_pattern_property(self) -> bool:
        return bool(self.parent and self.property_name in self.parent.pattern_properties.keys())

    @property
    def is_additional_properties(self) -> bool:
        return self.parent_key == KW_ADDITIONAL_PROPERTIES

    @property
    def is_a_property_node(self) -> bool:
        return self.is_property or self.is_pattern_property or self.is_additional_properties

    @property
    def is_additional_properties_schema(self) -> bool:
        return self.is_additional_properties and self.literal is not True

    @property
    def iterate_properties(self) -> Iterable["SchemaNode"]:
        if self.properties:
            yield from self.properties.values()

        if self.pattern_properties:
            yield from self.pattern_properties.values()

        if self.additional_properties:
            yield self.additional_properties

    @property
    def required_properties(self) -> List[str]:
        """The required properties for this node"""
        required_properties = self.kw_required
        if not required_properties:
            return []

        return [r.literal for r in required_properties.array_items]

    @property
    def is_required_property(self) -> bool:
        """Check if the current node represents a property and that this property is required by its parent"""
        return self.parent and self.property_name in self.parent.required_properties

    @property
    def nodes_from_root(self) -> Iterator["SchemaNode"]:
        """The list of nodes to reach this node"""
        nodes: List["SchemaNode"] = [self]
        current_node = self
        while current_node.parent:
            nodes.append(current_node.parent)
            current_node = current_node.parent

        if len(nodes) == 1:
            # Don't want to display "root" alone at the root
            return []

        return reversed(nodes)

    @property
    def path_to_property(self) -> str:
        """Human-readable representation of the path from the root of the schema to this node"""
        path_without_properties = [p for p in self.path_to_element if p not in [KW_PROPERTIES, KW_PATTERN_PROPERTIES]]
        return " -> ".join([p if isinstance(p, str) else f"Item {p}" for p in path_without_properties])

    @property
    def flat_path(self) -> str:
        """String representation of the path to this node from the root of the current schema"""
        return "/".join(str(part) for part in self.path_to_element)

    @property
    def default_value(self) -> Optional[Any]:
        def _default_value(node: SchemaNode) -> Optional[Any]:
            default = node.keywords.get(DEFAULT)
            if isinstance(default, SchemaNode) and default.is_a_property_node:
                return None
            return default

        seen = set()
        current_node = self
        possible_default = _default_value(current_node)
        while not possible_default and current_node.refers_to:
            if current_node in seen:
                break
            seen.add(current_node)
            current_node = current_node.refers_to
            possible_default = _default_value(current_node)

        return possible_default

    @property
    def examples(self) -> List[str]:
        possible_examples = self.keywords.get(EXAMPLES)
        if not possible_examples:
            return []

        if isinstance(possible_examples, SchemaNode) and possible_examples.is_a_property_node:
            return []

        return possible_examples

    @property
    def refers_to_merged(self) -> Optional["SchemaNode"]:
        """The referenced node, with values from the current node merged in"""
        if self._refers_to_merged:
            return self._refers_to_merged

        if not self.refers_to:
            return None

        merged_node = copy.copy(self.refers_to)
        merged_node.keywords = {k: copy.copy(v) for k, v in self.refers_to.keywords.items()}
        merged_node.array_items = [copy.copy(i) for i in self.refers_to.array_items]

        merged_node.keywords.update({k: copy.copy(v) for k, v in self.keywords.items()})
        merged_node.array_items += [copy.copy(i) for i in self.array_items]

        return merged_node

        # self._refers_to_merged = merged_node

        # return self._refers_to_merged

    def get_keyword(self, keyword: str) -> Optional["SchemaNode"]:
        """Get the value of a keyword if present and it is not a property (to avoid conflicts with properties being
        named like a keyword, e.g. a property named "if")
        """
        possible_keyword = self.keywords.get(keyword)
        if possible_keyword and isinstance(possible_keyword, SchemaNode) and not possible_keyword.is_property:
            return possible_keyword

        return None

    @property
    def kw_all_of(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_ALL_OF)

    @property
    def kw_any_of(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_ANY_OF)

    @property
    def kw_one_of(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_ONE_OF)

    @property
    def kw_not(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_NOT)

    @property
    def has_conditional(self) -> bool:
        return self.kw_if is not None and (self.kw_then is not None or self.kw_else is not None)

    @property
    def kw_if(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_IF)

    @property
    def kw_then(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_THEN)

    @property
    def kw_else(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_ELSE)

    @property
    def kw_enum(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_ENUM)

    @property
    def kw_const(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_CONST)

    @property
    def kw_pattern(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_PATTERN)

    @property
    def kw_properties(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_PROPERTIES)

    @property
    def kw_pattern_properties(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_PATTERN_PROPERTIES)

    @property
    def kw_additional_properties(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_ADDITIONAL_PROPERTIES)

    @property
    def kw_min_length(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_MIN_LENGTH)

    @property
    def kw_max_length(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_MAX_LENGTH)

    @property
    def kw_items(self) -> Optional[List["SchemaNode"]]:
        "items can be either an object either a list of object"
        items = self.get_keyword(KW_ITEMS) or []
        if type(items) == List:
            return items.array_items

        return [items]

    @property
    def kw_min_items(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_MIN_ITEMS)

    @property
    def kw_max_items(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_MAX_ITEMS)

    @property
    def kw_unique_items(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_UNIQUE_ITEMS)

    @property
    def kw_additional_items(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_ADDITIONAL_ITEMS)

    @property
    def kw_contains(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_CONTAINS)

    @property
    def kw_required(self) -> Optional["SchemaNode"]:
        return self.get_keyword(KW_REQUIRED)

    @property
    def title(self) -> Optional[str]:
        title_kw = self.get_keyword(KW_TITLE)
        if not title_kw:
            return None
        title = title_kw.literal
        title = cast(str, title)
        return title

    @property
    def property_name(self) -> Optional[str]:
        return self.parent_key

    @property
    def property_display_name(self) -> Optional[str]:
        """The name to display in documentation for this property.

        This is simply the property name unless it is under "patternProperties" and it has a title,
        in which case it is that title
        """
        if self.is_pattern_property:
            return self.title or self.parent_key
        if self.is_additional_properties:
            return "Additional Properties"
        return self.parent_key

    @property
    def type_name(self) -> str:
        name = get_type_name(self)

        if name:
            return name

        seen = set()
        current_node = self
        while not name and current_node.refers_to:
            if current_node in seen:
                break
            seen.add(current_node)
            referenced_schema = current_node.refers_to
            name = get_type_name(referenced_schema)
            current_node = referenced_schema

        return name or TYPE_OBJECT

    def should_be_a_link(self, config: GenerationConfiguration) -> bool:
        """Check if this node should be displayed as a link to another section of the schema in the context of
        the provided configuration.
        """
        if not self.links_to or self.is_displayed:
            return False

        if config.link_to_reused_ref:
            return True

        return self.has_circular_reference(config)

    def node_is_parent(self, node_to_check: "SchemaNode") -> bool:
        """Check if the provided node is a parent of the current node"""
        if self.file != node_to_check.file:
            return False

        for i, path_part in enumerate(node_to_check.path_to_element):
            if len(self.path_to_element) <= i:
                return False
            if self.path_to_element[i] != path_part:
                return False
        return True

    def has_circular_reference(self, config: GenerationConfiguration) -> bool:
        """Check if the current schema is a reference to another section that references the current schema.

        The check is recursive up to config.recursive_detection_depth levels, meaning that if the node refers to another
        node that refers to another node that refers to a parent of itself, this will still return True if, and only if,
        it takes less than config.recursive_detection_depth steps to get to the parent.
        """
        if self in circular_references:
            return circular_references[self]

        if not self.links_to:
            circular_references[self] = False
            return False

        iteration_count = 0
        to_check = {self.links_to}
        while to_check and iteration_count < config.recursive_detection_depth:
            for node_to_check in to_check:
                # If the node reached via reference, keywords, or array items is the node itself, we have a circular
                # reference.
                # We also check if the path is for a parent to save on cycles
                if node_to_check == self or self.node_is_parent(node_to_check):
                    circular_references[self] = True
                    return True

            new_to_check: Set[SchemaNode] = set()
            for node_to_check in to_check:
                if node_to_check.links_to:
                    new_to_check.add(node_to_check.links_to)
                new_to_check = new_to_check.union(
                    set(n for n in node_to_check.keywords.values() if isinstance(n, SchemaNode))
                )
                new_to_check = new_to_check.union(set(node_to_check.array_items))
            to_check = new_to_check
            iteration_count += 1

        circular_references[self] = False
        return False

    def __eq__(self, other: object) -> bool:
        """For two schema nodes to be considered equals they must represent the same element in the same file"""
        if other is None:
            return False

        if not isinstance(other, SchemaNode):
            return NotImplemented

        return self.file == other.file and self.path_to_element == other.path_to_element

    def __hash__(self) -> int:
        return hash(self.file + self.flat_path)

    def __str__(self) -> str:
        return self.flat_path


class MdTemplate(object):
    def __init__(self, config):
        self.headings = {}
        self.auto_generated_heading = 0
        self.toc = {}
        self.config = config

    def registerJinja(self, env: jinja2.Environment):
        env.filters["md_get_numeric_minimum_restriction"] = self.get_numeric_minimum_restriction
        env.filters["md_get_numeric_maximum_restriction"] = self.get_numeric_maximum_restriction
        env.filters["md_escape_for_table"] = self.escape_for_table
        env.filters["md_heading"] = self.heading
        env.filters["md_properties_table"] = self.properties_table
        env.filters["md_type_info_table"] = self.type_info_table
        env.filters["md_array_restrictions"] = self.array_restrictions
        env.filters["md_array_items_restrictions"] = self.array_items_restrictions
        env.filters["md_array_items"] = self.array_items
        env.filters["md_restrictions_table"] = self.restrictions_table
        env.filters["md_generate_table"] = self.generate_table
        env.filters["md_first_line"] = self.first_line

        env.globals["md_badge"] = self.badge
        env.globals["md_get_toc"] = self.get_toc

    def get_numeric_minimum_restriction(self, schema_node: SchemaNode, default: str = "N/A") -> str:
        """Filter. Get the text to display about minimum restriction on a numeric type(integer or number)"""
        minimum = schema_node.keywords.get(MINIMUM)
        if minimum:
            minimum = minimum.literal
        exclusive_minimum = schema_node.keywords.get(EXCLUSIVE_MINIMUM)
        if exclusive_minimum:
            exclusive_minimum = exclusive_minimum.literal

        # Fix minimum and exclusive_minimum both there
        if minimum is not None and exclusive_minimum is not None:
            if minimum <= exclusive_minimum:
                exclusive_minimum = None
            else:
                minimum = None

        minimum_fragment = default
        if minimum is not None:
            minimum_fragment = f"&ge; {minimum}"
        if exclusive_minimum is not None:
            minimum_fragment = f"&gt; {exclusive_minimum}"

        return minimum_fragment

    def get_numeric_maximum_restriction(self, schema_node: SchemaNode, default: str = "N/A") -> str:
        """Filter. Get the text to display about maximum restriction on a numeric type(integer or number)"""
        maximum = schema_node.keywords.get(MAXIMUM)
        if maximum:
            maximum = maximum.literal
        exclusive_maximum = schema_node.keywords.get(EXCLUSIVE_MAXIMUM)
        if exclusive_maximum:
            exclusive_maximum = exclusive_maximum.literal

        # Fix maximum and exclusive_maximum both there
        if maximum is not None and exclusive_maximum is not None:
            if maximum > exclusive_maximum:
                exclusive_maximum = None
            else:
                maximum = None

        maximum_fragment = default
        if maximum is not None:
            maximum_fragment = f"&le; {maximum}"
        if exclusive_maximum is not None:
            maximum_fragment = f"&lt; {exclusive_maximum}"

        return maximum_fragment

    def escape_for_table(self, example_text: str) -> str:
        """Filter. escape characters('|', '`') in string to be inserted into markdown table"""
        return example_text.translate(str.maketrans({"|": "\\|", "`": "\\`"}))

    def heading(self, title: str, depth: int, html_id: Union[bool, str] = False) -> str:
        """
        Filter. display heading menu, heading number automatically calculated
        from previous heading and depth provided
        """
        if not (html_id):
            self.auto_generated_heading = self.auto_generated_heading + 1
            html_id = f"autogenerated_heading_{self.auto_generated_heading}"
        if not (title and title.strip()):
            title = "Auto generated title"
        else:
            title = title.strip()

        # reset heading depth greater than current depth
        for curDepth in range(depth + 1, max(self.headings, key=int) + 1 if self.headings else depth + 1):
            self.headings.pop(curDepth, None)

        # compute heading, for each depth get last level, and increment level of asked depth
        headingNumbers = ""
        for curDepth in range(0, depth + 1):
            if curDepth in self.headings:
                if curDepth == depth:
                    self.headings[curDepth] = self.headings[curDepth] + 1
            else:
                self.headings[curDepth] = 1
            if curDepth != 0:
                headingNumbers += f"{self.headings[curDepth]}."

        # markdown menu depth
        menu = "#" * (depth + 1)

        # generate markdown title with anchor (except if depth 0)
        if depth == 0:
            menu += f" {title}"
        else:
            menu += f' <a name="{html_id}"></a>{headingNumbers} {title}'

        # store current heading in toc
        toc_menu = f"[{headingNumbers} {title}](#{html_id})"
        self.toc[headingNumbers] = {"depth": depth, "menu": toc_menu}

        return menu

    def get_toc(self) -> str:
        """
        generate Table Of Content from the heading that have been generated
        """
        tocStr = ""

        firstHeadingDepth = False
        secondHeadingDepth = False
        for heading in self.toc:
            menu = self.toc[heading]
            # ignore first heading
            if type(firstHeadingDepth) == type(False):
                firstHeadingDepth = menu["depth"]
                continue
            if type(secondHeadingDepth) == type(False):
                secondHeadingDepth = menu["depth"]
            # ensure we have no space at first level for TOC to be recognized
            indent = "  " * (menu["depth"] - secondHeadingDepth)
            tocStr += indent + "- " + menu["menu"] + "\n"

        return tocStr

    def link(self, title, link, tooltip="") -> str:
        "Makdown link"
        return f"[{title}](#{link} {tooltip})"

    def badge(self, name: str, color: str, value: str = "") -> str:
        """
        Badge as markdown image link if badge_as_image option set
        otherwise Badge as text
        """
        if self.config.template_md_options["badge_as_image"]:
            valueStr = ""
            if value and len(value) > 0:
                valueStr = "-" + quote_plus(value)
            name = quote_plus(name)
            color = quote_plus(color)
            return f"![badge](https://img.shields.io/badge/{name}{valueStr}-{color})"
        else:
            if value and len(value) > 0:
                return f"[{name}: {value}]"
            return f"[{name}]"

    def properties_table(self, schema: SchemaNode) -> List[List]:
        """
        Generate list of properties ready to be rendered by generate_table filter
        """
        properties = []
        for sub_property in schema.iterate_properties:
            line = []
            # property name
            propertyName = "+ " if sub_property.is_required_property else "- "
            propertyName += self.link(self.escape_for_table(sub_property.property_name), sub_property.html_id)
            line.append(propertyName)
            # pattern
            line.append("Yes" if sub_property.is_pattern_property else "No")
            # type
            line.append("Combination" if is_combining(sub_property) else self.escape_for_table(sub_property.type_name))
            # Deprecated
            line.append(self.badge("Deprecated", "red") if deprecated(self.config, sub_property) else "No")
            # Link
            if sub_property.should_be_a_link(self.config):
                line.append("Same as " + self.link(sub_property.links_to.link_name, sub_property.links_to.html_id))
            elif sub_property.refers_to:
                line.append("In " + sub_property.ref_path)
            else:
                line.append("-")

            # title or description
            description = get_description(sub_property) or "-"
            if sub_property.title:
                description = sub_property.title

            line.append(self.escape_for_table(self.first_line(description, 80)))

            properties.append(line)

        if len(properties) > 0:
            # add header
            properties.insert(0, ["Property", "Pattern", "Type", "Deprecated", "Definition", "Title/Description"])

        return properties

    def first_line(self, example_text: str, max_length=False) -> str:
        """first_line truncated but replace ` with ' to avoid to have only one ` to avoid issues with jekyll"""
        return first_line(example_text, max_length).translate(str.maketrans({"`": "'"}))

    def type_info_table(self, schema: SchemaNode) -> List[List]:
        """
        Schema type info table :
        - type,
        - additional properties,
        - default value,
        - definitions links
        ready to be rendered by generate_table filter
        """
        type_info = []

        schemaType = schema.type_name
        defaultValue = schema.default_value
        type_info.append(["Type", "`combining`" if is_combining(schema) else f"`{schemaType}`"])
        if deprecated(self.config, schema):
            type_info.append(["**Deprecated**", self.badge("Deprecated", "red")])

        type_info.append(["**Additional properties**", self.additional_properties(schema)])
        if schema.default_value:
            type_info.append(["**Default**", f"`{defaultValue}`"])
        if schema.should_be_a_link(self.config):
            schemaLinkName = schema.links_to.link_name
            htmlId = schema.links_to.html_id
            type_info.append(["**Same definition as**", f"`[{ schemaLinkName }](#{ htmlId })`"])
        elif schema.refers_to:
            type_info.append(["**Defined in**", schema.ref_path])

        return type_info

    def additional_properties(self, schema: SchemaNode) -> str:
        """additional properties badge generation"""
        additionalProperties = ""
        for sub_property in schema.iterate_properties:
            if sub_property.is_additional_properties:
                if sub_property.is_additional_properties_schema:
                    htmlId = sub_property.html_id
                    shouldConformBadge = self.badge("Should-conform", "blue")
                    additionalProperties = f'[{shouldConformBadge}](#{htmlId} "Each additional property must conform to the following schema")'
                    break
                else:
                    badgeAnyType = self.badge("Any type", "green", "allowed")
                    additionalProperties = f'[{badgeAnyType}](# "Additional Properties of any type are allowed.")'
                    break

        if len(additionalProperties) == 0:
            if schema.explicit_no_additional_properties:
                badgeNotAllowed = self.badge("Not allowed", "red")
                additionalProperties = f'[{badgeNotAllowed}](# "Additional Properties not allowed.")'
            else:
                badgeAllowed = self.badge("Any type", "green", "allowed")
                additionalProperties = f'[{badgeAllowed}](# "Additional Properties of any type are allowed.")'

        return additionalProperties

    def array_restrictions(self, schema: SchemaNode) -> List[List]:
        """
        array restrictions: min/max items, items unicity, additional items, Tuple validation
        ready to be rendered by generate_table filter
        """

        array_restrictions = []
        array_restrictions.append(["", "Array restrictions"])
        array_restrictions.append(["**Min items**", str(schema.kw_min_items.literal) if schema.kw_min_items else "N/A"])
        array_restrictions.append(["**Max items**", str(schema.kw_max_items.literal) if schema.kw_max_items else "N/A"])
        array_restrictions.append(
            [
                "**Items unicity**",
                "True" if schema.kw_unique_items and schema.kw_unique_items.literal == True else "False",
            ]
        )
        array_restrictions.append(
            [
                "**Additional items**",
                "True" if schema.kw_additional_items and schema.kw_additional_items.literal == True else "False",
            ]
        )
        array_restrictions.append(
            [
                "**Tuple validation**",
                "See below" if schema.kw_items or (schema.kw_contains and schema.kw_contains.literal != {}) else "N/A",
            ]
        )

        return array_restrictions

    def array_items_restrictions(self, schema: SchemaNode) -> List[List]:
        """
        Tuple validation restrictions
        ready to be rendered by generate_table filter
        """
        if not schema.kw_items:
            return []
        array_items_restrictions = []
        array_items_restrictions.append(["Each item of this array must be", "Description"])
        for idx, item in enumerate(schema.kw_items):
            itemLabel = item.name_for_breadcrumbs or "Array Item " + idx
            itemHtmlId = item.html_id
            array_items_restrictions.append(
                [
                    f"[{itemLabel}](#{itemHtmlId})",
                    self.escape_for_table(self.first_line(get_description(item) or "-", 80)),
                ]
            )

        return array_items_restrictions

    def array_items(self, schema: SchemaNode, title: str) -> List[List]:
        """
        List of array items
        ready to be rendered by generate_table filter
        """
        if not schema.array_items:
            return []
        array_items = []
        array_items.append([title])
        for idx, item in enumerate(schema.array_items):
            itemLabel = item.name_for_breadcrumbs or title + " " + idx
            itemHtmlId = item.html_id
            array_items.append([f"[{itemLabel}](#{itemHtmlId})"])

        return array_items

    def restrictions_table(self, schema: SchemaNode) -> List[List]:
        """
        String or numeric restrictions tables
        - min/max length
        - regexp pattern + link to regexp101
        - multipleOf
        - minimum/maximum
        ready to be rendered by generate_table filter
        """
        restrictions = []
        if schema.kw_min_length:
            restrictions.append(["**Min length**", str(schema.kw_min_length.literal)])
        if schema.kw_max_length:
            restrictions.append(["**Max length**", str(schema.kw_max_length.literal)])
        if schema.kw_pattern:
            patternCode = schema.kw_pattern.literal.replace("|", "\|")
            patternUrl = quote_plus(schema.kw_pattern.literal)
            exampleUrl = ""
            if len(schema.examples) > 0:
                exampleUrl = "&testString=" + quote_plus(schema.examples[0])
            restrictions.append(
                [
                    "**Must match regular expression**",
                    f"```{patternCode}``` [Test](https://regex101.com/?regex={patternUrl}{exampleUrl})",
                ]
            )
        if schema.keywords.get("multipleOf"):
            restrictions.append(["**Multiple of**", str(schema.keywords.get("multipleOf").literal)])
        if schema.keywords.get("minimum") or schema.keywords.get("exclusiveMinimum"):
            restrictions.append(["**Minimum**", str(self.get_numeric_minimum_restriction(schema))])
        if schema.keywords.get("maximum") or schema.keywords.get("exclusiveMaximum"):
            restrictions.append(["**Maximum**", str(self.get_numeric_maximum_restriction(schema))])

        if len(restrictions) > 0:
            # add header
            restrictions.insert(0, ["Restrictions", " "])

        return restrictions

    def generate_table(self, table: List[List]) -> List[List]:
        """
        Pretty print markdown table using list of rows.
        Assuming first row is header line.
        Ending with empty line for rendering bottom border.
        Each column is str padded to max size string in the column.
        """
        if len(table) == 0:
            return ""

        # compute max length of each column
        max_cell_length: Dict = {}
        for idxRow, row in enumerate(table):
            for idxCol, cell in enumerate(row):
                max_cell_length[idxCol] = max(max_cell_length.get(idxCol, 0), len(cell))

        # generate md table
        output = ""
        for idxRow, row in enumerate(table):
            for idxCol, cell in enumerate(row):
                output += "| " + cell.ljust(max_cell_length[idxCol], " ") + " "
            output += "|\n"
            # add header line
            if idxRow == 0:
                for idxCol, cell in enumerate(row):
                    output += "| " + "".ljust(max_cell_length[idxCol], "-") + " "
                output += "|\n"

        # add last empty row
        for cell in max_cell_length.values():
            output += "| " + "".ljust(cell, " ") + " "
        output += "|\n"

        return output


def build_intermediate_representation(
    schema_path: Union[str, TextIO],
    config: GenerationConfiguration,
    loaded_schemas: Optional[Dict[str, Any]] = None,
) -> SchemaNode:
    """Build a SchemaNode object representing a JSON schema with added metadata to help rendering as a documentation.

    The representation will resolve references and generate HTML ids for elements
    """
    resolved_references: Dict[str, Dict[str, SchemaNode]] = defaultdict(dict)

    def defaultdict_list() -> Dict[Any, List]:
        return defaultdict(list)

    reference_users: Dict[str, Dict[str, List[SchemaNode]]] = defaultdict(defaultdict_list)
    _loaded_schemas: Dict[str, Any]
    if loaded_schemas is None:
        _loaded_schemas = {}
    else:
        assert isinstance(loaded_schemas, dict) and all(
            isinstance(k, str) for k in loaded_schemas.keys()
        ), "loaded_schemas must be Dict[str, Any]"
        _loaded_schemas = loaded_schemas

    # Make sure schema_path is absolute, all symlinks are resolved
    if isinstance(schema_path, Path):
        schema_path = str(schema_path.resolve())
    elif isinstance(schema_path, str):
        schema_path = os.path.realpath(schema_path)
    else:
        # Assuming schema_path is a file object (TextIO)
        schema_path = os.path.realpath(schema_path.name)

    def _record_ref(schema_real_path: str, path_to_element: List[Union[str, int]], current_node: SchemaNode) -> None:
        """Record that the node is describing the schema at the provided path"""
        resolved_references[schema_real_path]["/".join(str(e) for e in path_to_element)] = current_node

    def _resolve_ref(
        current_node: SchemaNode, schema: Union[Dict, List, int, str]
    ) -> Tuple[Optional[SchemaNode], Optional[SchemaNode]]:
        """Resolve the $ref keyword

        2 values are returned:
         - The "links_to" value, which is the node to which the current node should point to. This is used when several
           nodes have the same reference.

           This value cannot be under #/definitions, since those are not displayed.

           If properties a and b both references #/definitions/common, only a will be documented and b will link to a.
           In that case, the method would return the tuple (a, common).

           This method makes sure that the final element to be fully documented is the one that is the less nested so
           that the information is closer to the user.
           If properties a/b and c both references #/definitions/common, then a/b will link to c (c, common) and c will
           refer to common directly (None, common)
        - The "refers_to" value which is where the definition is in the schema.

        In general:
        - If there is no $ref, return (None, None).
        - If there is a referenced element that was never encountered before, build that element and return it for both
          "links_to" and "refers_to".
        - If there is a referenced element that was already encountered:
          - Check for circular references, if there are, return (None, None)
          - Check if another built node references the same one. If that node is closer to the user, "links_to" will be
            that node. Otherwise "links_to" is the same as "refers_to". "refers_to" is the reference that was found.
        """
        if not isinstance(schema, Dict) or REF not in schema:
            return None, None

        reference_path = schema.get(REF)
        if not reference_path:
            return None, None

        # Reference found, resolve the path (format "#/a/b/c", "file.json#/a/b/c", or "file.json")
        if "#" not in reference_path:
            uri_part = reference_path
            anchor_part = ""
        else:
            uri_part, anchor_part = reference_path.split("#", maxsplit=1)
            anchor_part = anchor_part.strip("/")

        # Resolve file path portion of reference
        if uri_part:
            if uri_part.startswith("http"):
                referenced_schema_path = uri_part
            else:
                referenced_schema_path = os.path.realpath(os.path.join(os.path.dirname(current_node.file), uri_part))
        elif current_node.file.startswith("http"):
            referenced_schema_path = current_node.file
        else:
            referenced_schema_path = os.path.realpath(current_node.file)

        def _find_reference(path: str, anchor_path: str) -> Optional[SchemaNode]:
            resolved_references_for_this_schema = resolved_references[path]
            return resolved_references_for_this_schema.get(anchor_path)

        # Check if already loaded
        found_reference = _find_reference(referenced_schema_path, anchor_part)

        if found_reference == current_node:
            found_reference = None

        if found_reference:
            reference_users_for_this_schema = reference_users[found_reference.file][anchor_part]
            reference_users[referenced_schema_path][anchor_part].append(current_node)

            # Detect infinite loop
            ref_by_file = current_node.file
            ref_by_path = current_node.flat_path
            found_users = reference_users.get(ref_by_file, {}).get(ref_by_path)
            while found_users:
                new_found_users = []
                for found_user in found_users:
                    if found_user == current_node:
                        # Huh oh, this node refers to the current node, let's break the cycle!
                        return None, None
                    ref_by_file = found_user.file
                    ref_by_path = found_user.flat_path
                    found_users_for_this = reference_users.get(ref_by_file, {}).get(ref_by_path)
                    if found_users_for_this:
                        new_found_users += found_users_for_this
                found_users = new_found_users

            # Find the first displayed node following the references
            while not found_reference.is_displayed and found_reference.refers_to:
                if found_reference.refers_to == current_node:
                    break
                found_reference = found_reference.refers_to

            # Is someone else using the reference?
            if reference_users_for_this_schema:
                other_user = None
                other_is_better = False
                i_am_better = False
                for user in reference_users_for_this_schema:
                    if user == current_node or not user.is_displayed:
                        continue

                    if not other_user:
                        other_user = user

                    if user.depth < other_user.depth:
                        other_user = user

                    if other_user.depth < current_node.depth:
                        other_user = user
                        other_is_better = True
                        i_am_better = False
                    elif other_user.depth > current_node.depth:
                        other_is_better = False
                        i_am_better = True

                # There is at least one other node having the same reference as the current node.
                if other_is_better:
                    # The other referencing node is nearer to the user, so it will now be displayed
                    # We mark the current node as being hidden and linking to the other one
                    other_user.is_displayed = True
                    current_node.is_displayed = False
                    return other_user, found_reference
                elif i_am_better:
                    # The other referencing node is more nested, it should be hidden and link to the current node
                    # The current node will documented the element referenced by both
                    other_user.is_displayed = False
                    other_user.links_to = current_node
                    current_node.is_displayed = True
                    return found_reference, found_reference
                elif other_user and other_user.refers_to:
                    # Both nodes are the same depth. The other having been seen first,
                    # this node will be hidden and linked to the other node
                    current_node.is_displayed = False
                    return other_user, found_reference

            return found_reference, found_reference
        else:
            reference_users[referenced_schema_path][anchor_part].append(current_node)

        # Not an existing reference, so it shall be built
        referenced_schema_path_to_element = anchor_part.split("/")
        new_reference = _build_node(
            current_node.depth,
            current_node.html_id,
            current_node.breadcrumb_name,
            referenced_schema_path,
            referenced_schema_path_to_element,
            _load_schema(referenced_schema_path, referenced_schema_path_to_element),
            current_node.parent,
            current_node.parent_key,
        )
        return new_reference, new_reference

    def _load_schema(schema_uri: str, path_to_element: List[Union[str, int]]) -> Union[Dict, List, int, str]:
        """Load the schema at the provided path or URL.

        If the URI is for a local file, it must be a "realpath", meaning absolute and with symlinks resolved.

        Loaded paths are kept in memory as to ensure never loading the same file twice
        """
        if schema_uri in _loaded_schemas:
            loaded_schema = _loaded_schemas[schema_uri]
        else:
            if schema_uri.startswith("http"):
                if schema_uri.endswith(".yaml"):
                    loaded_schema = yaml.safe_load(requests.get(schema_uri).text)
                else:
                    loaded_schema = requests.get(schema_uri).json()
            else:
                with open(schema_uri, encoding="utf-8") as schema_fp:
                    _, extension = os.path.splitext(schema_uri)
                    if extension == ".json":
                        loaded_schema = json.load(schema_fp)
                    else:
                        loaded_schema = yaml.safe_load(schema_fp)
            _loaded_schemas[schema_uri] = loaded_schema

        if path_to_element:
            for path_part in path_to_element:
                if not path_part:
                    # Empty string
                    continue
                if isinstance(path_part, str):
                    loaded_schema = loaded_schema[path_part]
                elif isinstance(path_part, int):
                    loaded_schema = loaded_schema[path_part]

        return loaded_schema

    def _get_node_ref(schema: Union[int, str, List, Dict]) -> str:
        if isinstance(schema, dict) and REF in schema:
            return schema[REF]
        return ""

    def _build_node(
        depth: int,
        html_id: str,
        breadcrumb_name: str,
        schema_file_path: str,
        path_to_element: List[Union[str, int]],
        schema: Union[Dict, List, int, str],
        parent: Optional[SchemaNode] = None,
        parent_key: Optional[str] = None,
    ) -> SchemaNode:
        """Recursively build a schema representation

        :param depth: Number of levels from the root of the schema to this node. Used when there are references to
                      figure out the less nested one in order to display it.
        :param html_id: HTML ID for the current element. Used for anchor links.
        :param breadcrumb_name: Name of the node in the breadcrumbs
        :param schema_file_path: Real path to the schema (absolute path with symlinks resolved)
        :param path_to_element: Path from the root of the schema to the current element
        :param schema: The JSON schema part being represented
        :return: A representation of the schema
        """
        if not schema_file_path.startswith("http"):
            schema_file_path = os.path.realpath(schema_file_path)

        new_node = SchemaNode(
            depth,
            file=schema_file_path,
            path_to_element=path_to_element,
            html_id=html_id,
            breadcrumb_name=breadcrumb_name,
            parent=parent,
            parent_key=parent_key,
            ref_path=_get_node_ref(schema),
        )
        if html_id == "root":
            html_id = ""

        _record_ref(schema_file_path, path_to_element, new_node)

        if isinstance(schema, dict):
            keywords = {}
            pattern_id = 1
            for schema_key, schema_value in schema.items():
                # These won't be needed to render the documentation.
                # The definitions will be reached from references, otherwise they are useless
                if schema_key in ["$id", "$ref", "$schema", "definitions"]:
                    continue

                # Examples are rendered in JSON because they will be represented that way in the documentation,
                # no need for a SchemaNode object
                if schema_key == "examples":
                    keywords[schema_key] = [
                        json.dumps(example, indent=4, separators=(",", ": "), ensure_ascii=False)
                        for example in schema_value
                    ]
                    continue

                # The default value will be printed as-is, no need for a SchemaNode object
                if schema_key == "default":
                    keywords[schema_key] = json.dumps(schema_value, ensure_ascii=False)
                    continue

                if schema_key in KW_PROPERTIES:
                    for new_property_name, new_property_schema in schema_value.items():
                        new_html_id = html_id
                        new_html_id += "_" if html_id else ""
                        new_html_id += escape_property_name_for_id(new_property_name)
                        new_node.properties[new_property_name] = _build_node(
                            depth + 1,
                            new_html_id,
                            new_property_name,
                            schema_file_path,
                            copy.deepcopy(path_to_element) + [new_property_name],
                            new_property_schema,
                            new_node,
                            new_property_name,
                        )
                elif schema_key == KW_ADDITIONAL_PROPERTIES:
                    if schema_value == False:
                        new_node.no_additional_properties = True
                    else:
                        new_html_id = html_id
                        new_html_id += "_" if html_id else ""
                        new_html_id += KW_ADDITIONAL_PROPERTIES
                        new_node.additional_properties = _build_node(
                            depth + 1,
                            new_html_id,
                            KW_ADDITIONAL_PROPERTIES,
                            schema_file_path,
                            copy.deepcopy(path_to_element) + [KW_ADDITIONAL_PROPERTIES],
                            schema_value,
                            new_node,
                            KW_ADDITIONAL_PROPERTIES,
                        )
                elif schema_key == KW_PATTERN_PROPERTIES:
                    for new_property_name, new_property_schema in schema_value.items():
                        new_html_id = html_id
                        new_html_id += "_" if html_id else ""
                        new_html_id += f"pattern{pattern_id}"
                        pattern_id += 1
                        new_node.pattern_properties[new_property_name] = _build_node(
                            depth + 1,
                            new_html_id,
                            new_property_name,
                            schema_file_path,
                            copy.deepcopy(path_to_element) + [new_property_name],
                            new_property_schema,
                            new_node,
                            new_property_name,
                        )
                else:
                    # Add the property name (correctly escaped) to the ID
                    new_html_id = html_id
                    new_depth = depth
                    if schema_key not in [KW_PROPERTIES, KW_PATTERN_PROPERTIES]:
                        new_depth += 1
                        new_html_id += "_" if html_id else ""
                        if not parent_key == KW_PATTERN_PROPERTIES:
                            new_html_id += escape_property_name_for_id(schema_key)
                        else:
                            new_html_id += f"pattern{pattern_id}"
                            pattern_id += 1

                    keywords[schema_key] = _build_node(
                        new_depth,
                        new_html_id,
                        schema_key,
                        schema_file_path,
                        copy.deepcopy(path_to_element) + [schema_key],
                        schema_value,
                        parent=new_node,
                        parent_key=schema_key,
                    )
            new_node.keywords = keywords
        elif isinstance(schema, list):
            array_items = []
            for i, element in enumerate(schema):
                # Add the property name (correctly escaped) to the ID
                new_html_id = html_id + ("_" if html_id else "") + "i" + str(i)

                array_items.append(
                    _build_node(
                        depth + 1,
                        new_html_id,
                        f"item {i}",
                        schema_file_path,
                        path_to_element + [i],
                        element,
                        parent=new_node,
                    )
                )
            new_node.array_items = array_items

        else:
            new_node.literal = schema

        new_node.links_to, new_node.refers_to = _resolve_ref(new_node, schema)

        return new_node

    intermediate_representation = _build_node(0, "", "root", schema_path, [], _load_schema(schema_path, []))

    return intermediate_representation


def is_combining(schema_node: SchemaNode) -> bool:
    """Test if a schema is one of the combining schema keyword"""
    return bool({"anyOf", "allOf", "oneOf", "not"}.intersection(schema_node.keywords.keys()))


def is_text_short(text: str) -> bool:
    """Check if a string is short so that we can decide whether to make the section containing it expandable or not.
    The heuristic is counting 1 for each line + 1 for each group of 80 characters a line has
    """
    return sum((len(line) / 80 + 1) for line in str(text).splitlines()) < SHORT_DESCRIPTION_NUMBER_OF_LINES


def is_deprecated(_property_dict: Dict[str, Any]) -> bool:
    """Test. Check if a property is deprecated without looking in description"""
    return False


def is_deprecated_look_in_description(schema_node: SchemaNode) -> bool:
    """Test. Check if a property is deprecated looking in description"""
    if DESCRIPTION not in schema_node.keywords:
        return False

    return bool(re.match(DEPRECATED_PATTERN, schema_node.keywords[DESCRIPTION].literal))


def get_required_properties(schema_node: SchemaNode) -> List[str]:
    required_properties = schema_node.keywords.get("required") or []
    if required_properties:
        required_properties = [p.literal for p in required_properties.array_items]

    return required_properties


def get_first_property(schema_node: SchemaNode) -> Any:
    """
    Filter. get first property of given schema no matter the property key
    Usage:
    md template does not recurse on schema to render the if portion
    instead it renders the if in the heading directly
    """
    properties = schema_node.properties
    if not properties:
        return None
    firstPropertyName = next(iter(properties))
    return properties[firstPropertyName]


def get_undocumented_required_properties(schema_node: SchemaNode) -> List[str]:
    return list(set(get_required_properties(schema_node)).difference(schema_node.properties.keys()))


def python_to_json(value: Any) -> Any:
    """Filter. Return the value as it needs to be displayed in JSON

    Used to display a string literals more explicitly for default and const values.
    """
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"

    if isinstance(value, str) and not value.startswith('"'):
        return f'"{value}"'

    return value


def get_type_name(schema_node: SchemaNode) -> Optional[str]:
    """Filter. Return the type of a property taking into account the type of items for array and enum"""

    def _python_type_to_json_type(python_type: Type[Union[str, int, float, bool, list, dict]]) -> str:
        return {
            str: TYPE_STRING,
            int: TYPE_INTEGER,
            float: TYPE_NUMBER,
            bool: TYPE_BOOLEAN,
            list: TYPE_ARRAY,
            dict: TYPE_OBJECT,
        }.get(python_type, TYPE_STRING)

    def _enum_type(enum_values: List[SchemaNode]) -> str:
        enum_type_names = [
            _python_type_to_json_type(python_type_name)
            for python_type_name in set(type(v.literal) for v in enum_values)
        ]
        if enum_type_names:
            return f"{TYPE_ENUM} (of {' or '.join(enum_type_names)})"

        return TYPE_ENUM

    def _add_subtype_if_array(type_name: str):
        if type_name == TYPE_ARRAY:
            items = schema_node.keywords.get(ITEMS, None)
            if not items:
                return type_name

            subtype = items.keywords.get(TYPE)
            if subtype:
                subtype = subtype.literal
            if TYPE_ENUM in items.keywords:
                subtype = _enum_type(items.keywords[TYPE_ENUM].array_items)

            if not subtype:
                # Too complex to guess items
                return type_name

            type_name = f"{type_name} of {subtype}"

        return type_name

    if TYPE_CONST in schema_node.keywords:
        return TYPE_CONST
    if TYPE_ENUM in schema_node.keywords:
        return _enum_type(schema_node.keywords[TYPE_ENUM].array_items)

    type_node = schema_node.keywords.get(TYPE)
    if type_node:
        if type_node.array_items:
            type_names = [node.literal for node in type_node.array_items]
        else:
            type_names = [type_node.literal]
    else:
        return None

    type_names = [_add_subtype_if_array(type_name) for type_name in type_names]

    return ", ".join(type_names[:-1]) + (" or " if len(type_names) > 1 else "") + type_names[-1]


def _get_description(schema_node: SchemaNode) -> str:
    description = ""
    description_node = schema_node.keywords.get(DESCRIPTION)
    if description_node:
        description = description_node.literal

    seen = set()
    current_node = schema_node
    while not description and current_node.refers_to:
        if current_node in seen:
            break
        seen.add(current_node)
        referenced_schema = current_node.refers_to
        referenced_description_node = referenced_schema.keywords.get(DESCRIPTION)
        if referenced_description_node:
            description = referenced_description_node.literal
        current_node = referenced_schema

    return description


def get_description(schema_node: SchemaNode) -> str:
    """Filter. Get the description of a property or an empty string"""
    return _get_description(schema_node)


def get_description_remove_default(schema_node: SchemaNode) -> str:
    """Filter. From the description attribute of a property, return the description without any default values in it.
    Will also convert None to an empty string.
    """
    description = _get_description(schema_node)
    if not description:
        return ""

    match = re.match(DEFAULT_PATTERN, description)
    if not match:
        return description

    return description[match.span(1)[1] :].lstrip()


def get_default(schema_node: SchemaNode) -> str:
    """Filter. Return the default value for a property"""
    return schema_node.default_value


def get_default_look_in_description(schema_node: SchemaNode) -> str:
    """Filter. Get the default value of a JSON Schema property. If not set, look for it in the description."""
    default_value = schema_node.default_value
    if default_value:
        return default_value

    description = schema_node.keywords.get(DESCRIPTION)
    if not description:
        return ""
    description = description.literal

    match = re.match(DEFAULT_PATTERN, description)
    if not match:
        return ""

    return match.group(2)


def get_numeric_restrictions_text(schema_node: SchemaNode, before_value: str = "", after_value: str = "") -> str:
    """Filter. Get the text to display about restrictions on a numeric type(integer or number)"""
    multiple_of = schema_node.keywords.get(MULTIPLE_OF)
    if multiple_of:
        multiple_of = multiple_of.literal
    maximum = schema_node.keywords.get(MAXIMUM)
    if maximum:
        maximum = maximum.literal
    exclusive_maximum = schema_node.keywords.get(EXCLUSIVE_MAXIMUM)
    if exclusive_maximum:
        exclusive_maximum = exclusive_maximum.literal
    minimum = schema_node.keywords.get(MINIMUM)
    if minimum:
        minimum = minimum.literal
    exclusive_minimum = schema_node.keywords.get(EXCLUSIVE_MINIMUM)
    if exclusive_minimum:
        exclusive_minimum = exclusive_minimum.literal

    # Fix minimum and exclusive_minimum both there
    if minimum is not None and exclusive_minimum is not None:
        if minimum <= exclusive_minimum:
            exclusive_minimum = None
        else:
            minimum = None

    minimum_fragment = ""
    if minimum is not None:
        minimum_fragment += f"greater or equal to {before_value}{minimum}{after_value}"
    if exclusive_minimum is not None:
        minimum_fragment += f"strictly greater than {before_value}{exclusive_minimum}{after_value}"

    # Fix maximum and exclusive_maximum both there
    if maximum is not None and exclusive_maximum is not None:
        if maximum > exclusive_maximum:
            exclusive_maximum = None
        else:
            maximum = None

    maximum_fragment = ""
    if maximum is not None:
        maximum_fragment += f"lesser or equal to {before_value}{maximum}{after_value}"
    if exclusive_maximum is not None:
        maximum_fragment += f"strictly lesser than {before_value}{exclusive_maximum}{after_value}"

    result = "Value must be "
    touched = False
    if minimum_fragment:
        touched = True
        result += minimum_fragment
    if maximum_fragment:
        if touched:
            result += " and "
        touched = True
        result += maximum_fragment
    if multiple_of:
        if touched:
            result += " and "
        result += f"a multiple of {before_value}{multiple_of}{after_value}"

    return result if touched else ""


def escape_property_name_for_id(property_name: str) -> str:
    """Filter. Escape unsafe characters in a property name so that it can be used in a HTML id"""

    escaped = re.sub("[^0-9a-zA-Z_-]", "_", str(property_name))
    if not escaped[0].isalpha():
        escaped = "a" + escaped
    return escaped


def first_line(example_text: str, max_length=False) -> str:
    """
    Filter. retrieve first line of string + add ... at the end if text has multiple lines
    cut line at max_length
    """
    part_line = example_text.partition("\n")
    first_line = part_line[0]
    etc = (part_line[1] == "\n") or (len(first_line) > max_length)
    if max_length:
        first_line = first_line[:max_length]
    return first_line + (" ..." if etc else "")


def deprecated(config, schema: SchemaNode) -> bool:
    return is_deprecated_look_in_description(schema) if config.deprecated_from_description else is_deprecated(schema)


def highlight_json_example(example_text: str) -> str:
    """Filter. Return an highlighted version of the provided JSON text"""
    return highlight(example_text, JavascriptLexer(), HtmlFormatter())


def get_local_time() -> str:
    return datetime.now(tz=reference.LocalTimezone()).strftime("%Y-%m-%d at %H:%M:%S %z")


def generate_from_schema(
    schema_file: Union[str, Path, TextIO],
    loaded_schemas: Optional[Dict[str, Any]] = None,
    minify: bool = True,
    deprecated_from_description: bool = False,
    default_from_description: bool = False,
    expand_buttons: bool = False,
    link_to_reused_ref: bool = True,
    config: GenerationConfiguration = None,
) -> str:
    config = config or _get_final_config(
        minify=minify,
        deprecated_from_description=deprecated_from_description,
        default_from_description=default_from_description,
        expand_buttons=expand_buttons,
        copy_css=False,
        copy_js=False,
        link_to_reused_ref=link_to_reused_ref,
    )

    templates_directory = os.path.join(config.templates_directory, config.template_name)
    base_template_path = os.path.join(templates_directory, TEMPLATE_FILE_NAME)

    md = markdown2.Markdown(extras=config.markdown_options)
    loader = FileSystemLoader(templates_directory)
    env = jinja2.Environment(
        loader=loader,
        extensions=[loopcontrols],
        trim_blocks=(config.template_name == "md"),
        lstrip_blocks=(config.template_name == "md"),
    )
    if config.template_name == "md":
        mdTemplate = MdTemplate(config)
        mdTemplate.registerJinja(env)

    env.filters["markdown"] = (
        lambda text: jinja2.Markup(md.convert(text)) if config.description_is_markdown else lambda t: t
    )
    env.filters["python_to_json"] = python_to_json
    env.filters["get_default"] = get_default_look_in_description if config.default_from_description else get_default
    env.filters["get_type_name"] = get_type_name
    env.filters["get_description"] = (
        get_description_remove_default if config.default_from_description else get_description
    )
    env.filters["get_numeric_restrictions_text"] = get_numeric_restrictions_text

    env.filters["get_required_properties"] = get_required_properties
    env.filters["get_first_property"] = get_first_property
    env.filters["get_undocumented_required_properties"] = get_undocumented_required_properties
    env.filters["highlight_json_example"] = highlight_json_example
    env.filters["first_line"] = first_line

    env.tests["combining"] = is_combining
    env.tests["description_short"] = is_text_short
    env.tests["deprecated"] = lambda schema: deprecated(config, schema)
    env.globals["get_local_time"] = get_local_time

    with open(base_template_path, "r") as template_fp:
        template = env.from_string(template_fp.read())

    if isinstance(schema_file, list):
        # Backward compatibility
        schema_file = os.path.sep.join(schema_file)

    intermediate_schema = build_intermediate_representation(schema_file, config, loaded_schemas)

    rendered = template.render(schema=intermediate_schema, config=config)

    if minify:
        if config.template_name == "md":
            # remove multiple contiguous empty lines
            rendered = re.sub(r"\n\s*\n", "\n\n", rendered)
        else:
            rendered = htmlmin.minify(rendered)

    return rendered


def generate_from_filename(
    schema_file_name: Union[str, Path],
    result_file_name: str,
    minify: bool = True,
    deprecated_from_description: bool = False,
    default_from_description: bool = False,
    expand_buttons: bool = False,
    copy_css: bool = True,
    copy_js: bool = True,
    link_to_reused_ref: bool = True,
    config: GenerationConfiguration = None,
) -> None:
    """Generate the schema documentation from a filename"""
    config = config or _get_final_config(
        minify=minify,
        deprecated_from_description=deprecated_from_description,
        default_from_description=default_from_description,
        expand_buttons=expand_buttons,
        copy_css=copy_css,
        copy_js=copy_js,
        link_to_reused_ref=link_to_reused_ref,
    )

    if isinstance(schema_file_name, str):
        schema_file_name = os.path.realpath(schema_file_name)
    elif isinstance(schema_file_name, Path):
        schema_file_name = str(schema_file_name.resolve())

    rendered_schema_doc = generate_from_schema(
        schema_file_name,
        minify=minify,
        deprecated_from_description=deprecated_from_description,
        default_from_description=default_from_description,
        expand_buttons=expand_buttons,
        link_to_reused_ref=link_to_reused_ref,
        config=config,
    )

    copy_css_and_js_to_target(result_file_name, config)

    with open(result_file_name, "w", encoding="utf-8") as result_schema_doc:
        result_schema_doc.write(rendered_schema_doc)


def generate_from_file_object(
    schema_file: TextIO,
    result_file: TextIO,
    minify: bool = True,
    deprecated_from_description: bool = False,
    default_from_description: bool = False,
    expand_buttons: bool = False,
    copy_css: bool = True,
    copy_js: bool = True,
    link_to_reused_ref: bool = True,
    config: GenerationConfiguration = None,
) -> None:
    """Generate the JSON schema documentation from opened file objects for both input and output files. The
    result_file should be opened in write mode.
    """
    config = config or _get_final_config(
        minify=minify,
        deprecated_from_description=deprecated_from_description,
        default_from_description=default_from_description,
        expand_buttons=expand_buttons,
        copy_css=copy_css,
        copy_js=copy_js,
        link_to_reused_ref=link_to_reused_ref,
    )

    result = generate_from_schema(schema_file, config=config)

    copy_css_and_js_to_target(result_file.name, config)

    result_file.write(result)


def copy_css_and_js_to_target(result_file_path: str, config: GenerationConfiguration) -> None:
    """Copy the CSS and JS files needed to display the resulting page to the directory containing the result file"""
    files_to_copy = []
    if config.copy_css:
        files_to_copy.append(CSS_FILE_NAME)
    if config.copy_js:
        files_to_copy.append(JS_FILE_NAME)
    if not files_to_copy:
        return

    target_directory = os.path.dirname(result_file_path)
    source_directory = os.path.join(config.templates_directory, config.template_name)
    if target_directory == source_directory:
        return

    for file_to_copy in files_to_copy:
        source_file_path = os.path.join(source_directory, file_to_copy)
        if not os.path.exists(source_file_path):
            continue
        try:
            shutil.copy(source_file_path, os.path.join(target_directory, file_to_copy))
        except shutil.SameFileError:
            print(f"Not copying {file_to_copy} to {os.path.abspath(target_directory)}, file already exists")


def _get_final_config(
    minify: bool,
    deprecated_from_description: bool,
    default_from_description: bool,
    expand_buttons: bool,
    copy_css: bool,
    copy_js: bool,
    link_to_reused_ref: bool,
    config: Union[str, Path, TextIO, Dict[str, Any], GenerationConfiguration] = None,
    config_parameters: List[str] = None,
) -> GenerationConfiguration:
    if config:
        final_config = _load_config(config)
    else:
        final_config = GenerationConfiguration(
            minify=minify,
            deprecated_from_description=deprecated_from_description,
            default_from_description=default_from_description,
            expand_buttons=expand_buttons,
            link_to_reused_ref=link_to_reused_ref,
            copy_css=copy_css,
            copy_js=copy_js,
        )
        if (
            not minify
            or deprecated_from_description
            or default_from_description
            or expand_buttons
            or not link_to_reused_ref
        ):
            logging.info(CONFIG_DEPRECATION_MESSAGE)

    if config_parameters:
        final_config = _apply_config_cli_parameters(final_config, config_parameters)

    return final_config


def _load_config(
    config_parameter: Optional[Union[str, Path, TextIO, Dict[str, Any], GenerationConfiguration]]
) -> GenerationConfiguration:
    """Load the configuration from either the path (as str or Path) to a config file, the open config file object,
    The loaded config as a dict or the GenerateConfiguration object directly.
    """
    if config_parameter is None:
        return GenerationConfiguration()

    if isinstance(config_parameter, GenerationConfiguration):
        return config_parameter

    if isinstance(config_parameter, dict):
        config_dict = config_parameter
    elif isinstance(config_parameter, (str, Path)):
        if isinstance(config_parameter, str):
            real_path = os.path.realpath(config_parameter)
        else:
            real_path = str(config_parameter.resolve())
        with open(os.path.realpath(real_path), encoding="utf-8") as config_fp:
            config_dict = yaml.safe_load(config_fp.read())
    else:
        config_dict = yaml.safe_load(config_parameter.read())

    return GenerationConfiguration.from_dict(config_dict)


def _apply_config_cli_parameters(
    current_configuration: GenerationConfiguration, config_cli_parameters: List[str]
) -> GenerationConfiguration:
    if not config_cli_parameters:
        return current_configuration

    current_configuration_as_dict = current_configuration.to_dict()
    for parameter in config_cli_parameters:
        if "=" in parameter:
            parameter_name, parameter_value = parameter.split("=")
            try:
                parameter_value = json.loads(parameter_value)
            except JSONDecodeError:
                pass
        else:
            parameter_name = parameter
            if parameter_name.startswith("no_") or parameter_name.startswith("no-"):
                parameter_value = False
                parameter_name = parameter_name[3:]  # Strip the `no_`/`no-`
            else:
                parameter_value = True
        current_configuration_as_dict[parameter_name] = parameter_value

    return GenerationConfiguration.from_dict(current_configuration_as_dict)


@click.command()
@click.argument("schema_file", nargs=1, type=click.File("r", encoding="utf-8"))
@click.argument("result_file", nargs=1, type=click.File("w+", encoding="utf-8"), default="schema_doc.html")
@click.option(
    "--config-file", type=click.File("r", encoding="utf-8"), help="JSON or YAML file containing generation parameters"
)
@click.option(
    "--config",
    multiple=True,
    help="Override generation parameters from the configuration file. "
    "Format is parameter_name=parameter_value. For example: --config minify=false. Can be repeated.",
)
@click.option("--minify/--no-minify", default=True, help="Run minification on the HTML result")
@click.option(
    "--deprecated-from-description", is_flag=True, help="Look in the description to find if an attribute is deprecated"
)
@click.option(
    "--default-from-description", is_flag=True, help="Look in the description to find an attribute default value"
)
@click.option("--expand-buttons", is_flag=True, help="Add 'Expand all' and 'Collapse all' buttons at the top")
@click.option("--copy-css/--no-copy-css", default=True, help=f"Copy {CSS_FILE_NAME} to the folder of the result_file")
@click.option("--copy-js/--no-copy-js", default=True, help=f"Copy {JS_FILE_NAME} to the folder of the result_file")
@click.option(
    "--link-to-reused-ref/--no-link-to-reused-ref",
    default=True,
    help="If set and 2 parts of the schema refer to the same definition, the definition will only be rendered once "
    "and all other references will be replaced by a link.",
)
def main(
    schema_file: TextIO,
    result_file: TextIO,
    config_file: TextIO,
    config: List[str],
    minify: bool,
    deprecated_from_description: bool,
    default_from_description: bool,
    expand_buttons: bool,
    copy_css: bool,
    copy_js: bool,
    link_to_reused_ref: bool,
) -> None:
    start = datetime.now()
    config = _get_final_config(
        minify=minify,
        deprecated_from_description=deprecated_from_description,
        default_from_description=default_from_description,
        expand_buttons=expand_buttons,
        copy_css=copy_css,
        copy_js=copy_js,
        link_to_reused_ref=link_to_reused_ref,
        config=config_file,
        config_parameters=config,
    )

    generate_from_file_object(schema_file, result_file, config=config)
    duration = datetime.now() - start
    print(f"Generated {result_file.name} in {duration}")


if __name__ == "__main__":
    main()
