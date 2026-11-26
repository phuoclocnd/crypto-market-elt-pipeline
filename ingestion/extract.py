import os

import dlt
from dotenv import load_dotenv
from dlt.sources.rest_api import rest_api_source

load_dotenv()
coingecko_api_key = os.environ.get("COINGECKO_API_KEY")


def load_coingecko() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_coingecko",
        destination="duckdb",
        dataset_name="rest_api_data",
    )

    coingecko_source = rest_api_source(
        {
            "client": {
                "base_url": "https://api.coingecko.com/api/v3/",
                "auth": {
                    "type": "api_key",
                    "name": "x-cg-demo-api-key",
                    "api_key": coingecko_api_key,
                },
                "paginator": {
                    "type": "page_number",
                    "base_page": 1,
                    "page_param": "page",
                    "maximum_page": 5,
                    "stop_after_empty_page": True,
                },
            },
            "resource_defaults": {
                "endpoint": {
                    "params": {
                        "vs_currency": "usd",
                        "per_page": 100,
                    },
                },
            },
            "resources": [
                {
                    "name": "coins_markets",
                    "endpoint": {"path": "coins/markets"},
                },
            ],
        }
    )

    load_info = pipeline.run(coingecko_source)
    print(load_info)


if __name__ == "__main__":
    load_coingecko()