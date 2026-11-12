"""
Waterwachter

Command-line application for searching measurement locations and retrieving water measurement data from the
Rijkswaterstaat WaterWebservices API.
"""

import logging
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from api_service import load_locations, get_latest_measurements

# Configure application logging according to criteria 1.3
logging.basicConfig(
    filename="waterwachter.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console = Console()

def search_location(locations):
    query_location = Prompt.ask("Zoek op locatie").lower()

    if not query_location.strip():
        console.print("[yellow]Voer een zoekterm in.[/yellow]")
        return None

    logging.info(f"Zoekopdracht uitgevoerd: {query_location}")

    results = []

    for location in locations:
        naam = (location.get("Naam") or "").lower()
        omschrijving = (location.get("Omschrijving") or "").lower()

        if query_location in naam or query_location in omschrijving:
            results.append(location)

    if not results:
        console.print("[yellow]Geen locaties gevonden.[/yellow]")
        return None

    results = results[:10]

    console.print(f"\n[green]Top {len(results)} resultaten:[/green]")

    for index, location in enumerate(results, start=1):
        console.print(f"[{index}] {location['Naam']}")

    console.print("[0] Terug naar hoofdmenu")

    choices = ["0"]

    for i in range(1, len(results) + 1):
        choices.append(str(i))

    choice = Prompt.ask("Maak een keuze", choices=choices)
    console.print()

    if choice == "0":
        return None

    selected_location = results[int(choice) - 1]

    return selected_location

def show_measurements(measurements):
    if not measurements:
        console.print("\n[yellow]Geen waterhoogte- of debietmetingen beschikbaar voor deze locatie.[/yellow]\n")
        return None

    console.print()

    for waarneming in measurements.values():
        grootheid = waarneming["AquoMetadata"]["Grootheid"]["Omschrijving"]
        waarde = waarneming["MetingenLijst"][0]["Meetwaarde"]["Waarde_Numeriek"]
        eenheid = waarneming["AquoMetadata"]["Eenheid"]["Code"]
        tijdstip = waarneming["MetingenLijst"][0]["Tijdstip"]

        console.print(f"{grootheid}")
        console.print("-" * len(grootheid))
        console.print(f"Waarde   : {waarde} {eenheid}")
        console.print(f"Tijdstip : {tijdstip}")
        console.print()

def location_sub_menu(location):
    while True:
        console.print(
            Panel(
                f"Naam: {location['Naam']}\n"
                f"Code: {location['Code']}\n"
                f"Latitude: {location['Lat']}\n"
                f"Longitude: {location['Lon']}\n\n"
                "[1] Actuele metingen opvragen\n"
                "[2] Toevoegen aan favorieten\n"
                "[0] Terug naar hoofdmenu",
                title=location["Naam"],
                expand=False
            )
        )

        choice = Prompt.ask("Maak een keuze", choices=["0", "1", "2"])

        if choice == "1":
            measurements = get_latest_measurements(location["Code"])

            show_measurements(measurements)

        elif choice == "2":
            console.print("Nog niet geïmplementeerd")

        elif choice == "0":
            break

def main():
    logging.info("Applicatie Waterwachter gestart.")

    locations = load_locations()

    if not locations:
        console.print("[red]Kan geen locaties laden van Rijkswaterstaat. Controleer je internetverbinding.[/red]")
        return

    console.print(
        Panel(
            "Welkom bij Waterwachter.\n\n"
            "Met deze applicatie kunt u meetlocaties opzoeken, actuele watermetingen raadplegen en favoriete locaties "
            "beheren op basis van gegevens uit de Rijkswaterstaat WaterWebservices API.",
            title="[bold blue]Waterwachter[/bold blue]",
            width=90,
            expand=False,
        )
    )

    while True:
        console.print()

        console.print(
            Panel(
                "[1] Meetlocatie zoeken\n"
                "[2] Favorieten beheren\n"
                "[3] Zoekgeschiedenis bekijken\n"
                "[0] Afsluiten",
                title="Hoofdmenu",
                expand=False
            )
        )

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