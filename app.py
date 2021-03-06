from flask import Flask, request, render_template, jsonify

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, CollectionInvalid
from mongo import MONGO_CONN_STR
import certifi

ca = certifi.where()
app = Flask(__name__, template_folder="templates")

MONGO_CONNECTION = MongoClient(MONGO_CONN_STR, serverSelectionTimeoutMS=5000, tlsCAFile=ca)

try:
    MONGO_CONNECTION.admin.command('ismaster')
except ConnectionFailure:
    print("Couldn't connect to Mongo")

routes_db = MONGO_CONNECTION["Routes"]


@app.route('/', methods=["GET", "POST"])
def routes():
    try:
        with open("passenger.txt", 'r') as passenger_info:
            data = passenger_info.readlines()

            id_of_passenger = data[0]
            name = data[1]
            balance = data[2]

        if request.method == "POST":
            req = request.form

            print(req)

            data_input = {"kav": req["kav"], "current_stop": req["current_stop"], "exit_stop": req["exit_stop"]}

            route_num = data_input["kav"]
            curr_stop = data_input["current_stop"]
            exit_stop = data_input["exit_stop"]

            try:
                route = routes_db.get_collection(route_num)
            except CollectionInvalid:
                route_err = "no such route"
                return render_template("route.html", errors=route_err)
                print("no such route")
            else:
                # CHANGE HERE
                route.update_one({"Stop name": curr_stop},
                                 {"$inc": {"Passengers": {"passenger_id": id_of_passenger, "exit_stop": exit_stop}}})
    except FileNotFoundError:
        card_info_not_found_err = "no such route"
        return render_template("route.html", errors=card_info_not_found_err)
    else:
        return render_template("route.html", id=id_of_passenger, name=name, bal=balance)

    # try:
    #     with open("passenger.txt", 'r') as f:
    #         data = f.readlines()
    #
    #         id_of_passenger = data[0]
    #         name = data[1]
    #         balance = data[2]
    #
    # except FileNotFoundError:
    #     print("File wasn't found")
    #
    # else:
    #     return render_template("route.html", id=id_of_passenger, name=name, bal=balance)


@app.route('/nahag')
def hey():
    return render_template("nahagos.html")


@app.route('/getstops')
def retrieve_bus_stops():
    if "kav" not in request.args:
        return jsonify([]), 500
    kav = request.args['kav']
    if kav.isdecimal() and kav in routes_db.list_collection_names():
        stops = [s['Stop name'] for s in routes_db[kav].find({"Stop name": {"$exists": True}})]
        return jsonify(stops)
    return jsonify([]), 500


@app.route('/getroutes')
def retrieve_routes():
    route_names = [route for route in routes_db.list_collection_names()]

    return jsonify(route_names)


@app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        req = request.form

        data = req.to_dict()
        new_route_info = {"Route number": data['route_num'],
                          "Current amount of passengers": 0}

        route_number = data.pop('route_num')
        data.pop('submitButton')

        new_route_collection = routes_db[route_number]
        new_route_data = [new_route_info]

        for stop_number, stop_name in data.items():
            new_stop = {"Stop name": stop_name, "Passengers": ""}
            new_route_data.append(new_stop)

        # print(new_route_data)

        db_insertion = new_route_collection.insert_many(new_route_data)

        print(db_insertion)

    return render_template("admin.html")


if __name__ == '__main__':
    app.run(debug=True)
