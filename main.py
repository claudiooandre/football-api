from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)

# Config. to database mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root1234'
app.config['MYSQL_DB'] = 'football'

# Function to connect the database mysql
def conectar_mysql():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# Route to index page
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Route to login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = conectar_mysql()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM football.users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close() 
        if user:
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return 'Login invalid'
    return render_template('login.html')

# Route to main page
@app.route('/main')
def main():
    if 'username' in session:
        # Connection to the database
        connection = conectar_mysql()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM football.athletes')
        athletes = cursor.fetchall()
        ###print(athletes)
        cursor.close()
        connection.close() 
        return render_template('main.html', athletes=athletes)
    return redirect(url_for('login'))

# Route to logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.secret_key = '1234'
    app.run(debug=True)
