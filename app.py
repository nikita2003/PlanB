from flask import Flask, request, render_template
from pymongo import MongoClient

client = MongoClient(port=27017)
passengers = client.passengers
drivers = client.drivers

app = Flask(__name__, template_folder="templates")


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