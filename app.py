from flask import Flask, request, render_template

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from mongo import MONGO_CONN_STR

app = Flask(__name__, template_folder="templates")

MONGO_CONNECTION = MongoClient(MONGO_CONN_STR, serverSelectionTimeoutMS=5000)

try:
    MONGO_CONNECTION.admin.command('ismaster')
except ConnectionFailure:
    print("Couldn't connect to Mongo")


@app.route('/', methods=["GET", "POST"])
def routes():
    if request.method == "POST":
        req = request.form

        print(req)

        data_input = {"kav": req["kav"], "current_stop": req["current_stop"], "exit_stop": req["exit_stop"]}
        print(data_input)

        return render_template("route.html")

    try:
        with open("passenger.txt", 'r') as f:
            data = f.readlines()

            id_of_passenger = data[0]
            name = data[1]
            balance = data[2]

    except FileNotFoundError:
        print("File wasn't found")

    else:
        return render_template("route.html", id=id_of_passenger, name=name, bal=balance)

    return render_template("route.html")


@app.route('/nahag')
def hey():
    return render_template("nahagos.html")


@app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        req = request.form

        data = req.to_dict()
        new_route = {"Route info": {"Route number": data['route_num'],
                                    'Current amount of passengers': 0}}

        data.pop('route_num')
        data.pop('submitButton')

        for stop_number, stop_name in data.items():
            new_stop = {"Stop name": stop_name, "Passangers waiting": 0}
            new_route[stop_number] = new_stop

        print(new_route)

    return render_template("admin.html")


if __name__ == '__main__':
    app.run(debug=True)
