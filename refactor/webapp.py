'''flask webapp'''

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from villog import Logger
from config import db_name, db_path, usercode_json, user_csv_path, ftp_path
from src.json_handle import JsonManager
from src.csv_handle import CsvMaster
from src.ftp_handle import Client as FtpClient
from src.gen_uuid import generate_uuid

# Path for this file
path: str = os.path.dirname(__file__)

# Creating logger
l = Logger()

# JsonManager for usercode.json
usercode_jsh = JsonManager(usercode_json)
if not os.path.exists(usercode_json):
    usercode_jsh.write({"usercode": 1})

# JsonManager for ftp.json
ftp_jsh = JsonManager(ftp_path)
ftp_client = FtpClient(
    hostname = ftp_jsh.read()["hostname"],
    username = ftp_jsh.read()["username"],
    password = ftp_jsh.read()["password"],
    logger = l
)

# Reading users
user_csv = CsvMaster(user_csv_path)

# Creating Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
db = SQLAlchemy(app)
app.secret_key = generate_uuid()

# Package db class
class PackageDb(db.Model):
    '''package_db'''
    id = db.Column(db.Integer, primary_key = True)
    package_no = db.Column(db.String(200), nullable = False)
    is_state = db.Column(db.Integer, nullable = False, default = 0)
    crus = db.Column(db.Integer, nullable = False)
    crdti = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self) -> str:
        return f"{self.package_no} - {self.crus} - {self.crdti}"

# Work states
work_states: list[dict] = [
    {"id": 1, "name": "csomagolás", "selected": True},
    {"id": 2, "name": "elpakolás", "selected": False},
    {"id": 3, "name": "targoncázás", "selected": False},
    {"id": 4, "name": "egyéb munkavégzés", "selected": False}
]

# Select work state
def select_work_state(work_state_id: int):
    '''select work state'''
    global work_states
    for work_state in work_states:
        if work_state["id"] == work_state_id:
            work_state["selected"] = True
        else:
            work_state["selected"] = False

# Get name of the work state
def get_work_state_name(work_state_id: int) -> str:
    '''get work state name'''
    for work_state in work_states:
        if work_state["id"] == work_state_id:
            return work_state["name"]
    return "N/A"

# Get active work state
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
        try:
            usercode: int = int(request.form.get("usercode"))
            if usercode_jsh.read()["usercode"] != usercode:
                usercode_jsh.update({"usercode": usercode})
                l.log(f"Usercode changed to '{usercode}'")
        except ValueError:
            l.log(f"Usercode '{request.form.get("usercode")}' is not a number")
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
        l.log(f"Package '{new_package.id} ({package_no})' added")
        return redirect("/")
    return render_template(
        "index.html",
        packages = packages,
        usercode = usercode_jsh.read()["usercode"],
        work_states = work_states,
        active_work_state = get_active_work_state(),
        error = None
    )

# edit.html
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
                l.log(f"Package '{package.id}' edited from '{old_package_no}' to '{new_package_no}'")
            return redirect("/")
    return render_template(
        "edit.html", 
        package = package
    )

# delete package
@app.route("/delete/<int:package_id>", methods = ["GET", "POST"])
def delete(package_id: int):
    '''delete package'''
    package = PackageDb.query.get_or_404(escape(package_id))
    db.session.delete(package)
    db.session.commit()
    l.log(f"Package '{package.id} ({package.package_no})' deleted")
    return redirect("/")

# change_user.html
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

# change user id
@app.route("/change_user/<int:usercode>", methods = ["GET", "POST"])
def change_user_id(usercode: int):
    '''change user id'''
    usercode_jsh.update({"usercode": usercode})
    l.log(f"Usercode changed to '{usercode}'")
    return redirect("/change_user")

# upload.html
@app.route("/upload/", methods = ["GET", "POST"])
def upload():
    '''upload db'''
    result: str = None
    if request.method == "POST":
        result = ftp_client.upload(
            local_file_path = db_path,
            remote_directory = "csomagolas_refactor",
            remote_filename = db_name
        )
    return render_template(
        "upload.html",
        ftp_status = ftp_client.ping(),
        ftp_info = result
    )

# run
def run() -> None:
    '''run'''
    app.app_context().push()
    db.create_all()
    l.log("Webapp starting")
    app.run(
        host = "0.0.0.0",
        debug = True,
        port = 8000
    )

if __name__ == "__main__":
    run()
