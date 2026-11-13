"""
Waterwachter

Command-line application for searching measurement locations and retrieving water measurement data from the
Rijkswaterstaat WaterWebservices API.
"""

import logging
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from api_service import load_locations, get_latest_measurements
from storage_service import load_file, is_favorite, is_favorites_full, add_favorite, remove_favorite, add_history

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
    add_history(query_location)

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
            if is_favorite(location["Code"]):
                console.print("\n[yellow]Deze locatie staat al in je favorieten.[/yellow]\n")

            elif is_favorites_full():
                proceed = Confirm.ask(
                    "\n[yellow]Maximaal aantal favorieten bereikt. Door deze toe te voegen aan uw favorieten "
                    "wordt de oudste favoriet verwijderd. Doorgaan?[/yellow]",
                    default=False
                )

                if proceed:
                    add_favorite(location)
                    console.print(
                        f"\n[green]'{location['Naam']}' is toegevoegd (oudste favoriet verwijderd).[/green]\n")
                else:
                    console.print("\n[yellow]Toevoegen geannuleerd.[/yellow]\n")

            else:
                add_favorite(location)
                console.print(f"\n[green]'{location['Naam']}' is toegevoegd aan je favorieten.[/green]\n")

        elif choice == "0":
            break

def favorite_sub_menu(favorites):
    for index, favorite in enumerate(favorites, start=1):
        console.print(f"[{index}] {favorite['naam']}")

    console.print("[0] Terug naar hoofdmenu")

    choices = ["0"]

    for i in range(1, len(favorites) + 1):
        choices.append(str(i))

    choice = Prompt.ask("Maak een keuze",choices=choices)

    console.print()

    if choice == "0":
        return None

    favorite = favorites[int(choice) - 1]

    while True:
        console.print(
            Panel(
                f"Naam: {favorite['naam']}\n"
                f"Code: {favorite['code']}\n"
                f"Toegevoegd aan favorieten op: {favorite['toegevoegd_op']}\n\n"
                "[1] Actuele metingen opvragen\n"
                "[2] Verwijderen uit favorieten\n"
                "[0] Terug naar hoofdmenu",
                title=favorite["naam"],
                expand=False
            )
        )

        choice = Prompt.ask("Maak een keuze", choices=["0", "1", "2"])

        if choice == "1":
            measurements = get_latest_measurements(favorite["code"])
            show_measurements(measurements)

        elif choice == "2":
            remove_favorite(favorite["code"])
            console.print(f"\n[green]{favorite['naam']} is verwijderd uit je favorieten.[/green]")
            break

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
            favorites = load_file("favorites")

            if favorites:
                console.print(f"\n[green]U heeft {len(favorites)} favorieten opgeslagen:[/green]")
                favorite_sub_menu(favorites)

            else:
                console.print("\n[yellow]U heeft nog geen favorieten opgeslagen.[/yellow]")

        elif choice == "3":
            search_history = load_file("history")

            if search_history:
                console.print(f"\n[green]Uw laatste {len(search_history)} zoekopdrachten waren:[/green]")

                for index, search_record in enumerate(search_history, start=1):
                    console.print(f"[{index}] {search_record['zoekterm']} ({search_record['toegevoegd_op']})")

            else:
                console.print("\n[yellow]Er is nog geen zoekgeschiedenis aanwezig.[/yellow]")

        elif choice == "0":
            logging.info("Applicatie afgesloten door gebruiker.")
            console.print("Waterwachter wordt afgesloten. Tot ziens!")
            break

if __name__ == "__main__":
    main()