from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    character_info = {}
    error_message = None

    if request.method == 'POST':
        character_id = request.form['character_id']
        
        # Request to SWAPI for character data
        response = requests.get(f'https://swapi.py4e.com/api/people/{character_id}')
        
        if response.status_code == 200:
            data = response.json()
            character_info = {
                'name': data['name'],
                'height': data['height'],
                'mass': data['mass'],
                'hair_color': data['hair_color'],
                'eye_color': data['eye_color']
            }

            # Request for Homeworld data
            homeworld_url = data['homeworld']
            homeworld_response = requests.get(homeworld_url)
            if homeworld_response.status_code == 200:
                homeworld_data = homeworld_response.json()
                character_info['homeworld'] = homeworld_data['name']
            else:
                character_info['homeworld'] = 'Unknown'
            
            character_info['films'] = []
            for film_url in data['films']:
                film_response = requests.get(film_url)
                if film_response.status_code == 200:
                    film_data = film_response.json()
                    character_info['films'].append(film_data['title'])

        else:
            error_message = "Character not found or an error occurred."

    return render_template('index.html', character_info=character_info, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)