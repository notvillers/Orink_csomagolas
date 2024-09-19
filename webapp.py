'''webapp'''

import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from markupsafe import escape
from villog import Logger
from villog.writexcel import WorkSheet, WorkBook
from config import log_path, o8_json, maria_json, DEFAULT_USERCODE, O8_PACKAGE_CHECK_PATH, WORK_STATES, temp_path
from src.slave import date_str, gen_uuid, read_json, read_file
from src.classes.octopus_handle import Octopus

l: Logger = Logger(
    file_path = os.path.join(log_path, f"{date_str()}.log")
)

o8_data: dict = read_json(o8_json)
db_data: dict = read_json(maria_json)

app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_data['username']}:{db_data['password']}@{db_data['server']}:{db_data['port']}/{db_data['database']}"
db: SQLAlchemy = SQLAlchemy(app)
app.secret_key = gen_uuid()

def get_octopus_connection() -> Octopus:
    '''get octopus connection'''
    return Octopus(
        login_data = o8_data,
        logger = l
    )

def get_users_from_octopus() -> list[str]:
    '''get users from octopus'''
    octopus: Octopus = get_octopus_connection()
    users: list[str] = octopus.get_table(
        table = "USERS",
        USERACTIVE = 1,
        USERTIPUS = 1
    ).return_columns(
        column_names = ["USERCODE", "USERNAME"]
    )
    octopus.close()
    return users

users: list[list] = get_users_from_octopus()

def get_username(usercode: int) -> str:
    '''get username'''
    for user in users:
        if user[0] == usercode:
            return user[1]
    return "Ismeretlen felhasználó"

class Packages(db.Model):
    '''packages db'''
    id: int = db.Column(db.Integer, primary_key = True)
    package_no: str = db.Column(db.String(200), nullable = False)
    is_state: bool = db.Column(db.Boolean, default = False)
    crus: int = db.Column(db.Integer, nullable = False, default = DEFAULT_USERCODE)
    crdti: int = db.Column(db.DateTime, default = datetime.now)
    o8_state: bool = db.Column(db.Boolean, default = False)
    o8_found: bool = db.Column(db.Boolean, default = False)

    def get_username(self) -> str:
        '''get username'''
        for user in users:
            if user[0] == self.crus:
                return user[1]
        return "Ismeretlen felhasználó"

    def check_octopus(self, octopus: Octopus) -> None:
        '''check octopus'''
        query: str = read_file(O8_PACKAGE_CHECK_PATH)
        result: list[str] = octopus.custom_query_only_values(
            query,
            [self.package_no]
        )
        if result:
            self.o8_state = True
            if result[0][0]:
                self.o8_found = True
            db.session.commit()

    def get_o8_state(self) -> str:
        '''get o8 state'''
        if self.o8_state:
            if self.o8_found:
                return "Megtalálva"
            return "Nem található"
        return "Nem ellenőrzött"

    def get_package_no(self) -> str:
        '''get package no'''
        if self.is_state:
            return self.package_no.split("#", maxsplit = 1)[0]
        return self.package_no

    def __repr__(self) -> str:
        return f"<Package {self.package_no}>"

class UserSession(db.Model):
    '''user session db'''
    id: int = db.Column(db.Integer, primary_key = True)
    session_id: str = db.Column(db.String(200), nullable = False)
    session_filter: str = db.Column(db.String(200), nullable = True)
    usercode: int = db.Column(db.Integer, nullable = False, default = DEFAULT_USERCODE)
    ip_address: str = db.Column(db.String(200), nullable = True)
    current_work_state: int = db.Column(db.Integer, nullable = True, default = 1)

    def __repr__(self) -> str:
        return f"<UserSession {self.session_id}>"

class Logs(db.Model):
    '''logs db'''
    id: int = db.Column(db.Integer, primary_key = True)
    log: str = db.Column(db.String(200), nullable = False)
    session_id: str = db.Column(db.String(200), nullable = True)
    log_date: datetime = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self) -> str:
        return f"<Log {self.log}>"

def db_log(content: str, session_id: int = None) -> None:
    '''log to db'''
    new_log: Logs = Logs(
        log = content,
        session_id = session_id
    )
    db.session.add(new_log)
    db.session.commit()

def is_work_state(work_state_int) -> bool:
    '''is work state'''
    for key, _ in WORK_STATES.items():
        if key == work_state_int:
            return True
    return False

