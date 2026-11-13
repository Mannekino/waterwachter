"""
Collection of functions to interact with the WaterWebservices API
"""

import logging
import requests
from datetime import datetime

def load_locations():
    url = (
        "https://ddapi20-waterwebservices.rijkswaterstaat.nl/"
        "METADATASERVICES/OphalenCatalogus"
    )

    body = {
        "CatalogusFilter": {
            "Compartimenten": True
        }
    }

    response = requests.post(url, json=body)

    if response.status_code != 200:
        logging.error(f"Locaties laden mislukt: {response.status_code}")
        return None

    data = response.json()
    logging.info("Locaties succesvol geladen.")
    return data["LocatieLijst"]

def get_latest_measurements(location_code):
    url = (
        "https://ddapi20-waterwebservices.rijkswaterstaat.nl/"
        "ONLINEWAARNEMINGENSERVICES/OphalenLaatsteWaarnemingen"
    )

    body = {
        "AquoPlusWaarnemingMetadataLijst": [
            {
                "AquoMetadata": {
                    "Compartiment": {
                        "Code": "OW"
                    }
                }
            }
        ],
        "LocatieLijst": [
            {
                "Code": location_code
            }
        ]
    }

    response = requests.post(url, json=body)

    if response.status_code != 200:
        logging.error(f"Meetgegevens ophalen mislukt: {response.status_code}")
        return None

    logging.info(f"Metingen succesvol opgevraagd voor locatie: {location_code}")

    data = response.json()

    latest = {}

    for waarneming in data["WaarnemingenLijst"]:
        code = waarneming["AquoMetadata"]["Grootheid"]["Code"]

        # Filter on water level (waterhoogte) and flow rate (debiet) measurements
        if code not in ["WATHTE", "Q"]:
            continue

        tijdstip = datetime.fromisoformat(waarneming["MetingenLijst"][0]["Tijdstip"])

        if code not in latest:
            latest[code] = waarneming

        else:
            bestaand = datetime.fromisoformat(latest[code]["MetingenLijst"][0]["Tijdstip"])

            if tijdstip > bestaand:
                latest[code] = waarneming

    if not latest:
        logging.info(f"Geen waterhoogte- of debietmetingen beschikbaar voor {location_code}")
        return None

    return latest