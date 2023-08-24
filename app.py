from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.services.generate_users import generate_users
from application.services.get_requests import get_astronaut
from application.services.read_csv import read_csv_file
from application.services.read_file import read_file

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/get-content/")
def get_content():
    text = read_file()
    return text


@app.route("/generate-users/")
@use_args({"count": fields.Int(missing=100)}, location="query")
def show_users(args):
    count = args["count"]
    users = generate_users(count=count)
    users_formatted = []
    for user in users:
        user_formatted = f"<li><b>{user.name}</b> - <span>{user.email}</span>"
        users_formatted.append(user_formatted)
    _temp = "\n".join(users_formatted)
    return f"<ol>{_temp}</ol>"


@app.route("/space/")
def space():
    numbers_astronauts = get_astronaut()
    return f"Currently <b>{numbers_astronauts}</b> astronauts."


@app.route("/mean/")
def mean():
    height, weight = read_csv_file()
    return f"Average height of people: <b>{height}</b> sm<br>Average weight of people: <b>{weight}</b> kg"


if __name__ == '__main__':
    app.run()
