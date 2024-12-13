import argparse
import json
import pandas as pd
import os

METRIC_FILE_NAME = "metric.json"
REPORT_FILE_NAME = "report.csv"


def report_csv(
    report_file,
    report_date,
    total_active_users,
    total_engaged_users,
    total_code_suggestions,
    total_code_acceptances,
    total_code_lines_suggested,
    total_code_lines_accepted,
):
    # formatted_date = report_date.strftime("%Y-%m-%d")
    total_active_users = str(total_active_users)
    total_engaged_users = str(total_engaged_users)
    total_code_suggestions = str(total_code_suggestions)
    total_code_acceptances = str(total_code_acceptances)
    total_code_lines_suggested = str(total_code_lines_suggested)
    total_code_lines_accepted = str(total_code_lines_accepted)

    # Write the data line with commas between values
    line = (
        report_date
        + ","
        + total_active_users
        + ","
        + total_engaged_users
        + ","
        + total_code_suggestions
        + ","
        + total_code_acceptances
        + ","
        + total_code_lines_suggested
        + ","
        + total_code_lines_accepted
        + "\n"
    )
    report_file.write(line)


def get_metrics(data):
    report_file = open(REPORT_FILE_NAME, "w")
    report_file.write(
        "report_date,total_active_users,total_engaged_users,total_code_suggestions,total_code_acceptances,total_code_lines_suggested,total_code_lines_accepted\n"
    )
    for item in data:
        total_engaged_users = 0
        total_active_users = 0
        total_code_acceptances = 0
        total_code_suggestions = 0
        total_code_lines_accepted = 0
        total_code_lines_suggested = 0

        report_date = item["date"]
        total_active_users = total_active_users + item["total_active_users"]
        total_engaged_users = total_engaged_users + item["total_engaged_users"]
        if "copilot_ide_code_completions" in item:
            code_completions = item["copilot_ide_code_completions"]
            # print("Copilot IDE Code Completions:")
            if "editors" in code_completions:
                for editor in code_completions["editors"]:
                    # print(f"  Editor: {editor['name']}")
                    if "models" in editor:
                        for model in editor["models"]:
                            # print(f"    Model: {model['name']}")
                            if "languages" in model:
                                for language in model["languages"]:

                                    if "total_code_acceptances" in language:
                                        total_code_acceptances = (
                                            total_code_acceptances
                                            + language["total_code_acceptances"]
                                        )
                                    if "total_code_suggestions" in language:
                                        total_code_suggestions = (
                                            total_code_suggestions
                                            + language["total_code_suggestions"]
                                        )
                                    if "total_code_lines_accepted" in language:
                                        total_code_lines_accepted = (
                                            total_code_lines_accepted
                                        ) + language["total_code_lines_accepted"]

                                    if "total_code_lines_suggested" in language:
                                        total_code_lines_suggested = (
                                            total_code_lines_suggested
                                        ) + language["total_code_lines_suggested"]

        report_csv(
            report_file,
            report_date,
            total_active_users,
            total_engaged_users,
            total_code_suggestions,
            total_code_acceptances,
            total_code_lines_suggested,
            total_code_lines_accepted,
        )
    report_file.close


def convert_csv_to_excel(csv_file_path, excel_file_path, sheet_name):
    try:
        data = pd.read_csv(csv_file_path)

        data.to_excel(
            excel_file_path,
            sheet_name=sheet_name,
            index=False,
            engine="openpyxl",
        )

        print(f"Successfully converted {csv_file_path} to {excel_file_path}.")
    except Exception as e:
        print(f"Error during conversion: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get Copilot metrics for an enterprise."
    )

    parser.add_argument(
        "--enterprise", required=True, help="Your GitHub Enterprise name"
    )

    parser.add_argument("--uploadlocation", required=False, help="Upload location")
    args = parser.parse_args()

    METRIC_FILE_NAME = "out/" + args.enterprise + "-metrics.json"
    REPORT_FILE_NAME = "out/" + args.enterprise + "-metrics.csv"
    try:
        if os.path.exists(REPORT_FILE_NAME):
            os.remove(REPORT_FILE_NAME)
    except Exception as err:
        print(err)
    with open(METRIC_FILE_NAME, "r") as f:
        data = json.load(f)
    get_metrics(data)
    EXCEL_FILE_NAME = "out/" + args.enterprise + "-metrics.xlsx"
    try:
        if os.path.exists(EXCEL_FILE_NAME):
            os.remove(EXCEL_FILE_NAME)
    except Exception as err:
        print(err)
    sheet_name = args.enterprise + "-metrics"
    convert_csv_to_excel(REPORT_FILE_NAME, EXCEL_FILE_NAME, sheet_name)
    if args.uploadlocation != None:
        EXCEL_FILE_NAME = args.uploadlocation + args.enterprise + "-metrics.xlsx"
        convert_csv_to_excel(REPORT_FILE_NAME, EXCEL_FILE_NAME, sheet_name)
