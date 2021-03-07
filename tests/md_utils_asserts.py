import os

from json_schema_for_humans.generate import generate_from_schema, GenerationConfiguration
from tests.test_utils import get_test_case_path
import re


class MdUtilsAsserts:
    @staticmethod
    def generate_case(case_name: str, config: GenerationConfiguration = None) -> str:
        """Get the generated markdown schema string for a given schema test case"""
        return generate_from_schema(get_test_case_path(case_name), None, config=config)

    @staticmethod
    def get_expected_case(case_dir: str, test_case: str, case_name: str) -> str:
        """Get the content of case_dir/test_case/case_name.md - containing expected result"""
        file = os.path.realpath(os.path.join(os.path.dirname(__file__), case_dir, test_case, f"{case_name}.md"))
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        return content

    def assert_case_equals(
        self,
        case_dir: str,
        test_case: str,
        case_name: str,
        config: GenerationConfiguration = None,
        expected_case_name: str = "",
    ) -> None:
        content = self.generate_case(case_name, config)
        expected_content = self.get_expected_case(
            case_dir, test_case, expected_case_name if expected_case_name else case_name
        )

        # remove generation date on both contents
        regexp = r"^(Generated using \[json-schema-for-humans\]\(https:[^)]+\) on) (.+)$"
        content = re.sub(regexp, r"\1 date", content, flags=re.MULTILINE)

        assert expected_content == content
