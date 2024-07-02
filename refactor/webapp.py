'''flask webapp'''

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from villog import Logger
from config import db_path, usercode_json
from src.json_handle import JsonManager

path: str = os.path.dirname(__file__)

l = Logger()
l.log("Webapp starting")

usercode_jsh = JsonManager(usercode_json)
if not os.path.exists(usercode_json):
    usercode_jsh.write({"usercode": 1})

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
db = SQLAlchemy(app)
app.secret_key = "Orink160"

class package_db(db.Model):
    '''package_db'''
    id = db.Column(db.Integer, primary_key = True)
    package_no = db.Column(db.String(200), nullable = False)
    crus = db.Column(db.Integer, nullable = False)
    crdti = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self) -> str:
        return f"{self.package_no} - {self.crus} - {self.crdti}"

# index.html
@app.route("/", methods = ["GET", "POST"])
def index() -> str:
    '''index'''
    packages: list = package_db.query.order_by(package_db.id.desc()).all()
    print(packages)
    package_nos = [package.package_no for package in packages]
    print(package_nos)
    if request.method == "POST":
        l.log("POST request")
        package_no: str = request.form.get("package_no")
        if package_no in package_nos or not package_no or package_no == '':
            if not package_no or package_no == '':
                l.log("Package number is empty")
                return render_template("index.html", packages = packages, usercode = usercode_jsh.read()["usercode"], error = "Üres csomagszám!")
            if package_no in package_nos:
                l.log(f"Package ({package_no}) already exist")
                return render_template("index.html", packages = packages, usercode = usercode_jsh.read()["usercode"], error = f"{package_no}: ez a csomag már létezik")
        new_package = package_db(package_no = package_no, crus = usercode_jsh.read()["usercode"])
        db.session.add(new_package)
        db.session.commit()
        l.log(f"Package ({package_no}) added")
        return redirect("/")
    return render_template("index.html", packages = packages, usercode = usercode_jsh.read()["usercode"], error = None)

@app.route("/edit/<int:package_id>", methods = ["GET", "POST"])
def edit(package_id: int):
    '''edit package'''
    if request.method == "POST":
        package = package_db.query.get_or_404(escape(package_id))
        old_package_no: str = package.package_no
        new_package_no: str = request.form.get("package_no")
        if old_package_no != new_package_no:
            packages: list = package_db.query.order_by(package_db.id.desc()).all()
            package_nos = [package.package_no for package in packages]
            if new_package_no not in package_nos or new_package_no or new_package_no != '':
                package.package_no = new_package_no
                db.session.commit()
                l.log(f"Package '{old_package_no}' edited to '{new_package_no}'")
        return redirect("/")
    package = package_db.query.get_or_404(escape(package_id))
    print(package)
    return render_template("edit.html", package = package)


def run() -> None:
    '''run'''
    app.app_context().push()
    db.create_all()
    app.run(debug = True)

if __name__ == "__main__":
    run()
