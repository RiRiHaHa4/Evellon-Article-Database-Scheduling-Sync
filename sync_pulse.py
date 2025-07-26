#!/usr/bin/env python3
"""Turn 'Scheduled' → 'Live' when Publish Date arrives."""
import os
from datetime import date
from notion_client import Client

notion = Client(auth=os.environ["NOTION_TOKEN"])
DB_ID = "2151f2862b90802aba98fc99afda5cd3"  # <-- replace this with your 32-character Notion DB ID
today = date.today().isoformat()

result = notion.databases.query(
    database_id=DB_ID,
    filter={
        "and": [
            {"property": "Publish Date", "date": {"on_or_before": today}},
            {"property": "Pulse", "multi_select": {"contains": "Scheduled"}}
        ]
    }
)

for page in result["results"]:
    notion.pages.update(
        page_id=page["id"],
        properties={
            "Pulse": {
                "multi_select": [{"name": "Live"}]
            }
        }
    )

print(f"Marked {len(result['results'])} page(s) Live.")
