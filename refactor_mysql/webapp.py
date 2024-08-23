'''webapp'''

import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from markupsafe import escape
from villog import Logger
from config import log_path, o8_json, maria_json, DEFAULT_USERCODE, O8_PACKAGE_CHECK_PATH
from src.slave import date_str, gen_uuid, read_json, read_file
from src.classes.octopus_handle import Octopus

l: Logger = Logger(
    file_path = os.path.join(log_path, f"{date_str()}.log")
)

o8_data: str = read_json(o8_json)
db_data: str = read_json(maria_json)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_data['username']}:{db_data['password']}@{db_data['server']}:{db_data['port']}/{db_data['database']}"
db = SQLAlchemy(app)
app.secret_key = gen_uuid()

octopus: Octopus = Octopus(
    login_data = o8_data,
    logger = l
)

users: list[str] = octopus.get_table(
    table = "USERS"
).return_columns(
    column_names = ["USERCODE", "USERNAME"]
)

class Packages(db.Model):
    '''packages db'''
    id = db.Column(db.Integer, primary_key = True)
    package_no = db.Column(db.String(200), nullable = False)
    is_state = db.Column(db.Boolean, default = False)
    crus = db.Column(db.Integer, nullable = False, default = DEFAULT_USERCODE)
    crdti = db.Column(db.DateTime, default = datetime.now)
    o8_state = db.Column(db.Boolean, default = False)
    o8_found = db.Column(db.Boolean, default = False)

    def get_username(self) -> str:
        '''get username'''
        for user in users:
            if user[0] == self.crus:
                return user[1]
        return "Ismeretlen felhasználó"

    def check_octopus(self) -> None:
        '''check octopus'''
        l.log(f"Checking package {self.package_no} in Octopus")
        query: str = read_file(O8_PACKAGE_CHECK_PATH)
        result: list[str] = octopus.custom_query_only_values(
            query,
            [self.package_no]
        )
        if result:
            self.o8_state = True
            if result[0][0]:
                self.o8_found = True
                l.log(f"Package {self.package_no} found in Octopus")
            else:
                l.log(f"Package {self.package_no} not found in Octopus")
            db.session.commit()

    def get_o8_state(self) -> str:
        '''get o8 state'''
        if self.o8_state:
            if self.o8_found:
                return "Megtalálva"
            return "Nem található"
        return "Nem ellenőrzött"

    def __repr__(self) -> str:
        return f"<Package {self.package_no}>"

class UserSession(db.Model):
    '''user session db'''
    id = db.Column(db.Integer, primary_key = True)
    session_id = db.Column(db.String(200), nullable = False)
    session_filter = db.Column(db.String(200), nullable = True)
    usercode = db.Column(db.Integer, nullable = False, default = DEFAULT_USERCODE)

    def __repr__(self) -> str:
        return f"<UserSession {self.session_id}>"

@app.route("/", methods = ["GET", "POST"])
def index() -> str:
    '''index page'''

    if "session_id" not in session:
        session["session_id"] = gen_uuid()
        new_session = UserSession(
            session_id = session["session_id"]
        )
        db.session.add(new_session)
        db.session.commit()
        u_session = new_session
    else:
        u_session = UserSession.query.filter_by(session_id = session["session_id"]).first()
    all_packages = Packages.query.order_by(desc(Packages.id))
    if request.method == "POST":
        package_no = escape(request.form["package_no"])
        user_code = escape(request.form["user_code"])
        if package_no:
            if package_no not in [package.package_no for package in all_packages]:
                new_package = Packages(
                    package_no = str(package_no),
                    crus = u_session.usercode
                )
                db.session.add(new_package)
                db.session.commit()
                all_packages = Packages.query.order_by(desc(Packages.id))
        if user_code:
            if int(user_code) in [user[0] for user in users]:
                u_session.usercode = int(user_code)
                db.session.commit()
    packages_today = []
    for package in all_packages:
        if package.crdti.date() == datetime.now().date():
            packages_today.append(package)
    return render_template(
        "index.html",
        session = u_session,
        packages = packages_today
    )

@app.route("/o8_check/", methods = ["GET", "POST"])
def check() -> str:
    '''check packages'''
    all_packages = Packages.query.all()
    l.log("Fetching checkable packages")
    for package in all_packages:
        if not package.o8_state:
            package.check_octopus()
    return redirect(
        "/"
    )

def run() -> None:
    '''starts the webapp'''
    l.log("Flask webapp started")
    app.app_context().push()
    db.create_all()
    app.run(
        host = "0.0.0.0",
        debug = True,
        port = 8000
    )
    octopus.close()
    l.log("Flask webapp stopped")

if __name__ == "__main__":
    run()
