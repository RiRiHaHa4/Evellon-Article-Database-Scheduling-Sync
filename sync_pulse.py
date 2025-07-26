#!/usr/bin/env python3
"""Turn 'Scheduled' → 'Live' when Publish Date arrives and optionally update Status."""
import os
from datetime import date
from notion_client import Client, APIResponseError

try:
    notion = Client(auth=os.environ["NOTION_TOKEN"])
    DB_ID = "2151f2862b90802aba98fc99afda5cd3"
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
        page_id = page["id"]
        current_status = page["properties"].get("Status", {}).get("select", {}).get("name")

        # Build update payload
        update_payload = {
            "Pulse": {
                "select": {"name": "Live"}
            }
        }

        if current_status == "Complete":
            update_payload["Status"] = {
                "select": {"name": "Published"}
            }

        notion.pages.update(
            page_id=page_id,
            properties=update_payload
        )

        print(f"➡️ Page updated: Pulse → Live", end="")
        if current_status == "Complete":
            print(", Status → Published")
        else:
            print("")

    print("✅ All updates complete.")

except APIResponseError as e:
    print("❌ Notion API error:", e)
    exit(1)
except Exception as ex:
    print("❌ Unexpected error:", str(ex))
    exit(1)
