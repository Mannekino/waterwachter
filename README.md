# Waterwachter
Waterwachter is een command-line applicatie waarmee gebruikers meetlocaties van Rijkswaterstaat kunnen opzoeken en actuele watermetingen kunnen raadplegen via de WaterWebservices API.

## Functionaliteiten
- Zoeken naar meetlocaties op naam of omschrijving
- Opvragen van actuele waterhoogte- en debietmetingen
- Opslaan en beheren van favoriete meetlocaties (maximaal 10)
- Bijhouden van zoekgeschiedenis (maximaal 10)
- Logging van applicatiegebeurtenissen en fouten naar `waterwachter.log`

## Projectstructuur
- `main.py`: Bevat de gebruikersinterface, menustructuur en invoervalidatie.
- `api_service.py`: Verzorgt de communicatie met de Rijkswaterstaat WaterWebservices API en filtert de meetgegevens.
- `storage_service.py`: Beheert het laden en opslaan van favorieten en zoekgeschiedenis in JSON-bestanden (`favorites.json` en `history.json`).
- `requirements.txt`: Overzicht van de benodigde externe Python-packages (`requests` en `rich`).

## Installatie & vereisten
Vereist **Python 3.10** of hoger. Installeer de benodigde packages vanuit de projectmap:

```bash
pip install -r requirements.txt
```

## Applicatie starten
```bash
python main.py
```

## Testlocaties

Niet alle ruim 2.000 meetlocaties van Rijkswaterstaat leveren waterhoogte- of debietmetingen; sommige stations meten uitsluitend waterkwaliteit. Om de applicatie direct te testen met locaties die actuele waterhoogte- en/of debietwaarden teruggeven, kun je bijvoorbeeld zoeken op:

- `Arnhem, Nederrijn`
- `Rotterdam Kuip`
- `Dieren, IJssel`
- `Botlek Geulhaven`
- `Wijk bij Duurstede, Amsterdam-Rijnkanaal`

## Auteur
Hans Vos