@app.route("/", methods = ["GET", "POST"])
def index() -> str:
    '''index page'''
    if "session_id" not in session:
        session["session_id"] = gen_uuid()
        new_session: UserSession = UserSession(
            session_id = session["session_id"],
            ip_address = request.remote_addr if request.remote_addr else "Ismeretlen IP"
        )
        db.session.add(new_session)
        db.session.commit()
        u_session: UserSession = new_session
        db_log(f"New session from {request.remote_addr}", session["session_id"])
    else:
        u_session: UserSession = UserSession.query.filter_by(session_id = session["session_id"]).first()
    all_packages: list[Packages] = Packages.query.order_by(desc(Packages.id))
    if request.method == "POST":
        package_no: str = escape(request.form["package_no"])
        user_code: str = escape(request.form["user_code"])
        if package_no:
            if package_no not in [package.package_no for package in all_packages]:
                new_package: Packages = Packages(
                    package_no = str(package_no),
                    crus = u_session.usercode
                )
                db.session.add(new_package)
                db.session.commit()
                db_log(f"New package added: {package_no}", session["session_id"])
                all_packages: list[Packages] = Packages.query.order_by(desc(Packages.id))
        if user_code and int(user_code) != u_session.usercode:
            if int(user_code) in [user[0] for user in users]:
                u_session.usercode = int(user_code)
                db.session.commit()
                db_log(f"User code changed to: {user_code}", session["session_id"])
    packages_today: list[Packages] = []
    for package in all_packages:
        if package.crdti.date() == datetime.now().date():
            packages_today.append(package)
    return render_template(
        "index.html",
        session = u_session,
        packages = packages_today,
        work_states = WORK_STATES
    )

@app.route("/delete/<int:package_id>")
def delete(package_id: int) -> str:
    '''delete package'''
    package: Packages = Packages.query.filter_by(id = package_id).first()
    if package:
        db_log(f"Deleting request for: {package.package_no}", session["session_id"])
        u_session: UserSession = UserSession.query.filter_by(session_id = session["session_id"]).first()
        return render_template(
            "delete.html",
            session = u_session,
            package = package
        )
    return redirect(
        "/"
    )

@app.route("/delete_confirm/<int:package_id>")
def delete_confirm(package_id: int) -> str:
    '''delete package confirm'''
    package: Packages = Packages.query.filter_by(id = package_id).first()
    u_session: UserSession = UserSession.query.filter_by(session_id = session["session_id"]).first()
    if package:
        if package.crus == u_session.usercode:
            db_log(f"Deleting package: {package.package_no}", session["session_id"])
            db.session.delete(package)
            db.session.commit()
    return redirect(
        "/"
    )

@app.route("/work_state/<int:new_work_state>")
def work_state(new_work_state: int) -> str:
    '''change work state'''
    if is_work_state(new_work_state):
        if session["session_id"]:
            u_session: UserSession = UserSession.query.filter_by(session_id = session["session_id"]).first()
            if u_session:
                old_state: int = u_session.current_work_state
                if old_state != new_work_state:
                    u_session.current_work_state = new_work_state
                    db.session.commit()
                    new_work_state: Packages = Packages(
                        package_no = f"{WORK_STATES[new_work_state]}#{gen_uuid()}",
                        is_state = True,
                        crus = u_session.usercode
                    )
                    db.session.add(new_work_state)
                    db.session.commit()
                    db_log(f"Work state changed from {old_state} to {new_work_state}", session["session_id"])
    return redirect(
        "/"
    )

@app.route("/o8_check/", methods = ["GET", "POST"])
def check() -> str:
    '''check packages'''
    all_packages: list[Packages] = Packages.query.all()
    db_log("Fetching checkable packages")
    if all_packages:
        octopus: Octopus = get_octopus_connection()
        for package in all_packages:
            if not package.o8_state:
                package.check_octopus(octopus = octopus)
        octopus.close()
    return redirect(
        "/"
    )

@app.route("/users/")
def show_users() -> str:
    '''users'''
    if "session_id" not in session:
        session["session_id"] = gen_uuid()
        new_session: UserSession = UserSession(
            session_id = session["session_id"],
            ip_address = request.remote_addr if request.remote_addr else "Ismeretlen IP"
        )
        db.session.add(new_session)
        db.session.commit()
        u_session: UserSession = new_session
        db_log(f"New session from {request.remote_addr}", session["session_id"])
    else:
        u_session: UserSession = UserSession.query.filter_by(session_id = session["session_id"]).first()
    return render_template(
        "users.html",
        session = u_session,
        users = users
    )

