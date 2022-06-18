from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy

API_key = "b8d7ba7777379b79c5af2ebe9002f4e9"
app = Flask(__name__)
app.config['DEBUG'] = True
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)





@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method =='POST':
        new_city = request.form.get('city')
        if new_city:
            new_city_ob = City(name=new_city)
            db.session.add(new_city_ob)
            db.session.commit()

    cities = City.query.all()
    #url = f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API key}"
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=b8d7ba7777379b79c5af2ebe9002f4e9"
    weather_data = []
    for city in cities:
        r= requests.get(url.format(city.name)).json()   
        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        print(weather)
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

if __name__ == "__main__":
    app.run()

