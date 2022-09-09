#run flask on port 5000
import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'TEST123'

@app.route('/')
def index():
    return 'it works'

#get db connection SQLit3 function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#show all posts
@app.route('/posts')
def posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('posts.html', posts=posts)

#show single post
@app.route('/posts/<int:id>')
def post(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('posts.html', post=post)

#create a user table on DB
@app.route('/create')
def create():
    conn = get_db_connection()
    conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)')
    conn.close()
    return 'Table created'

#insert a user on DB
@app.route('/insert')
def insert():
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin'))
    conn.commit()
    conn.close()
    return 'User inserted'


#insert user input to DB
@app.route('/insert/<username>/<password>')
def insert_user(username, password):
    conn = get_db_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    return 'User inserted'

#show all users
@app.route('/users')
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('users.html', users=users)


#show single user
@app.route('/users/<int:id>')
def user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('users.html', user=user)

#edit user
@app.route('/edit/<int:id>/<username>/<password>')
def edit(id, username, password):
    conn = get_db_connection()
    conn.execute('UPDATE users SET username = ?, password = ? WHERE id = ?', (username, password, id))
    conn.commit()
    conn.close()
    return 'User updated'

#delete user
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return 'User deleted'

#authenticate user with session
@app.route('/login/<username>/<password>')
def login(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    if user:
        #set session 
        session['user_id'] = user['id']
        return 'User authenticated'
    else:
        return 'User not authenticated'

#logout user
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return 'User logged out'

#redirect user to params page
@app.route('/redirect')
def redirect_to_params():
    return redirect(url_for('params'))

#Say hello to Mehmet
@app.route('/params')
def params():
    name = request.args.get('name')
    return 'Hello ' + name


#show user profile
@app.route('/profile')
def profile():
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        return render_template('profile.html', user=user)
    else:
        return 'User not authenticated'

    









#run flask on port 5000
app.debug = True
app.run(host='0.0.0.0', port=5000)