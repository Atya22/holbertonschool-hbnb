from flask import Flask
from api.api_amenities import api_amenities
from api.api_review import api_review
from api.api_place import api_place
from api.api_country_city import api_country_city
from api.api_user import api_user

app = Flask(__name__)

app.register_blueprint(api_amenities)
app.register_blueprint(api_review)
app.register_blueprint(api_place)
app.register_blueprint(api_country_city)
app.register_blueprint(api_user)

@app.route('/')
def hello():
    return "Hbnb Project!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)