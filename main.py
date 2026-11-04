import requests

def test_catalog():
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

    print(f"Statuscode: {response.status_code}")

    if response.status_code == 200:
        print("API bereikbaar")
    else:
        print(response.text)

def test_locations():
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
    data = response.json()

    for locatie in data["LocatieLijst"][:5]:
        print(f"Naam: {locatie['Naam']}")
        print(f"Code: {locatie['Code']}")
        print("-" * 40)

def main():
    test_locations()

if __name__ == "__main__":
    main()