"""
Manage persistent storage for the Waterwachter application.

This module loads and saves favorites and search history as JSON files
and limits both collections to the ten most recent entries.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

FAVORITES_FILE = Path("favorites.json")
HISTORY_FILE = Path("history.json")
MAX_FAVORITES = 10
MAX_HISTORY = 10

def load_file(file_type):
    if file_type == "favorites":
        file_name = FAVORITES_FILE
    else:
        file_name = HISTORY_FILE

    if not file_name.exists():
        return []

    with file_name.open("r", encoding="utf-8") as file:
        try:
            return json.load(file)

        except json.JSONDecodeError:
            logging.warning(f"{file_name} bevat geen geldige JSON")
            return []

def save_file(content, file_type):
    if file_type == "favorites":
        file_name = FAVORITES_FILE
    else:
        file_name = HISTORY_FILE

    with file_name.open("w", encoding="utf-8") as file:
        json.dump(content, file, indent=4, ensure_ascii=False)

def is_favorite(location_code):
    favorites = load_file("favorites")
    for fav in favorites:
        if fav["code"] == location_code:
            return True
    return False

def is_favorites_full():
    favorites = load_file("favorites")
    return len(favorites) >= MAX_FAVORITES

def add_favorite(location):
    favorites = load_file("favorites")

    # Remove the oldest favorite when the maximum of ten favorites is reached
    if len(favorites) >= MAX_FAVORITES:
        favorites.pop(0)

    new_favorite = {
        "naam": location["Naam"],
        "code": location["Code"],
        "toegevoegd_op": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    favorites.append(new_favorite)
    save_file(favorites, "favorites")
    logging.info(f"Favoriet toegevoegd: {location['Code']}")

def remove_favorite(location_code):
    favorites = load_file("favorites")

    favorites = [
        fav
        for fav in favorites
        if fav["code"] != location_code
    ]

    save_file(favorites, "favorites")

    logging.info(f"Favoriet verwijderd: {location_code}")

def add_history(query_location):
    history = load_file("history")

    # Keep only the ten most recent search queries
    if len(history) >= MAX_HISTORY:
        history.pop(0)

    new_history = {
        "zoekterm": query_location,
        "toegevoegd_op": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(new_history)
    save_file(history, "history")
    logging.info(f"Zoekterm opgeslagen: {query_location}")