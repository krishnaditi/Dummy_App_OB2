from flask import Flask, render_template, request, redirect, url_for, session, flash 
from models import db, User, Admin, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aditi.db'
app.secret_key = 'your_secret_key_here'  # Add a secret key for sessions

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
        flash('Registration successful! Please login.', 'success')
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
            session['admin_id'] = admin.id
            flash('Logged in as admin!', 'success')
            return redirect(url_for("admin_dashboard"))
        elif user and user.status == "active":
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for("user_dashboard"))
        else:
            flash('Invalid email or password.', 'error')
    return render_template("login.html")

@app.route("/admin_dashboard", methods=["GET", "POST"])
def admin_dashboard():
    search = request.args.get('search', '')
    if search:
        users = User.query.filter(User.full_name.contains(search)).all()
    else:
        users = User.query.all()
    return render_template("admin_dashboard.html", users=users, search=search)

@app.route("/logout")
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route("/approve_user/<int:author_id>")
def approve_user(author_id):
    user = User.query.get(author_id)
    if user:
        user.status = "active"
        db.session.commit()
        flash('User approved!', 'success')
    return redirect(url_for("admin_dashboard"))

@app.route("/reject_user/<int:author_id>")
def reject_user(author_id):
    user = User.query.get(author_id)
    if user:
        user.status = "inactive"
        db.session.commit()
        flash('User rejected!', 'success')
    return redirect(url_for("admin_dashboard"))

@app.route("/search", methods=["GET","POST"])
def search():
    query = request.form.get("query", "")
    results = User.query.filter(User.full_name.contains(query)).all()
    return render_template("admin_dashboard.html", users=results)

@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = Post(title=title, content=content, author_id=user_id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for("user_dashboard"))
    return render_template("create_post.html")

@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    post = Post.query.get_or_404(post_id)
    if post.author_id != user_id:
        return redirect(url_for('user_dashboard'))  # Not authorized
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for("user_dashboard"))
    return render_template("edit_post.html", post=post)

@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    post = Post.query.get_or_404(post_id)
    if post.author_id != user_id:
        return redirect(url_for('user_dashboard'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for("user_dashboard"))

@app.route("/close_post/<int:post_id>")
def close_post(post_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    post = Post.query.get_or_404(post_id)
    if post.author_id != user_id:
        return redirect(url_for('user_dashboard'))
    post.status = 'closed'
    db.session.commit()
    flash('Post closed successfully!', 'success')
    return redirect(url_for("user_dashboard"))

with app.app_context():
    create_admin()
    db.create_all()
    

if __name__ == "__main__":
    app.run()
