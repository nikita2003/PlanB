from flask import Flask, request, render_template
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__, template_folder="templates")

MONGO_CONN_STR = "mongodb://Becker2103:nikita03@planb-shard-00-00.0gsad.mongodb.net:27017,planb-shard-00-01.0gsad.mongodb.net:27017,planb-shard-00-02.0gsad.mongodb.net:27017/?ssl=true&replicaSet=atlas-fqu4pa-shard-0&authSource=admin&retryWrites=true&w=majority"
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

        print(req)

        data = req.to_dict()
        new_route = {"RouteNumber": data['route_num']}

        data.pop('route_num')
        data.pop('submitButton')

        for stop in data:
            pass

    return render_template("admin.html")


if __name__ == '__main__':
    app.run(debug=True)
