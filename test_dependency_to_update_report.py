import unittest

from mt.ef import decode_dependency_report_json_file
from mt.ur import create_update_report_from_dependency_report, latest_version_of_dependency, UPDATE_REPORT_RENDERERS, \
    UpdateReport


class UpdateReportTest(unittest.TestCase):
    def test_latest_version_retrieval(self):
        latest_version_of_flying_saucer = latest_version_of_dependency("org.xhtmlrenderer", "flying-saucer-pdf")
        print(latest_version_of_flying_saucer)
        self.assertIsNotNone(latest_version_of_flying_saucer)
        self.assertIsNone(latest_version_of_dependency("org.xhtmlrendere", "flying-saucer-pdf"))
        self.assertIsNotNone(latest_version_of_dependency("com.afrunt", "jach"))

    @staticmethod
    def create_update_report() -> UpdateReport:
        dependency_report = decode_dependency_report_json_file("sample-data/dependency-report.json")
        return create_update_report_from_dependency_report(dependency_report)

    def test_create_update_report_from_dependency_report(self):
        self.assertIsNotNone(self.create_update_report())

    def test_text_renderer(self):
        update_report = self.create_update_report()

        renderer = UPDATE_REPORT_RENDERERS["txt"]

        txt_report = renderer.render(update_report)

        self.assertIsNotNone(txt_report)

        print(txt_report)

        self.assertTrue("org.xhtmlrenderer:flying-saucer-pdf 9.1.20 9.1.22" in txt_report)

    def test_html_renderer(self):
        update_report = self.create_update_report()

        renderer = UPDATE_REPORT_RENDERERS["html"]

        html_report = renderer.render(update_report)

        self.assertIsNotNone(html_report)

        print(html_report)

        self.assertTrue("org.xhtmlrenderer:flying-saucer-pdf" in html_report)


if __name__ == '__main__':
    unittest.main()
