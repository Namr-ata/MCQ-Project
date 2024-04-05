from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Function to connect to the MySQL database
def get_db_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',  # Enter your MySQL password here
                                 database='data',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# Route for the homepage
@app.route('/')
def cover():
    return render_template('cover.html')

# Route for user registration
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing it in the database
        hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO register (username, email, password) VALUES (%s, %s, %s)', (username, email, hashed_password))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))  # Redirect to login page after successful registration
    
    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM register WHERE email = %s', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            # User authentication successful, redirect to a logged-in page
            return redirect(url_for('index'))
        
        # If authentication fails, redirect back to login page with an error message
        return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

# Route for logged-in page (you need to define this)
@app.route('/')
def index():
    return render_template('index.html') # we can render a template or redirect to a different page here

if __name__ == '__main__':
    app.run(debug=True)
