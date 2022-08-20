from datetime import datetime
import os

import requests
from parsedatetime import Calendar


def main():
    terms = [
        "minutes",
        "meeting",
        "commission",
        "library",
        "finance",
        "cannabis",
        "arts",
        "aging",
        "disability",
        "childhood",
        "health",
        "disaster",
        "downtown",
        "elmwood",
        "energy",
        "transportation",
        "campaign",
        "homeless",
        "housing",
        "welfare",
        "redistricting",
        "joint",
        "landmarks",
        "medical",
        "loan",
        "peace",
        "personnel",
        "planning",
        "police",
        "public",
        "redevelopment",
        "successor",
        "sugar",
        "waterfront",
        "youth",
        "waste",
    ]

    for term in terms:
        json_data = {
            "SearchText": term,
            "QueryID": 115,
            "Keywords": [
                {
                    "ID": 123,
                    "Value": "",
                    "KeywordOperator": "=",
                },
            ],
            "QueryLimit": 0,
        }
        fetch(json_data)


def fetch(json_data):

    calendar = Calendar()

    cookies = {
        "cookiesession1": "678A3E8EC1F0126650FA101BAC3C9DBE",
        "ASP.NET_SessionId": "jqf1abt2fo1c10svhzkurz22",
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://records.cityofberkeley.info",
        "Referer": "https://records.cityofberkeley.info/PublicAccess/paFiles/cqFiles/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    response = requests.post(
        "https://records.cityofberkeley.info/PublicAccess/api/DocumentType/FullTextSearch",
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    items = response.json()["Data"]
    print(f"fetched {len(items)} for {json_data['SearchText']}")
    for item in items:
        try:
            # raw_date, _, body_name, _, _ = item["Name"].split("; ")
            metadata = item["Name"].split("; ")
            raw_date = metadata[0]
            body_name = metadata[2]
        except:
            print(item["Name"])
            continue
        time_struct, _ = calendar.parse(raw_date)
        current_item_datetime = datetime(*time_struct[:6])
        date_string = current_item_datetime.strftime("%Y-%m-%d")
        body_name = (
            body_name.replace(" of ", "Of")
            .replace(" on ", "On")
            .replace(" and ", "And")
            .replace(" ", "")
        )
        if not body_name:
            print(item["Name"])
            continue
        directory = f"./data/{body_name}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = date_string + ".pdf"
        filepath = f"{directory}/{filename}"
        if os.path.exists(filepath):
            continue
        pdf_url = f"https://records.cityofberkeley.info/PublicAccess/api/Document/{item['ID'].replace('=', '%3D')}"
        pdf_response = requests.get(pdf_url, allow_redirects=True)
        with open(filepath, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)
    print(f"done fetching for {json_data['SearchText']}")


if __name__ == "__main__":
    main()
