import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

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
MASTER_KEY = 'G0Mmi0w1guwj0o34EfJnpadk8qf9DFIP2kM3rMbJ5KBP2RX1WBgH3EF2SpRnHvDXSmQsPTQTMCjeVNWR7oWKtg=='
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

@app.route('/newuser', methods=['POST'])
def newuser():
   username = request.form.get('username')
   password = request.form.get('password')
   vehicleId = request.form.get('vehicleId') #from smartcar?

   userData=createUserData(username,password,vehicleId)
   db_client.CreateItem(users_collection_link, userData)

    #add user info to database

@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)

def returnMPG():
    return


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
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

    mpg = getMPG(vehicleId)
    emission = (odometer/mpg*8887)/(1000000.0)

    return jsonify(CO2emission = emission)

@app.route('treestoplant', methods=['GET'])
def treestoplant():
    global access
    
    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']

    mpg = getMPG(vehicleId)
    emission = (odometer/mpg*8887)/(1000000.0)
    trees = emission * 0.2

    return jsonify(TreesToPlant = trees)

@app.route('lightbulbs', methods=['GET'])
def lightbulbs():
    global access
    
    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']

    mpg = getMPG(vehicleId)
    emission = (odometer/mpg*8887)/(1000000.0)
    lightbulbs = emission * 63

    return jsonify(LightBulbHours = lightbulbs)


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
        '2018 Audi A4' :'27.8',
        '2017 Audi A8' : '22.0',
        '2017 Audi Q5' : '21.5',
        '2017 BMW 3 Series' : '27.4',
        '2017 BMW X5' : '20.5',
        '2018 BMW i3' : '117.7',
        '2018 Buick Verano' : '24.0',
        '2017 Buick LaCrosse' : '24.0',
        '2018 Buick Enclave' : '17.5',
        '2018 Cadillac ATS' : '23.0',
        '2017 Cadillac CTS' : '19.7',
        '2018 Cadillac Escalade' : '17.0',
        '2018 Chevrolet Traverse' : '17.5',
        '2018 Chevrolet Volt' : '106.0',
        '2017 Chevrolet Equinox' : '22.3',
        '2018 Chrysler Pacifica' : '22.0',
        '2017 Chrysler 300' : '23.0',
        '2015 Dodge Journey' : '23.0',
        '2017 Dodge Challenger' : '18.0',
        '2016 Dodge Charger' : '22.0',
        '2017 GMC Acadia' : '20.3',
        '2018 GMC Yukon' : '17.9',
        '2018 GMC Sierra' : '22.0',
        '2018 Jeep Wrangler' : '19.0',
        '2016 Jeep Cherokee' : '22.0',
        '2017 Jeep Compass' : '22.0',
        '2017 Lexus RX ' : '25.0',
        '2018 Lexus ES' : '24.0',
        '2017 Lexus IS' : '23.0',
        '2018 RAM 2500' : '15.0',
        '2017 RAM 1500' : '14.5',
        '2019 RAM 3500' : '14.6',
        '2017 Tesla Model X' : '89.0',
        '2018 Tesla Model 3' : '126.0',
        '2016 Tesla Model S' : '99.0',
        '2018 Volkswagen Golf' : '33.0',
        '2017 Volkswagen Beetle' : '28.0',
        '2018 Volkswagen Tiguan' : '22.0'
    }
    return (float)(cars[carid])

if __name__ == '__main__':
    app.run(port=8000)
