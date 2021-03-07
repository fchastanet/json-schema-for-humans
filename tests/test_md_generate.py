import os
import pytest

from json_schema_for_humans.generate import GenerationConfiguration
from tests.md_utils_asserts import MdUtilsAsserts

configBadge = GenerationConfiguration(
    template_name="md", template_md_options={"badge_as_image": True, "toc_template_name": "classic"}
)
configNoBadge = GenerationConfiguration(
    template_name="md", template_md_options={"badge_as_image": False, "toc_template_name": "classic"}
)
testCases = []
cases_source_dir = os.path.join(os.path.dirname(__file__), "cases")

for case_name in os.listdir(cases_source_dir):
    name, ext = os.path.splitext(case_name)
    case_source = os.path.abspath(os.path.join(cases_source_dir, case_name))
    if not os.path.isfile(case_source) or ext != ".json":
        continue
    testCases.append(("with_badge", name, configBadge))
    testCases.append(("without_badge", name, configNoBadge))

toc_test_cases = []
toc_template_names = ("none", "classic")
for toc_template_name in toc_template_names:
    toc_test_cases.append((toc_template_name, "complex", "toc_with_badge", configBadge))
    toc_test_cases.append((toc_template_name, "complex", "toc_without_badge", configNoBadge))


class TestMdGenerate(MdUtilsAsserts):
    @pytest.mark.parametrize("testCase, schema, config", testCases)
    def test_basic(self, testCase, schema, config):
        """Test rendering a basic schema with title"""
        self.assert_case_equals("expected_md", testCase, schema, config)

    @pytest.mark.parametrize("toc_template_name, schema, testCase, config", toc_test_cases)
    def test_toc(self, toc_template_name, schema, testCase, config):
        """Test rendering a complex schema with different toc templates"""
        config.template_md_options["toc_template_name"] = toc_template_name
        self.assert_case_equals("expected_md", testCase, schema, config, f"{schema}_{toc_template_name}")
