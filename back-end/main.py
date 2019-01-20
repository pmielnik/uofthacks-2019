import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import requests
import os

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import datetime

import samples.Shared.config as cfg

app = Flask(__name__)
CORS(app)

#print("connecting to database.....")

HOST ='https://greenicle.documents.azure.com:443/'
MASTER_KEY = os.environ.get('DATABASE_MASTER_KEY')
DATABASE_ID = 'greenicle'
CARS_COLLECTION_ID = 'cars'
USERS_COLLECTION_ID = 'users'

database_link = 'dbs/' + DATABASE_ID
cars_collection_link = database_link + '/colls/' + CARS_COLLECTION_ID
users_collection_link = database_link + '/colls/' + USERS_COLLECTION_ID

db_client=cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY} )

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id=os.environ.get('CLIENT_ID'),
    client_secret=os.environ.get('CLIENT_SECRET'),
    redirect_uri=os.environ.get('REDIRECT_URI'),
    scope=['read_vehicle_info', 'read_odometer', 'read_location', 'read_vin'],
    test_mode=True
)

# Bing search key
subscription_key = os.environ.get('BING_SUBSCRIPTION_KEY')
assert subscription_key
bingSearchUrl = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

# @app.route('/newuser', methods=['POST'])    # may need to change to args.get?
# def newuser():
#    #username = request.form.get('username')
#    #password = request.form.get('password')
#    #vehicleId = request.form.get('vehicleId') #from smartcar?

#    userData=createUserData(username,password,vehicleId)
#    db_client.CreateItem(users_collection_link, userData)

#     #add user info to database

@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)

    # TODO: insert vehicleId to database here

    return '', 200


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()
    print(info)

    return jsonify(info)

@app.route('/odometer', methods=['GET'])
def odometer():
    # access our global variable to retrieve our access tokens
    global access

    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()

    return jsonify(odometer)

@app.route('/location', methods=['GET'])
def location():
    global access

    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    location = vehicle.location()

    return jsonify(location)

@app.route('/co2emission', methods=['GET'])
def co2emission():
    global access

    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']
    info = vehicle.info()
    make = info['make']
    model = info['model']
    year = info['year']
    carId = str(year) + " " + make + " " + str(model)

    mpg = getMPG(carId)
    emission = (odometer/mpg*8887)/(1000000.0)

    return jsonify(CO2emission = emission)

@app.route('/treestoplant', methods=['GET'])
def treestoplant():
    global access
    
    year = 2018
    make = "Audi"
    model = "A4"

    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']
    info = vehicle.info()
    make = info['make']
    model = info['model']
    year = info['year']
    carId = str(year) + " " + make + " " + str(model)

    mpg = getMPG(carId)
    emission = (odometer/mpg*8887)/(1000000.0)
    trees = emission * 0.2

    return jsonify(TreesToPlant = trees)

@app.route('/lightbulbs', methods=['GET'])
def lightbulbs():
    global access
    
    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']
    info = vehicle.info()
    make = info['make']
    model = info['model']
    year = info['year']
    carId = str(year) + " " + make + " " + str(model)

    mpg = getMPG(carId)
    emission = (odometer/mpg*8887)/(1000000.0)
    lightbulbs = emission * 63

    return jsonify(LightBulbHours = lightbulbs)

