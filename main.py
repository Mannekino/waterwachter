"""
Waterwachter

Command-line application for searching measurement locations and retrieving water measurement data from the
Rijkswaterstaat WaterWebservices API.
"""

import logging
import requests
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Configure application logging according to criteria 1.3
logging.basicConfig(
    filename="waterwachter.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console = Console()

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

    if response.status_code == 200:
        data = response.json()
        logging.info("Locaties succesvol geladen.")
        return data["LocatieLijst"]

    else:
        logging.error(f"Locaties laden mislukt: {response.status_code}")
        return None

def search_location(locations):
    query_location = Prompt.ask("Zoek op locatie").lower()

    if not query_location.strip():
        console.print(
            "[yellow]Voer een zoekterm in.[/yellow]"
        )
        return None

    logging.info(
        f"Zoekopdracht uitgevoerd: {query_location}"
    )

    results = []

    for location in locations:
        if (query_location in location["Naam"].lower() or query_location in location["Omschrijving"].lower()):
            results.append(location)

    if not results:
        console.print("[yellow]Geen locaties gevonden.[/yellow]")
        return None

    results = results[:10]

    console.print(
        f"\n[green]Top {len(results)} resultaten:[/green]"
    )

    for index, location in enumerate(results, start=1):
        console.print(
            f"[{index}] {location['Naam']}"
        )

    console.print("[0] Terug naar hoofdmenu")

    choices = ["0"]

    for i in range(1, len(results) + 1):
        choices.append(str(i))

    choice = Prompt.ask("Maak een keuze", choices=choices)

    if choice == "0":
        return None

    selected_location = results[int(choice) - 1]

    return selected_location

def location_sub_menu(location):
    while True:
        panel_text = (
            f"Naam: {location['Naam']}\n"
            f"Code: {location['Code']}\n"
            f"Latitude: {location['Lat']}\n"
            f"Longitude: {location['Lon']}\n\n"
            "[1] Actuele metingen opvragen\n"
            "[2] Toevoegen aan favorieten\n"
            "[0] Terug naar hoofdmenu"
        )

        console.print(
            Panel(
                panel_text,
                title=location["Naam"],
                expand=False
            )
        )

        choice = Prompt.ask(
            "Maak een keuze",
            choices=["0", "1", "2"]
        )

        if choice == "1":
            console.print(
                "Nog niet geïmplementeerd"
            )

        elif choice == "2":
            console.print(
                "Nog niet geïmplementeerd"
            )

        elif choice == "0":
            break

def main():
    logging.info("Applicatie Waterwachter gestart.")

    locations = load_locations()

    console.print(Panel(
            "Welkom bij Waterwachter.\n\n"
            "Met deze applicatie kunt u meetlocaties opzoeken, actuele watermetingen raadplegen en favoriete locaties "
            "beheren op basis van gegevens uit de Rijkswaterstaat WaterWebservices API.",
            title="[bold blue]Waterwachter[/bold blue]",
            expand=False,
        )
    )

    console.print()

    while True:
        console.print(Panel(
            "[1] Meetlocatie zoeken\n"
            "[2] Favorieten beheren\n"
            "[3] Zoekgeschiedenis bekijken\n"
            "[0] Afsluiten",
            title="Hoofdmenu",
            expand=False
        ))

        choice = Prompt.ask("Maak een keuze", choices=["0", "1", "2", "3"])

        if choice == "1":
            location = search_location(locations)

            if location:
                location_sub_menu(location)
        elif choice == "2":
            console.print("Favorietenbeheer openen...")
        elif choice == "3":
            console.print("Zoekgeschiedenis tonen...")
        elif choice == "0":
            logging.info("Applicatie afgesloten door gebruiker.")
            console.print("Waterwachter wordt afgesloten. Tot ziens!")
            break

if __name__ == "__main__":
    main()