# Waterwachter

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import logging

console = Console()

logging.basicConfig(
    filename="waterwachter.log",
    level=logging.INFO
)

def show_main_menu():
    menu_text = """
    [1] Meetlocatie zoeken
    [2] Actuele watermetingen bekijken
    [3] Favorieten beheren
    [4] Zoekgeschiedenis bekijken
    [0] Afsluiten
    """

    console.print(
        Panel(menu_text,
            title="Waterwachter",
            subtitle="PGF Eindopdracht",
            expand=False
        )
    )

def search_location():
    print("Zoek locatie")

def show_measurements():
    print("Toon watermeting informatie")

def manage_favorites():
    print("Beheer favorieten")


def show_history():
    print("Toon zoekgeschiedenis")


def handle_user_choice(choice):
    if choice == "1":
        search_location()

    elif choice == "2":
        show_measurements()

    elif choice == "3":
        manage_favorites()

    elif choice == "4":
        show_history()

    elif choice == "0":
        print("Waterwachter wordt afgesloten.")

    else:
        print("Ongeldige keuze.")

def main():
    choice = ""

    console.print(
        Panel(
            "Welkom bij Waterwachter.\n\n"
            "Met deze applicatie kunt u meetlocaties opzoeken, "
            "actuele watermetingen raadplegen en favoriete locaties beheren "
            "op basis van gegevens uit de Rijkswaterstaat WaterWebservices API.",

            title="Waterwachter",
            expand=False,
        )
    )

    console.print()

    while choice != "0":
        show_main_menu()

        console.print()

        choice = Prompt.ask(
            "Maak een keuze",
            choices=["0", "1", "2", "3", "4"]
        )

        handle_user_choice(choice)

if __name__ == "__main__":
    main()