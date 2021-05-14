""" This script converts effective pom.xml to dependency report in JSON format """
import argparse
import os
import sys

from mt.ef import create_dependency_report_json, EXIT_CODE_ERROR

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create dependency report from effective pom.xml')
    parser.add_argument('--effective_pom_file', help='Path to effective pom.xml', required=True)
    parser.add_argument('--report_file', help='Path to target dependency report', required=True)

    args = parser.parse_args()

    if not os.path.exists(args.effective_pom_file):
        print(f"{args.effective_pom_file} not found")
        sys.exit(EXIT_CODE_ERROR)

    with open(args.report_file, "w") as report_file:
        report_file.write(create_dependency_report_json(args.effective_pom_file))
