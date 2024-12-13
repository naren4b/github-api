import requests
import argparse
import json
import os


def save_to_file(file_name, data):
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
        data_file = open(file_name, "x+")
    except Exception as err:
        print(err)
    str = json.dumps(data, indent=4, sort_keys=True)
    data_file.write(str)
    print("Data saved to file: ", file_name)
    data_file.close


def get_copilot_metrics(GHC_TOKEN, ENTERPRISE, metrics_fileName):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GHC_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    url = f"https://api.github.com/enterprises/{ENTERPRISE}/copilot/metrics"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print(json.dumps(data, indent=4, sort_keys=True))
        save_to_file(metrics_fileName, data)
    else:
        print(f"Error: {response.status_code}")
        print(f"Error: {response.content}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get Copilot metrics for an enterprise."
    )
    parser.add_argument("--token", required=True, help="Your GitHub access token")
    parser.add_argument(
        "--enterprise", required=True, help="Your GitHub Enterprise name"
    )
    args = parser.parse_args()

    metrics_fileName = "out/" + args.enterprise + "-metrics.json"
    os.makedirs(os.path.dirname(metrics_fileName), exist_ok=True)
    get_copilot_metrics(args.token, args.enterprise, metrics_fileName)
