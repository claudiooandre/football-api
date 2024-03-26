from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root1234'
app.config['MYSQL_DB'] = 'futebol'

# Função para conectar ao MySQL
def conectar_mysql():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

# Rota para página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = conectar_mysql()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM futebol.users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()  # Fecha o cursor
        connection.close()  #
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Login inválido'
    return render_template('login.html')

# Rota para a página do painel de controle
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
            # Estabelece uma conexão com o banco de dados
        connection = conectar_mysql()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM futebol.atletas')
        atletas = cursor.fetchall()
        print(atletas)
        cursor.close()  # Fecha o cursor
        connection.close()  # Fecha a conexão com o banco de dados
        return render_template('dashboard.html', atletas=atletas)
    return redirect(url_for('login'))

# Rota para fazer logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = '1234'
    app.run(debug=True)
