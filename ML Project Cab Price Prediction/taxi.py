from flask import Flask, render_template ,request, jsonify
from datetime import datetime
from geopy.distance import geodesic
import pickle
import pymysql as py


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',fare=f"Fare = ${0.00}")



@app.route('/hello')
def hello():
    return 'Hello, World❤️'



@app.route("/model")
def model():
    return render_template('index.html',fare=f"Fare = ${0.00}")



def fare_amount(data):
    with open('fare_price_predict.pkl','rb') as f:
        fare_model = pickle.load(f)
    price = round(fare_model.predict(data)[0],2)
    return price


def calculate_distance(pickup_lat, 
                       pickup_long, 
                       dropoff_lat, 
                       dropoff_long):
    
    
    return geodesic((pickup_lat, pickup_long), 
                    (dropoff_lat, dropoff_long)).miles


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        pickup_datetime = request.form['pickup_datetime']
        pickup_longitude = float(request.form['pickup_longitude'])
        pickup_latitude = float(request.form['pickup_latitude'])
        dropoff_longitude = float(request.form['dropoff_longitude'])
        dropoff_latitude = float(request.form['dropoff_latitude'])
        passenger_count = int(request.form['passenger_count'])
        
        
        pickup_datetime = datetime.strptime(pickup_datetime, '%Y-%m-%dT%H:%M')

        
        year = pickup_datetime.year
        month = pickup_datetime.month
        day = pickup_datetime.day
        hour = pickup_datetime.hour
        minute = pickup_datetime.minute
        second = pickup_datetime.second
        
        distance = calculate_distance(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude)
        
        X =[[pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,passenger_count,distance,year,month,day,hour,minute,second]]
                                      
    
    
    

        conn = py.Connect(user = 'root',host = 'localhost',password = '1401',autocommit = True)
        print('Connection created successfully!!!')

        cur = conn.cursor()

#         cur.execute('create database if not exists taxi_complete_data')
    
        q = f'''insert into taxi_complete_data.all_data values
            ("{pickup_longitude}", 
            "{pickup_latitude}", 
            "{dropoff_longitude}", 
            "{dropoff_latitude}", 
            "{passenger_count}", 
            "{distance}", 
            "{year}", 
            "{month}", 
            "{day}", 
            "{hour}", 
            "{minute}", "{second}")'''.replace('\n',' ')

        cur.execute(q)
        
        print('record inserted successfully!!!')
        
        return render_template('index.html', fare=f"Fare = ${fare_amount(X)*passenger_count}")
        
    
    return render_template('index.html', fare=f"Fare = ${0.00}")
    
        
        
        
if __name__ == '__main__':
    app.run(debug=True)