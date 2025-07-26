#!/usr/bin/env python3
"""Turn 'Scheduled' → 'Live' when Publish Date arrives."""
import os
from datetime import date
from notion_client import Client, APIResponseError

try:
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    DB_ID = "2151f2862b90802aba98fc99afda5cd3"  # ← Your actual database ID
    today = date.today().isoformat()

    print("🔍 Querying Notion database...")
    result = notion.databases.query(
        database_id=DB_ID,
        filter={
            "and": [
                {"property": "Publish Date", "date": {"on_or_before": today}},
                {"property": "Pulse", "select": {"equals": "Scheduled"}}
            ]
        }
    )

    print(f"✅ Found {len(result['results'])} matching page(s). Updating...")

    for page in result["results"]:
        notion.pages.update(
            page_id=page["id"],
            properties={
                "Pulse": {
                    "select": {"name": "Live"}
                }
            }
        )
    print("✅ Update complete.")

except APIResponseError as e:
    print("❌ Notion API error:", e)
    exit(1)
except Exception as ex:
    print("❌ Unexpected error:", str(ex))
    exit(1)