@app.route('/get-image', methods=['GET'])
def getimage():
    carModel = request.args.get('carModel')

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": carModel}                               # the cursed search engine: , "license": "public", "imageType": "photo"}
    response = requests.get(bingSearchUrl, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    image = search_results["value"][0]["thumbnailUrl"]

    return jsonify(imageURL = image)


def resaleValue(mileage, price):
    resale = 0.0

    if mileage <= 20000:
        resale=0.95*price

    elif mileage > 200000 and mileage <= 30000:
        resale=0.8*price

    elif mileage > 30000 and mileage <= 40000: 
        resale=0.75*price

    elif mileage > 40000 and mileage <= 50000:
        resale=0.7*price

    elif mileage > 50000 and mileage <= 80000:
        resale=0.6*price

    elif mileage > 80000:
        resale=0.4*price

    return resale


@app.route('/price', methods=['GET'])
def price():
    global access

    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']
    info = vehicle.info()
    make = info['make']
    model = info['model']
    year = info['year']
    carId = str(year) + " " + make + " " + str(model)

    return jsonify(price = resaleValue(odometer, getPrice(carId)))

# odometer update every 24hrs
# location update every 5mins

def createUserData(username,password,vehicleid):
    data={
        'id' : username,
        'password' : password,
        'cars' : [
            {'vehicleid' : vehicleid}
        ]
    }
    return data

def getMPG(carid):
    cars={
        '2018 AUDI A4' :'27.8',
        '2017 AUDI A8' : '22.0',
        '2017 AUDI Q5' : '21.5',
        '2017 BMW 3 SERIES' : '27.4',
        '2017 BMW X5' : '20.5',
        '2018 BMW I3' : '117.7',
        '2018 BUICK VERANO' : '24.0',
        '2017 BUICK LACROSSE' : '24.0',
        '2018 BUICK ENCLAVE' : '17.5',
        '2018 CADILLAC ATS' : '23.0',
        '2017 CADILLAC CTS' : '19.7',
        '2018 CADILLAC ESCALADE' : '17.0',
        '2018 CHEVROLET TRAVERSE' : '17.5',
        '2018 CHEVROLET VOLT' : '106.0',
        '2017 CHEVROLET EQUINOX' : '22.3',
        '2018 CHRYSLER PACIFICA' : '22.0',
        '2017 CHRYSLER 300' : '23.0',
        '2015 DODGE JOURNEY' : '23.0',
        '2017 DODGE CHALLENGER' : '18.0',
        '2016 DODGE CHARGER' : '22.0',
        '2017 GMC ACADIA' : '20.3',
        '2018 GMC YUKON' : '17.9',
        '2018 GMC SIERRA' : '22.0',
        '2018 JEEP WRANGLER' : '19.0',
        '2016 JEEP CHEROKEE' : '22.0',
        '2017 JEEP COMPASS' : '22.0',
        '2017 LEXUS RX ' : '25.0',
        '2018 LEXUS ES' : '24.0',
        '2017 LEXUS IS' : '23.0',
        '2018 RAM 2500' : '15.0',
        '2017 RAM 1500' : '14.5',
        '2019 RAM 3500' : '14.6',
        '2017 TESLA MODEL X' : '89.0',
        '2018 TESLA MODEL 3' : '126.0',
        '2016 TESLA MODEL S' : '99.0',
        '2018 VOLKSWAGEN GOLF' : '33.0',
        '2017 VOLKSWAGEN BEETLE' : '28.0',
        '2018 VOLKSWAGEN TIGUAN' : '22.0'
    }
    return (float)(cars[carid])

def getPrice(carid):
    cars={
        '2018 AUDI A4' : 40000,
        '2017 AUDI A8' : 58800,
        '2017 AUDI Q5' : 43800,
        '2017 BMW 3 SERIES' : 41200,
        '2017 BMW X5' : 70000,
        '2018 BMW I3' : 50000,
        '2018 BUICK VERANO' : 21000,
        '2017 BUICK LACROSSE' : 30000,
        '2018 BUICK ENCLAVE' : 40000,
        '2018 CADILLAC ATS' : 40000,
        '2017 CADILLAC CTS' : 46000,
        '2018 CADILLAC ESCALADE' : 75000,
        '2018 CHEVROLET TRAVERSE' : 30000,
        '2018 CHEVROLET VOLT' : 39000,
        '2017 CHEVROLET EQUINOX' : 21000,
        '2018 CHRYSLER PACIFICA' : 36000,
        '2017 CHRYSLER 300' : 42000,
        '2015 DODGE JOURNEY' : 25000,
        '2017 DODGE CHALLENGER' : 48000,
        '2016 DODGE CHARGER' : 50000,
        '2017 GMC ACADIA' : 47000,
        '2018 GMC YUKON' : 58000,
        '2018 GMC SIERRA' : 31000,
        '2018 JEEP WRANGLER' : 28200,
        '2016 JEEP CHEROKEE' : 26000,
        '2017 JEEP COMPASS' : 31000,
        '2017 LEXUS RX ' : 50000,
        '2018 LEXUS ES' : 40000,
        '2017 LEXUS IS' : 41000,
        '2018 RAM 2500' : 34000,
        '2017 RAM 1500' : 27600,
        '2019 RAM 3500' : 37000,
        '2017 TESLA MODEL X' : 80000,
        '2018 TESLA MODEL 3' : 49000,
        '2016 TESLA MODEL S' : 71000,
        '2018 VOLKSWAGEN GOLF' : 27000,
        '2017 VOLKSWAGEN BEETLE' : 30000,
        '2018 VOLKSWAGEN TIGUAN' : 35000
    }
    return (float)(cars[carid])

if __name__ == '__main__':
    app.run(port=8000)