@app.route("/switch_user/<int:usercode>")
def switch_user(usercode: int) -> str:
    '''switch user'''
    u_session: UserSession = UserSession.query.filter_by(session_id = session["session_id"]).first()
    if usercode in [user[0] for user in users]:
        if usercode != u_session.usercode:
            u_session.usercode = usercode
            db.session.commit()
            db_log(f"User code changed to: {usercode}", session["session_id"])
    return redirect(
        "/"
    )

def packages_on_date(date: datetime.date) -> list[Packages]:
    '''packages on date'''
    all_packages: list[Packages] = Packages.query.all()
    packages_on_date: list[Packages] = []
    for package in all_packages:
        if package.crdti.date() == date:
            packages_on_date.append(package)
    return packages_on_date

def dates_of_packages() -> list[datetime.date]:
    '''dates of packages'''
    all_packages: list[Packages] = Packages.query.all()
    dates = []
    for package in all_packages:
        if package.crdti.date() not in dates:
            dates.append(package.crdti.date())
    return dates

def all_user_of_packages() -> list[int]:
    '''all user of packages'''
    users: list[int] = []
    for package in Packages.query.all():
        if package.crus not in users:
            users.append(package.crus)
    return users

def all_package_for_user(usercode: int) -> list[Packages]:
    '''all package for user'''
    packages: list[Packages] = []
    for package in Packages.query.all():
        if package.crus == usercode:
            packages.append(package)
    return packages

def users_in_package_list(packages: list[Packages]) -> list[str]:
    '''users in package list'''
    users_in_packages: list[str] = []
    for package in packages:
        if package.crus not in users_in_packages:
            users_in_packages.append(package.crus)
    return users_in_packages

def package_counter_for_user(packages: list[Packages], usercode: int) -> int:
    '''package counter for user'''
    counter: int = 0
    for package in packages:
        if package.crus == usercode and not package.is_state:
            counter += 1
    return counter

def checked_package_counter_for_user(packages: list[Packages], usercode: int) -> int:
    '''checked package counter for user'''
    counter: int = 0
    for package in packages:
        if package.crus == usercode and package.o8_found and not package.is_state:
            counter += 1
    return counter

@app.route("/summary")
def summary() -> None:
    '''summary'''
    sheets: list[WorkSheet] = []
    summary_data_header: list[str] = [
        "Dátum", "Felhasználókód", "Felhasználónév", "Csomagszám", "Talált csomagok"
    ]
    summary_data = []
    dates: list[datetime.date] = dates_of_packages()
    for date in dates:
        pack_on_date: list[Packages] = packages_on_date(date)
        users: list[str] = users_in_package_list(pack_on_date)
        for user in users:
            usercode: int = user
            username: str = get_username(usercode)
            package_counter: int = package_counter_for_user(pack_on_date, usercode)
            found_package_counter: int = checked_package_counter_for_user(pack_on_date, usercode)
            summary_data.append(
                [
                    date,
                    usercode,
                    username,
                    package_counter,
                    found_package_counter
                ]
            )
    sheets.append(
        WorkSheet(
            name = "Összesítő",
            header = summary_data_header,
            data = summary_data
        )
    )
    users: list[int] = all_user_of_packages()
    sheet_header: list[str] = ["Dátum", "Csomagszám", "O8_állapot"]
    for user in users:
        sheet_data: list[list] = []
        packages: list[Packages] = all_package_for_user(user)
        for package in packages:
            sheet_data.append(
                [
                    package.crdti,
                    package.get_package_no(),
                    package.get_o8_state()
                ]
            )
        sheets.append(
            WorkSheet(
                name = get_username(user),
                header = sheet_header,
                data = sheet_data
            )
        )

    summary_workbook: WorkBook = WorkBook(
        name = "Összesítő",
        content = sheets
    )
    xlsx_path: str = summary_workbook.xlsx_create(
        file_path = temp_path,
        file_name = f"{date_str()}_{gen_uuid()}.xlsx"
    )

    return send_file(
        xlsx_path,
        as_attachment = True
    )

def run() -> None:
    '''starts the webapp'''
    l.log("Flask webapp started")
    app.app_context().push()
    db.create_all()
    app.run(
        host = "0.0.0.0",
        debug = True,
        port = 9000
    )
    l.log("Flask webapp stopped")

if __name__ == "__main__":
    run()
