import unittest

import effective_pom_to_dependency_report as ef


class DependencyReportTest(unittest.TestCase):
    def test_parse_effective_pom_xml(self):
        projects = ef.parse_effective_pom_xml("sample-data/effective-pom.xml")
        self.assertIsNotNone(projects)
        self.assertEqual(len(projects), 3)
        self.assertEqual(projects[0].packaging, "pom")
        self.assertEqual(projects[0].group_id, "org.example")
        self.assertEqual(projects[0].artifact_id, "sample-project")
        self.assertEqual(projects[0].version, "1.0-SNAPSHOT")
        self.assertIsNone(projects[1].packaging)
        self.assertIsNone(projects[2].packaging)


if __name__ == '__main__':
    unittest.main()
