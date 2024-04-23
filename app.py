from datetime import date

from flask import Flask
from flask_session import Session
from flask import Flask, url_for, render_template, request, session
from functools import wraps

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient


from src import cli_helper
from src.database import Database

app = Flask(__name__)
app.config.from_object("config")  # get data from config.py
Session(app)

configuration = Configuration(host=app.config["KINDE_ISSUER_URL"])
kinde_api_client_params = {
    "configuration": configuration,
    "domain": app.config["KINDE_ISSUER_URL"],
    "client_id": app.config["CLIENT_ID"],
    "client_secret": app.config["CLIENT_SECRET"],
    "grant_type": app.config["GRANT_TYPE"],
    "callback_url": app.config["KINDE_CALLBACK_URL"],
}
if app.config["GRANT_TYPE"] == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
    kinde_api_client_params["code_verifier"] = app.config["CODE_VERIFIER"]

kinde_client = KindeApiClient(**kinde_api_client_params)
user_clients = {}


def get_authorized_data(kinde_client):
    user = kinde_client.get_user_details()
    return {
        "id": user.get("id"),
        "user_given_name": user.get("given_name"),
        "user_family_name": user.get("family_name"),
        "user_email": user.get("email"),
        "user_picture": user.get("picture"),
    }


@app.route("/")
def index():
    data = {"current_year": date.today().year}
    template = "logged_out.html"
    if session.get("user"):
        kinde_client = user_clients.get(session.get("user"))
        if kinde_client and kinde_client.is_authenticated():
            data.update(get_authorized_data(kinde_client))
            template = "home.html"
    return render_template(template, **data)


@app.route("/api/auth/login")
def login():
    return app.redirect(kinde_client.get_login_url())


@app.route("/api/auth/register")
def register():
    return app.redirect(kinde_client.get_register_url())


@app.route("/api/auth/kinde_callback")
def callback():
    kinde_client.fetch_token(authorization_response=request.url)
    data = {"current_year": date.today().year}
    data.update(get_authorized_data(kinde_client))
    session["user"] = data.get("id")
    user_clients[data.get("id")] = kinde_client
    return app.redirect(url_for("index"))


@app.route("/api/auth/logout")
def logout():
    user_clients[session.get("user")] = None
    session["user"] = None
    return app.redirect(
        kinde_client.logout(redirect_to=app.config["LOGOUT_REDIRECT_URL"])
    )


@app.route("/details")
def get_details():
    template = "logged_out.html"
    if session.get("user"):
        kinde_client = user_clients.get(session.get("user"))
        data = {"current_year": date.today().year}
        data.update(get_authorized_data(kinde_client))
        data["access_token"] = kinde_client.configuration.access_token
        template = "details.html"
    return render_template(template, **data)


@app.route("/helpers")
def get_helper_functions():
    template = "logged_out.html"
    if session.get("user"):
        kinde_client = user_clients.get(session.get("user"))
        data = {"current_year": date.today().year}
        data.update(get_authorized_data(kinde_client))
        data["claim"] = kinde_client.get_claim("iss")
        data["organization"] = kinde_client.get_organization()
        data["user_organizations"] = kinde_client.get_user_organizations()
        template = "helpers.html"
    return render_template(template, **data)


@app.route("/list-courses")
def list_courses():
    template = "logged_out.html"
    data = {"current_year": date.today().year}
    if session.get("user"):
        result = cli_helper.list_all_course_details(Database())
        return f"{result}"
    return render_template(template, **data)


@app.route("/create-course")
def create_course():
    try:
        result = cli_helper.create_course(Database(), "my-course3", 10)
        return f"{result}"
    except Exception as e:
        print(str(e))
