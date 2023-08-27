from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.services.create_table import create_table
from application.services.db_connection import DBConnection
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


@app.route("/phones/create/")
@use_args({"contact_name": fields.Str(required=True), "phone_value": fields.Str(required=True)}, location="query")
def phones__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:contact_name, :phone_value);",
                {"contact_name": args["contact_name"], "phone_value": args["phone_value"]},
            )

    return "OK"


@app.route("/phones/read/<int:phone_ID>")
def phones__read(phone_ID: int):
    with DBConnection() as connection:
        phone = connection.execute(
            "SELECT * FROM phones WHERE (phone_ID=:phone_ID)",
            {
                "phone_ID": phone_ID,
            }
        ).fetchall()

    return f"{phone['phone_ID']} : {phone['contact_name']} - {phone['phone_value']}"


@app.route("/phones/update/<int:phone_ID>")
@use_args({"contact_name": fields.Str(), "phone_value": fields.Str()}, location="query")
def phone__update(
        args,
        phone_ID: int,
):
    with DBConnection() as connection:
        with connection:
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")
            if contact_name is None and phone_value is None:
                return Response(
                    "Need to provide at least one argument",
                    status=400,
                )

            args_for_request = []
            if contact_name is not None:
                args_for_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_for_request.append("phone_value=:phone_value")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE phones " f"SET {args_2} " "WHERE phone_ID=:phone_ID;",
                {
                    "contact_name": contact_name,
                    "phone_value": phone_value,
                    "phone_ID": phone_ID,
                },
            )

    return "OK"


@app.route("/phones/delete/<int:phone_ID>")
def phones__delete(phone_ID):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE * FROM phones WHERE (phone_ID=:phone_ID);",
                {
                    "phone_ID": phone_ID,
                }
            )

    return "OK"


@app.route("/phones/read-all")
def phones__read_all():
    with DBConnection() as connection:
        phones = connection.execute("SELECT * FROM phones;").fetchall()

        return "<br>".join([f"{phone['phone_ID']}: {phone['contact_name']} - "
                            f"{phone['phone_value']}" for phone in phones])


create_table()

if __name__ == '__main__':
    app.run()
