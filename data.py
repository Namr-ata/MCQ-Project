from flask import Flask, render_template, request, redirect, url_for,session
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'Namrata'


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
       # hashed_password = generate_password_hash(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO register (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
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

        if user:
            # Assuming 'password' is the column in your database table where passwords are stored
            if password == user['password']: 
                # Login successful
                session['email'] = email  # Store the email in the session
                return redirect(url_for('index'))  # Redirect to the dashboard or some other page
            else:
                # Incorrect password
                return render_template("login.html",error="Invalid password")
        else:
            # User not found
            return render_template("login.html",error="user not found")
    return render_template('login.html')

@app.route('/index')
#@login_required
def index():
    return render_template("index.html")
    
@app.route("/view_answer", methods=["POST"])
def view_answer():
    return render_template("view_answer.html")

@app.route("/submit", methods=["POST"])
def submit():
    return render_template("result.html")


@app.route('/logout', methods=['GET','POST'])
def logout():
   if request.method == 'POST':
       confirm_logout = request.form.get('confirm_logout')
       if confirm_logout=='yes':
           return redirect('/cover')
       else:
           return redirect(url_for('index'))
       return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
