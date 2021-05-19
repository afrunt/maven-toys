import argparse
import sys

from mt.diff import DIFF_REPORT_RENDERERS, DiffReport
from mt.ef import EXIT_CODE_ERROR, decode_dependency_report_json_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create report with version difference between two dependency reports')
    parser.add_argument("--left", help="left dependency report file", required=True)
    parser.add_argument("--right", help="right dependency report file", required=True)
    parser.add_argument("--diff", help="resulting diff report file", required=True)
    parser.add_argument("--formats", help="Comma separated list of output formats [txt]", default="txt")

    args = parser.parse_args()

    formats = args.formats.split(",")

    for fmt in formats:
        if DIFF_REPORT_RENDERERS[fmt] is None:
            print(f"Unknown format {fmt}")
            sys.exit(EXIT_CODE_ERROR)

    left = decode_dependency_report_json_file(args.left)
    right = decode_dependency_report_json_file(args.right)
    diff_report = DiffReport(left, right)

    for fmt in formats:
        file_path = args.diff + f".{fmt}"
        with open(file_path, "w") as file:
            print(f"Writing report to {file_path}")
            file.write(DIFF_REPORT_RENDERERS[fmt].render(diff_report))
