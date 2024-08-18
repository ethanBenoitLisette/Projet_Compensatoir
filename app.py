from flask import Flask, render_template, redirect, url_for, request, session
import requests

app = Flask(__name__)
app.secret_key = '0b62b88f-f890-4369-be70-4771e2fd8268'

# Simulation d'une base de données pour les utilisateurs
users_db = {}

# Route pour la page de connexion/inscription
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Traiter le formulaire de connexion
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db and users_db[username] == password:
            session['username'] = username
            return redirect(url_for('players'))
        else:
            return render_template('index.html', error="Nom d'utilisateur ou mot de passe incorrect")
    
    return render_template('index.html')

# Route pour la page d'inscription
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('signup.html', error="Les mots de passe ne correspondent pas.")
        
        if username in users_db:
            return render_template('signup.html', error="Le nom d'utilisateur est déjà pris.")
        
        # Ajouter l'utilisateur à la base de données simulée
        users_db[username] = password
        session['username'] = username
        return redirect(url_for('players'))
    
    return render_template('signup.html')

@app.route('/players')
def players():
    if 'username' in session:
        try:
            response = requests.get('https://www.balldontlie.io/api/v1/players')
            response.raise_for_status()  # Lève une exception pour les statuts HTTP 4xx/5xx
            players_data = response.json().get('data', [])
            return render_template('players.html', players=players_data)
        except requests.exceptions.RequestException as e:
            return f"Erreur lors de la récupération des données : {e}", 500
        except ValueError:
            return "Erreur de décodage JSON.", 500
    return redirect(url_for('login'))


@app.route('/teams')
def teams():
    if 'username' in session:
        response = requests.get('https://www.balldontlie.io/api/v1/teams')
        teams_data = response.json()
        return render_template('teams.html', teams=teams_data)
    return redirect(url_for('login'))

@app.route('/matches')
def matches():
    if 'username' in session:
        response = requests.get('https://www.balldontlie.io/api/v1/games')
        matches_data = response.json()['data']
        return render_template('matches.html', matches=matches_data)
    return redirect(url_for('login'))

@app.route('/player/<int:id>')
def player_detail(id):
    if 'username' in session:
        response = requests.get(f'https://www.balldontlie.io/api/v1/players/{id}')
        player = response.json()
        team_response = requests.get(f'https://www.balldontlie.io/api/v1/teams/{player["team"]["id"]}')
        team = team_response.json()
        return render_template('player_detail.html', player=player, team=team)
    return redirect(url_for('login'))

@app.route('/team/<int:id>')
def team_detail(id):
    if 'username' in session:
        response = requests.get(f'https://www.balldontlie.io/api/v1/teams/{id}')
        team = response.json()
        players_response = requests.get(f'https://www.balldontlie.io/api/v1/players?team_ids[]={id}')
        players = players_response.json()['data']
        return render_template('team_detail.html', team=team, players=players)
    return redirect(url_for('login'))

@app.route('/match/<int:id>')
def match_detail(id):
    if 'username' in session:
        response = requests.get(f'https://www.balldontlie.io/api/v1/games/{id}')
        match = response.json()
        home_team_response = requests.get(f'https://www.balldontlie.io/api/v1/teams/{match["home_team"]["id"]}')
        visitor_team_response = requests.get(f'https://www.balldontlie.io/api/v1/teams/{match["visitor_team"]["id"]}')
        home_team = home_team_response.json()
        visitor_team = visitor_team_response.json()
        return render_template('match_detail.html', match=match, home_team=home_team, visitor_team=visitor_team)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
