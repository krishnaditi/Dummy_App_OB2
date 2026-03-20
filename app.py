from flask import Flask, render_template, request, render_template, redirect, url_for 
from models import db, User, Admin, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aditi.db'

db.init_app(app)

def create_admin():
    if Admin.query.count() == 0:
        admin = Admin(full_name='Aditi K', email='aditi@gmail.com', password='securepassword@1234')
        db.session.add(admin)
        db.session.commit()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(full_name=full_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email, password=password).first()
        admin = Admin.query.filter_by(email=email, password=password).first()
        if admin:
            return redirect(url_for("admin_dashboard"))
        elif user and user.status == "active":
            return redirect(url_for("user_dashboard"))
    return render_template("login.html")

@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)

@app.route("/user_dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")

@app.route("/approve_user/<int:author_id>")
def approve_user(author_id):
    user = User.query.get(author_id)
    if user:
        user.status == "active"
        db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/reject_user/<int:author_id>")
def reject_user(author_id):
    user = User.query.get(author_id)
    if user:
        user.status == "inactive"
        db.session.commit()
    return redirect(url_for("admin_dashboard"))

with app.app_context():
    create_admin()
    db.create_all()
    

if __name__ == "__main__":
    app.run()
