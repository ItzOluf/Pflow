import requests  # Importiere das requests-Modul, um HTTP-Anfragen zu stellen.
import csv
# GraphQL-Abfrage für die zehn bestbewerteten Animes und ihre Hauptcharaktere
query = """
query {  # Beginne die GraphQL-Abfrage
  Page(page: 1, perPage: 100) {  # Hole die erste Seite der Animes mit zehn Animes pro Seite
    media(sort: SCORE_DESC, type: ANIME) {  # Sortiere die Animes nach Bewertung (absteigend) und filtere nur Animes
      title {  # Erhalte die Titel des Animes
        romaji  # Romaji-Titel des Animes (japanische Transkription)
        english  # Englischer Titel des Animes
      }
      averageScore  # Durchschnittliche Bewertung des Animes
      genres  # Liste der Genres des Animes
      siteUrl  # URL zur AniList-Seite des Animes
      characters (role: MAIN) {  # Hole nur Hauptcharaktere
        nodes {  # Alle Charakterdaten, die in der Antwort enthalten sind
          name {  # Name des Charakters
            full  # Vollständiger Name des Charakters
          }
        }
      }
    }
  }
}
"""  # Ende der GraphQL-Abfrage

# Sende die Anfrage an die AniList-API
url = "https://graphql.anilist.co"  # Die URL der AniList GraphQL-API
response = requests.post(url, json={"query": query})  # Sende die POST-Anfrage mit der GraphQL-Abfrage als JSON

# Verarbeite die Antwort
if response.status_code == 200:  # Wenn der HTTP-Statuscode 200 (Erfolg) ist
    data = response.json()  # Parsen der Antwort in JSON-Format
    animes = data["data"]["Page"]["media"]  # Alle Animes in der Antwort extrahieren
    with open('./Data/bestanimes.csv', mode='w', newline='') as file:
    # Erstellen eines CSV-Writers
      writer = csv.writer(file)
    # Gib die grundlegenden Anime-Informationen aus
    for idx, anime in enumerate(animes, start=1):  # Iteriere über die zehn Animes
        title_romaji = anime["title"]["romaji"]  # Hol den Romaji-Titel des Animes
        title_english = anime["title"].get("english", "Kein englischer Titel")  # Hol den englischen Titel (falls vorhanden)
        score = anime["averageScore"]  # Hol die durchschnittliche Bewertung des Animes
        genres = ", ".join(anime["genres"])  # Verbinde alle Genres des Animes zu einer kommagetrennten Liste
        link = anime["siteUrl"]  # Hol den Link zur AniList-Seite des Animes

        # Gib die grundlegenden Anime-Informationen aus
        if (title_romaji== title_english):
          print(f"{idx}: {title_romaji}")
        else:
          print(f"{idx}: {title_romaji} ({title_english})")
        print(f"   Bewertung: {score/10}/10")  # Anime-Bewertung (umgerechnet auf eine Skala von 1 bis 10)
        print(f"   Genres: {genres}")  # Genres des Animes ausgeben
        print(f"   Weitere Infos: {link}")  # Link zur AniList-Seite ausgeben
        
        # Hauptcharaktere ausdrucken
        if "characters" in anime and "nodes" in anime["characters"]:  # Überprüfe, ob Charaktere vorhanden sind
            characters = anime["characters"]["nodes"]  # Hol die Liste der Hauptcharaktere
            print("   Hauptcharaktere:")
            for character in characters:  # Schleife durch alle Hauptcharaktere
                character_name = character["name"]["full"]  # Hol den vollständigen Namen jedes Charakters
                print(f"   - {character_name}")  # Gib den Namen des Charakters aus
        else:
            print("   Keine Hauptcharaktere gefunden.")  # Falls keine Hauptcharaktere gefunden werden, eine Nachricht ausgeben

        print("\n" + "-"*50)  # Trenne die einzelnen Anime-Informationen für bessere Lesbarkeit
else:  # Wenn die Antwort nicht erfolgreich war (Statuscode nicht 200)
    print(f"Fehler: {response.status_code}")  # Fehlercode ausgeben
    print(response.text)  # Gebe die Antwort von der API aus, um den Fehler zu diagnostizieren
