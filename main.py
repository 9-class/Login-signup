from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "mysecretkey"

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# define the user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

# define the routes
@app.route('/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}!"
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return "Invalid login credentials"
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect('/')
    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
