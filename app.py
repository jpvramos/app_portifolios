from flask import Flask, render_template, request, json
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
import yaml
from contextlib import closing


mysql = MySQL
app = Flask(__name__)
config = yaml.safe_load(open("config.yml"))

app.config['MYSQL_DATABASE_USER'] = config['databases']['mysql']['username']
app.config['MYSQL_DATABASE_PASSWORD'] = config['databases']['mysql']['password']
app.config['MYSQL_DATABASE_DB'] = config['databases']['mysql']['db']
app.config['MYSQL_DATABASE_HOST'] = config['databases']['mysql']['host']


@app.route('/')
def index():
    return render_template('index.html')


@app.route( str(config['routes']['cadastro']['url']))
def cadastro():
    return render_template('cadastro.html')


@app.route(str(config['routes']['cadastrado']['url']), methods=['POST', 'GET'])
def cadastramentro():
    try:
        _name = request.form['input_name']
        _email = request.form['input_email']
        _password = request.form['input_password']

        # Valida os dados recebidos
        if _name and _email and _password:
            with closing(mysql.connect()) as conn:
                with closing (conn.cursor()) as cursor:
                    _hashed_password = generate_password_hash(_password)
                    cursor.callproc('sp_create_user', (_name, _email, _hashed_password))
                    data = cursor.fetchall()

                    if len(data) is 0:
                        conn.commit()
                        return json.dumps({'message': 'User criado com sucesso!'})
                    else:
                        return json.dumps({{ 'error': str(data[0])}})
        else:
            return json.dumps({'html': '<span>preencha os campos requeridos</span>' })

    except Exception as e:
        return json.dumps({'error' : str(e)})


if __name__ == '__main__':
    app.run()
