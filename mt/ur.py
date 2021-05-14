import requests
from xml.etree import ElementTree as ET


class UpdateReport:
    def __init__(self):
        pass


class AbstractUpdateReportRenderer:
    def __init__(self):
        pass

    def render(self, report):
        return NotImplementedError("render method is not implemented")

    def get_format(self):
        return NotImplementedError("get_format method is not implemented")


class TextUpdateReportRenderer(AbstractUpdateReportRenderer):

    def __init__(self):
        super().__init__()

    def render(self, report):
        def dependency_to_string(dependency):
            (d, v) = dependency
            return f"{d.group_id}:{d.artifact_id} {d.version} {v}"

        return "\n".join([dependency_to_string(d) for d in report.to_update])

    def get_format(self):
        return "txt"


class HtmlUpdateReportRenderer(AbstractUpdateReportRenderer):

    def __init__(self):
        super().__init__()

    def render(self, report):
        header = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dependency Update Report</title>
</head>
<body>
<table>
    <thead>
    <tr>
        <td>Dependency</td>
        <td>Current Version</td>
        <td>Latest Version</td>
    </tr>
    </thead>
    <tbody> 
        """

        footer = """
    </tbody>
</table>
</body>
</html>
        """

        def dependency_to_table_row(dependency):
            d, v = dependency
            dependency_name = f"{d.group_id}:{d.artifact_id}"
            link = f"<a target='_blank' href='https://search.maven.org/artifact/{d.group_id}/{d.artifact_id}' >" \
                   f"{dependency_name}</a>"

            return f"<tr><td>{link}</td><td>{d.version}</td><td>{v}</td></tr>"

        rows = "\n".join([dependency_to_table_row(d) for d in report.to_update])

        return header.strip() + rows + footer.strip()

    def get_format(self):
        return "html"


def latest_version_of_dependency(group_id, artifact_id):
    url = f'https://repository.sonatype.org/service/local/artifact/maven?r=central-proxy&g={group_id}&a={artifact_id}&v=LATEST'
    response = requests.get(url)

    print(f"{url}:{response.status_code}")

    if response.status_code != 200:
        return None

    project_xml = ET.fromstringlist([response.content])

    version_tag = project_xml.find("version")
    parent_tag = project_xml.find("parent")

    if version_tag is None and parent_tag is None:
        print("Cannot get the version because version and parent tags are not present")
        return None
    elif version_tag is not None:
        return version_tag.text
    else:
        return parent_tag.find("version").text


def create_update_report_from_dependency_report(dependency_report):
    all_dependencies = [dependency for project in dependency_report.projects for dependency in project.dependencies]
    unique_dependencies = list(set(all_dependencies))
    unique_dependencies.sort()

    dependencies_with_latest_versions = [
        (dependency, latest_version_of_dependency(dependency.group_id, dependency.artifact_id)) for
        dependency in unique_dependencies
    ]

    report = UpdateReport()
    report.to_update = [(d, v) for d, v in dependencies_with_latest_versions if v is not None and v != d.version]
    return report


UPDATE_REPORT_RENDERERS = {r.get_format(): r for r in [TextUpdateReportRenderer(), HtmlUpdateReportRenderer()]}
