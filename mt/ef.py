from xml.etree import ElementTree as ET

import jsonpickle

EXIT_CODE_OK, EXIT_CODE_ERROR = 0, 1

XML_NS_POM = "http://maven.apache.org/POM/4.0.0"


class Project:
    def __init__(self):
        pass


class Dependency:
    def __init__(self, group_id, artifact_id, version, scope):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.scope = scope

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o) and self.__str__() == o.__str__()

    def __hash__(self) -> int:
        return self.__str__().__hash__()

    def __str__(self) -> str:
        return f"{self.group_id}:{self.artifact_id}:{self.version}"

    def __lt__(self, other):
        return str(self) < str(other)


class DependencyReport:
    def __init__(self):
        self.projects = []
        pass

    def get_unique_dependencies(self):
        all_dependencies = [dependency for project in self.projects for dependency in project.dependencies]
        unique_dependencies = list(set(all_dependencies))
        unique_dependencies.sort()
        return unique_dependencies


def pom_ns_tag_name(tag):
    return "{%s}%s" % (XML_NS_POM, tag)


def child_tag_to_text(parent, tag):
    return child_tag_to(parent, tag, lambda e: e.text, None)


def child_tag_to(parent, tag, func, default):
    element = parent.find(pom_ns_tag_name(tag))
    return func(element) if element is not None else default


def child_tags_text_to_tuple(parent, *args):
    return tuple([child_tag_to_text(parent, tag) for tag in args])


def xml_element_to_dependency(element):
    g, a, v, s = child_tags_text_to_tuple(element, "groupId", "artifactId", "version", "scope")
    dependency = Dependency(g, a, v, s)
    return dependency


def xml_element_to_project(element):
    project = Project()
    values = child_tags_text_to_tuple(element, "groupId", "artifactId", "version", "packaging")
    project.group_id = values[0]
    project.artifact_id = values[1]
    project.version = values[2]
    project.packaging = values[3]

    def dependencies_from_elements(dependencies_element):
        return [xml_element_to_dependency(d) for d in dependencies_element]

    project.dependencies = child_tag_to(element, "dependencies", dependencies_from_elements, [])
    project.dependencies.sort()
    return project


def parse_effective_pom_xml(file_path):
    return [xml_element_to_project(element) for element in ET.parse(file_path).getroot()]


def create_dependency_report(file_path):
    projects = parse_effective_pom_xml(file_path)
    report = DependencyReport()
    report.projects = projects
    return report


def encode_dependency_report_json(report):
    return jsonpickle.encode(report, indent=True)


def create_dependency_report_json(file_path):
    return jsonpickle.encode(create_dependency_report(file_path), indent=True)


def decode_dependency_report_json_string(string_json):
    return jsonpickle.decode(string_json)


def decode_dependency_report_json_file(path):
    with open(path, "r") as file:
        return jsonpickle.decode("".join(file.readlines()))
