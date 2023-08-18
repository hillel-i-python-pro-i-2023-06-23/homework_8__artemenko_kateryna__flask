from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.services.generate_users import generate_users

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route('/get-content')
def read_file():
    return


@app.route("/generate-users")
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


if __name__ == '__main__':
    app.run()
