""" This script converts effective pom.xml to dependency report in JSON format """

import xml.etree.ElementTree as ET

EXIT_CODE_OK, EXIT_CODE_ERROR = 0, 1

XML_NS_POM = "http://maven.apache.org/POM/4.0.0"


class Project:
    def __init__(self):
        pass


def pom_ns_tag_name(tag):
    return "{%s}%s" % (XML_NS_POM, tag)


def child_tag_text_or_none(parent, tag):
    element = parent.find(pom_ns_tag_name(tag))
    return element.text if element is not None else None


def xml_element_to_project(element):
    project = Project()
    for e in element:
        print(e)
    project.group_id = child_tag_text_or_none(element, "groupId")
    project.artifact_id = child_tag_text_or_none(element, "artifactId")
    project.version = child_tag_text_or_none(element, "version")
    project.packaging = child_tag_text_or_none(element, "packaging")
    return project


def parse_effective_pom_xml(file_path):
    return [xml_element_to_project(element) for element in ET.parse(file_path).getroot()]
