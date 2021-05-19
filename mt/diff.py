from mt.ef import DependencyReport, Dependency


class DiffReport:
    def __init__(self, left: DependencyReport, right: DependencyReport) -> None:
        super().__init__()
        self.left = left
        self.right = right

    def get_difference(self):
        left_dependencies = self.left.get_unique_dependencies()
        right_dependencies = self.right.get_unique_dependencies()

        def get_versions_of_dependency(deps, group_id, artifact_id):
            return set([d.version for d in deps if d.group_id == group_id and d.artifact_id == artifact_id])

        def ids(deps: list[Dependency]):
            return set([(d.group_id, d.artifact_id) for d in deps])

        intersection = ids(left_dependencies) & ids(right_dependencies)

        left_intersected_with_versions = {
            f"{group_id}:{artifact_id}": get_versions_of_dependency(left_dependencies, group_id, artifact_id) for
            group_id, artifact_id in intersection}

        right_intersected_with_versions = {
            f"{group_id}:{artifact_id}": get_versions_of_dependency(right_dependencies, group_id, artifact_id) for
            group_id, artifact_id in intersection}

        def is_different_by_versions(left_dep_versions, right_dep_versions):
            return len(left_dep_versions.difference(right_dep_versions)) > 0

        deps_with_different_versions = [k for k, v in left_intersected_with_versions.items() if
                                        is_different_by_versions(v, right_intersected_with_versions[k])]

        def sorted(v):
            l = list(v)
            l.sort()
            return l

        return {name: (sorted(left_intersected_with_versions[name]), sorted(right_intersected_with_versions[name])) for
                name in
                deps_with_different_versions}


class AbstractDiffReportRenderer:
    def __init__(self):
        pass

    def render(self, report: DiffReport):
        return NotImplementedError("render method is not implemented")

    def get_format(self):
        return NotImplementedError("get_format method is not implemented")


class TextDiffReportRenderer(AbstractDiffReportRenderer):

    def render(self, report: DiffReport):
        diff = report.get_difference()
        names = [d for d, _ in diff.items()]
        names.sort()

        def format_line(d):
            left_versions, right_versions = diff[d]
            return "{0: <75} {1: <20} {2: <20}".format(d, ",".join(left_versions), ",".join(right_versions))

        return "\n".join([format_line(name) for name in names])

    def get_format(self):
        return "txt"


DIFF_REPORT_RENDERERS = {r.get_format(): r for r in [TextDiffReportRenderer()]}
