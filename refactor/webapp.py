'''flask webapp'''

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from villog import Logger
from config import db_path, usercode_json, user_csv_path
from src.json_handle import JsonManager
from src.csv_handle import CsvMaster
from src.gen_uuid import generate_uuid

path: str = os.path.dirname(__file__)

l = Logger()
l.log("Webapp starting")

usercode_jsh = JsonManager(usercode_json)
if not os.path.exists(usercode_json):
    usercode_jsh.write({"usercode": 1})

user_csv = CsvMaster(user_csv_path)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
db = SQLAlchemy(app)
app.secret_key = generate_uuid()

# package db class
class PackageDb(db.Model):
    '''package_db'''
    id = db.Column(db.Integer, primary_key = True)
    package_no = db.Column(db.String(200), nullable = False)
    is_state = db.Column(db.Integer, nullable = False, default = 0)
    crus = db.Column(db.Integer, nullable = False)
    crdti = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self) -> str:
        return f"{self.package_no} - {self.crus} - {self.crdti}"

work_states: list[dict] = [
    {"id": 1, "name": "csomagolás", "selected": True},
    {"id": 2, "name": "elpakolás", "selected": False},
    {"id": 3, "name": "targoncázás", "selected": False},
    {"id": 4, "name": "egyéb munkavégzés", "selected": False}
]

def select_work_state(work_state_id: int):
    '''select work state'''
    global work_states
    for work_state in work_states:
        if work_state["id"] == work_state_id:
            work_state["selected"] = True
        else:
            work_state["selected"] = False

def get_work_state_name(work_state_id: int) -> str:
    '''get work state name'''
    for work_state in work_states:
        if work_state["id"] == work_state_id:
            return work_state["name"]
    return "N/A"

def get_active_work_state() -> int:
    '''get active work state'''
    for work_state in work_states:
        if work_state["selected"]:
            return work_state["id"]
    return 1

# index.html
@app.route("/", methods = ["GET", "POST"])
def index() -> str:
    '''index'''
    packages: list = PackageDb.query.order_by(PackageDb.id.desc()).all()
    package_nos = [package.package_no for package in packages]
    if request.method == "POST":
        is_state: int = 0
        l.log("POST request")
        try:
            usercode: int = int(request.form.get("usercode"))
            if usercode_jsh.read()["usercode"] != usercode:
                usercode_jsh.update({"usercode": usercode})
                l.log(f"Usercode changed to {usercode}")
        except ValueError:
            l.log("Usercode is not a number")
            redirect("/")
        package_no: str = request.form.get("package_no")
        work_state: str = request.form.get("work_state")
        select_work_state(int(work_state))
        if work_state == "1":
            if package_no in package_nos or not package_no or package_no == '':
                if not package_no or package_no == '':
                    l.log("Package number is empty")
                    return render_template(
                        "index.html",
                        packages = packages,
                        usercode = usercode_jsh.read()["usercode"],
                        work_states = work_states,
                        active_work_state = get_active_work_state(),
                        error = "Üres csomagszám!"
                    )
                if package_no in package_nos:
                    l.log(f"Package ({package_no}) already exist")
                    return render_template(
                        "index.html",
                        packages = packages,
                        usercode = usercode_jsh.read()["usercode"],
                        work_states = work_states,
                        active_work_state = get_active_work_state(),
                        error = "A csomagszám már létezik!"
                    )
        else:
            package_no = f"{get_work_state_name(int(work_state))}_{generate_uuid(8)}"
            is_state = work_state
        new_package = PackageDb(package_no = package_no, crus = usercode_jsh.read()["usercode"], is_state = is_state)
        db.session.add(new_package)
        db.session.commit()
        l.log(f"Package ({package_no}) added")
        return redirect("/")
    return render_template(
        "index.html",
        packages = packages,
        usercode = usercode_jsh.read()["usercode"],
        work_states = work_states,
        active_work_state = get_active_work_state(),
        error = None
    )

@app.route("/edit/<int:package_id>", methods = ["GET", "POST"])
def edit(package_id: int):
    '''edit package'''
    package = PackageDb.query.get_or_404(escape(package_id))
    for work_state in work_states:
        if package.package_no.startswith(f"{work_state['name']}_"):
            return redirect("/")
    if request.method == "POST":
        old_package_no: str = package.package_no
        new_package_no: str = request.form.get("package_no")
        if old_package_no != new_package_no:
            packages: list = PackageDb.query.order_by(PackageDb.id.desc()).all()
            package_nos = [package.package_no for package in packages]
            if new_package_no not in package_nos or new_package_no or new_package_no != '':
                package.package_no = new_package_no
                db.session.commit()
                l.log(f"Package '{old_package_no}' edited to '{new_package_no}'")
            return redirect("/")
    package = PackageDb.query.get_or_404(escape(package_id))
    print(package)
    return render_template(
        "edit.html", 
        package = package
    )

@app.route("/delete/<int:package_id>", methods = ["GET", "POST"])
def delete(package_id: int):
    '''delete package'''
    package = PackageDb.query.get_or_404(escape(package_id))
    print("lelelelel")
    print(package.id)
    db.session.delete(package)
    db.session.commit()
    l.log(f"Package '{package.package_no}' deleted")
    return redirect("/")

@app.route("/change_user/", methods = ["GET", "POST"])
def change_user():
    '''change user'''
    if request.method == "POST":
        search: str = request.form.get("user_to_search")
        if search:
            users = user_csv.search_in_line_by_order(search, 1)
        else:
            users = user_csv.order_by_element(1)
    else:
        users = user_csv.order_by_element(1)
    return render_template(
        "change_user.html",
        users = users,
        current_usercode = str(usercode_jsh.read()["usercode"])
    )

@app.route("/change_user/<int:usercode>", methods = ["GET", "POST"])
def change_user_id(usercode: int):
    '''change user id'''
    usercode_jsh.update({"usercode": usercode})
    return redirect("/change_user")


def run() -> None:
    '''run'''
    app.app_context().push()
    db.create_all()
    app.run(debug = True, port=8000)

if __name__ == "__main__":
    run()

# FTP feltöltés
