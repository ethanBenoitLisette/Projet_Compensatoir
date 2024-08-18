import requests

# Remplacez 'YOUR_API_KEY' par votre clé API réelle
api_key = '0b62b88f-f890-4369-be70-4771e2fd8268'
headers = {"Authorization": api_key}

# Remplacez <ID> par l'ID de l'équipe que vous souhaitez récupérer
team_id = 2
url = f"https://api.balldontlie.io/v1/teams/{team_id}"

response = requests.get(url, headers=headers)

# Afficher le code de statut HTTP et le contenu de la réponse pour le débogage
print(f"Code de statut HTTP : {response.status_code}")
print(f"Contenu de la réponse : {response.text}")

if response.status_code == 200:
    data = response.json()
    team = data.get('data', {})

    if team:
        print(f"ID de l'équipe: {team['id']}")
        print(f"Conférence: {team['conference']}")
        print(f"Division: {team['division']}")
        print(f"Ville: {team['city']}")
        print(f"Nom de l'équipe: {team['name']}")
        print(f"Nom complet de l'équipe: {team['full_name']}")
        print(f"Abréviation: {team['abbreviation']}")
    else:
        print("Aucune équipe trouvée.")
else:
    print(f"Erreur HTTP : {response.status_code}")
