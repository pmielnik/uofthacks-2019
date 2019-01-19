import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

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
subscription_key = 'cdcce10aafc748929f842db03f1c0390'
assert subscription_key
bingSearchUrl = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

# TODO: determine if this is necessary
#@app.route('/newuser', methods=['POST'])
#def newuser():
#    firstname = request.args.get('firstname')
#    lastname = request.args.get('lastname')
#    username = request.args.get('user')
#    vehicleId = request.args.get('vehicleId')

    # add user info to database

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

    mpg = 1 # TODO: SQL querey to find mpg related to vehicle ID
    emission = odometer/10000 * mpg

    return jsonify(CO2emission = emission)

@app.route('/treestoplant', methods=['GET'])
def treestoplant():
    global access
    
    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']

    mpg = 1 # TODO: SQL querey to find mpg related to vehicle ID
    emission = odometer/10000 * mpg
    trees = emission * 0.2

    return jsonify(TreesToPlant = trees)

@app.route('/lightbulbs', methods=['GET'])
def lightbulbs():
    global access
    
    vehicleId = request.args.get('vehicleId')
    vehicle = smartcar.Vehicle(vehicleId, access['access_token'])
    odometer = vehicle.odometer()['data']

    mpg = 1 # TODO: SQL querey to find mpg related to vehicle ID
    emission = odometer/10000 * mpg
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


# odometer update every 24hrs
# location update every 5mins


if __name__ == '__main__':
    app.run(port=8000)
