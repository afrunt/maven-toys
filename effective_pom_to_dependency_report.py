""" This script converts effective pom.xml to dependency report in JSON format """

import xml.etree.ElementTree as ET

EXIT_CODE_OK, EXIT_CODE_ERROR = 0, 1

XML_NS_POM = "http://maven.apache.org/POM/4.0.0"


class Project:
    def __init__(self):
        pass


class Dependency:
    def __init__(self):
        pass


def pom_ns_tag_name(tag):
    return "{%s}%s" % (XML_NS_POM, tag)


def child_tag_to_text(parent, tag):
    return child_tag_to(parent, tag, lambda e: e.text, None)


def child_tag_to(parent, tag, func, default):
    element = parent.find(pom_ns_tag_name(tag))
    return func(element) if element is not None else default


def xml_element_to_dependency(element):
    dependency = Dependency()
    dependency.group_id = child_tag_to_text(element, "groupId")
    dependency.artifact_id = child_tag_to_text(element, "artifactId")
    dependency.version = child_tag_to_text(element, "version")
    dependency.scope = child_tag_to_text(element, "scope")
    return dependency


def xml_element_to_project(element):
    project = Project()
    project.group_id = child_tag_to_text(element, "groupId")
    project.artifact_id = child_tag_to_text(element, "artifactId")
    project.version = child_tag_to_text(element, "version")
    project.packaging = child_tag_to_text(element, "packaging")

    project.dependencies = child_tag_to(element, "dependencies", lambda deps: [xml_element_to_dependency(d) for d in deps], [])

    return project


def parse_effective_pom_xml(file_path):
    return [xml_element_to_project(element) for element in ET.parse(file_path).getroot()]
