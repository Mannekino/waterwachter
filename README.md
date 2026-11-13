# Waterwachter

Waterwachter is een command\-line applicatie waarmee gebruikers meetlocaties van Rijkswaterstaat kunnen opzoeken en actuele watermetingen kunnen raadplegen via de WaterWebservices API.

## Functionaliteiten

- Zoeken naar meetlocaties op naam of omschrijving
- Opvragen van actuele waterhoogte\- en debietmetingen
- Opslaan van favoriete meetlocaties
- Beheren van favorieten
- Bijhouden van zoekgeschiedenis
- Logging van gebruikersacties en fouten

## Projectstructuur

main.py

api\_service.py

storage\_service.py

- main.py bevat de gebruikersinterface en menustructuur.
- api\_service.py verzorgt communicatie met de Rijkswaterstaat API.
- storage\_service.py verzorgt opslag van favorieten en zoekgeschiedenis.

## Vereiste packages

pip install requests rich

## Applicatie starten

python main.py

## Auteur

Hans Vos

