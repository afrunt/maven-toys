import unittest

import mt.ef
from mt.diff import DiffReport, TextDiffReportRenderer
from mt.ef import DependencyReport


class DifferenceReportTest(unittest.TestCase):

    def read_dependency_report(self, path) -> DependencyReport:
        return mt.ef.decode_dependency_report_json_file(path)

    def create_diff_report(self):
        left_report = self.read_dependency_report("sample-data/left-dependency-report.json")
        right_report = self.read_dependency_report("sample-data/right-dependency-report.json")
        return DiffReport(left_report, right_report)

    def test_difference_report(self):
        report = self.create_diff_report()
        diff = report.get_difference()
        self.assertIsNotNone(diff)

    def test_text_renderer(self):
        report = self.create_diff_report()
        renderer = TextDiffReportRenderer()
        text = renderer.render(report)
        self.assertIsNotNone(text)

        print(text)


if __name__ == '__main__':
    unittest.main()
