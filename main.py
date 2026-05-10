import argparse
import json
from api_search import fetch_api, search_in_json


def main():
    parser = argparse.ArgumentParser(description="Fetch an API URL and search results by keyword")
    parser.add_argument("--url", "-u", required=True, help="API base URL")
    parser.add_argument("--keyword", "-k", action="append", required=True, help="Keyword to search for (can specify multiple)")
    parser.add_argument("--params", "-p", help="Optional query params as JSON string, e.g. '{\"action\":\"query\"}'", default=None)
    args = parser.parse_args()

    params = None
    if args.params:
        try:
            params = json.loads(args.params)
        except Exception as e:
            print("Failed to parse --params as JSON:", e)
            return

    data = fetch_api(args.url, params=params)
    keywords = args.keyword
    matches = search_in_json(data, keywords)
    print(json.dumps({"matches": matches}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
