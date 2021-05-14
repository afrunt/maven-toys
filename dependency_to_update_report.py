import argparse
import os
import sys

from mt.ef import EXIT_CODE_ERROR, decode_dependency_report_json_file
from mt.ur import create_update_report_from_dependency_report, UPDATE_REPORT_RENDERERS

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create update report from dependency report')
    parser.add_argument("--formats", help="Comma separated list of output formats [txt,html]", default="txt,html")
    parser.add_argument('--dependency_report_file', help='Path to source dependency report file', required=True)
    parser.add_argument('--report_file', help='Path to target update report file', required=True)

    args = parser.parse_args()

    if not os.path.exists(args.dependency_report_file):
        print(f"{args.dependency_report_file} not found")
        sys.exit(EXIT_CODE_ERROR)

    formats = args.formats.split(",")

    for fmt in formats:
        if UPDATE_REPORT_RENDERERS[fmt] is None:
            print(f"Unknown format {fmt}")
            sys.exit(EXIT_CODE_ERROR)

    dependency_report = decode_dependency_report_json_file(args.dependency_report_file)
    update_report = create_update_report_from_dependency_report(dependency_report)

    print("Updates are available for:")
    print(UPDATE_REPORT_RENDERERS["txt"].render(update_report))

    for fmt in formats:
        with open(args.report_file + f".{fmt}", "w") as file:
            file.write(UPDATE_REPORT_RENDERERS[fmt].render(update_report))
