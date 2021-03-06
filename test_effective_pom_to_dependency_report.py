import unittest

import mt.ef
from mt.ef import DependencyReport

SAMPLE_EFFECTIVE_POM_XML = "sample-data/effective-pom.xml"


class DependencyReportTest(unittest.TestCase):
    def test_parse_effective_pom_xml(self):
        projects = mt.ef.parse_effective_pom_xml(SAMPLE_EFFECTIVE_POM_XML)
        self.assertIsNotNone(projects)
        self.assertEqual(len(projects), 3)
        self.assertEqual(projects[0].packaging, "pom")
        self.assertEqual(projects[0].group_id, "org.example")
        self.assertEqual(projects[0].artifact_id, "sample-project")
        self.assertEqual(projects[0].version, "1.0-SNAPSHOT")
        self.assertIsNone(projects[1].packaging)
        self.assertIsNone(projects[2].packaging)

        self.assertIsNotNone(projects[1].dependencies)
        self.assertEqual(len(projects[1].dependencies), 1)
        self.assertEqual(projects[1].dependencies[0].artifact_id, "flying-saucer-pdf")
        self.assertEqual(projects[1].dependencies[0].version, "9.1.20")
        self.assertEqual(projects[1].dependencies[0].scope, "compile")

        self.assertIsNotNone(projects[2].dependencies)
        self.assertEqual(len(projects[2].dependencies), 1)
        self.assertEqual(projects[2].dependencies[0].artifact_id, "flying-saucer-pdf")
        self.assertEqual(projects[2].dependencies[0].version, "9.1.22")
        self.assertEqual(projects[2].dependencies[0].scope, "compile")

    def test_create_dependency_report_json(self):
        json = mt.ef.create_dependency_report_json(SAMPLE_EFFECTIVE_POM_XML)
        # print(json)
        self.assertIsNotNone(json)

    def test_decode_dependency_report_json(self):
        json = mt.ef.create_dependency_report_json(SAMPLE_EFFECTIVE_POM_XML)
        report = mt.ef.decode_dependency_report_json_string(json)
        self.assertIsNotNone(report)
        self.assertTrue(isinstance(report, DependencyReport))
        self.assertEqual(len(report.projects), 3)


if __name__ == '__main__':
    unittest.main()
