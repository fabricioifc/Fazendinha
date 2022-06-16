import sqlite3
from flask import Flask, flash, redirect, url_for, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

def get_db_connection():
    conn = sqlite3.connect('bancoDados.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/home')
def home():
    return render_template("index.html")

# páginas de usuário: login e cadastro

@app.route('/cadastro', methods=["POST"])
def cadUser():
    nomeUsuario = request.form["nomeUsuario"]
    emailUsuario = request.form["emailUsuario"]
    senha = request.form["senha"]

    return redirect(url_for('home'))

@app.route('/cadastro', methods=["GET"])
def getCadUser():
    return render_template("cadastro.html")

# visualizar dado

@app.route('/verdados')
def verDadosx():
    conn = get_db_connection()
    ambientes = conn.execute('SELECT * FROM ambientes').fetchall()
    conn.close()
    return render_template('verDados.html', ambientes=ambientes)


# páginas de cadastro

# cadastro de ambientes
@app.route('/cadastro/ambiente', methods=["POST"])
def cadAmbiente():

    nomeAmbiente = request.form["nomeAmbiente"]
    statusAmbiente=2

    if request.form["status"]=="ativo":
        statusAmbiente=1
    else:
        statusAmbiente=0
    
    if not nomeAmbiente:
        flash('É obrigatório inserir um nome')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO ambientes (name, status) VALUES (?, ?)',
                        (nomeAmbiente, statusAmbiente))
        conn.commit()
        conn.close()

    return redirect('../verdados')

@app.route('/cadastro/ambiente', methods=["GET"])
def getAmbiente():
    return render_template("cadastroAmbientes.html")


# cadastro de instâncias
@app.route('/cadastro/instancias', methods=["POST"])
def cadInstancia():
    nomeInstancia = request.form["nomeInstancia"]
    instanciaNumero = request.form["instanciaNumero"]
    idAmbienteInstancia = request.form["idAmbienteInstancia"]

    if request.form["status"]=="ativa":
        statusInstancia=1
    else:
        statusInstancia=0

    if not nomeInstancia:
            flash('É obrigatório inserir um nome')
    elif not instanciaNumero:
        flash('É obrigatório definir um número de instância')
    elif not idAmbienteInstancia:
        flash('É obrigatório definir um id de ambiente')#talvez esse seja redundante
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO instances (name, ambiente_id, instance_number, status) VALUES (?, ?, ?, ?)', (nomeInstancia, idAmbienteInstancia, instanciaNumero, statusInstancia))
        conn.commit()
        conn.close()

        return redirect('../home')

@app.route('/cadastro/instancias', methods=["GET"])
def getInstancia():
    
    conn = get_db_connection()
    id_ambiente = conn.execute('SELECT id FROM ambientes').fetchall()
    conn.close()
    return render_template('cadastroInstancias.html', id=id_ambiente)



# cadastro de recursos
@app.route('/cadastro/recursos', methods=["POST"])
def cadRecurso():
    valorInicial = request.form["vlIniAmb"]
    valorFinal = request.form["vlFinAmb"]

    if valorInicial>valorFinal:
        return render_template("cadastroRecursos.html", aviso="O valor final não pode ser maior que o inicial. Tente novamente.")
    else:

        name = request.form['nomeRecurso']
        resource_number = request.form['recursoNumero']

        if not name:
            flash('É obrigatório inserir um nome')
        elif not resource_number:
            flash('É obrigatório definir um número de recurso')
        elif not valorInicial:
            flash('É obrigatório definir um valor inicial')
        elif not valorFinal:
            flash('É obrigatório definir um valor final')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO resources (name, resource_number, vlini, vlfim) VALUES (?, ?, ?, ?)', (name, resource_number, valorInicial, valorFinal))
            conn.commit()
            conn.close()

            return redirect('../home')

@app.route('/cadastro/recursos', methods=["GET"])
def getRecurso():
    return render_template("cadastroRecursos.html")

# cadastro de instancia_recursos
@app.route('/cadastro/instancias_recursos', methods=["POST"])
def cadInstanciaRecurso():
    resource_id = request.form["resource_id"]
    instance_id = request.form["instance_id"]

    if request.form["status"]=="ativa":
        status=1
    else:
        status=0

    if request.form["normal"]=="ativa":
        normal=1
    else:
        normal=0

    if not resource_id:
        flash('É obrigatório inserir um nome')
    elif not instance_id:
        flash('É obrigatório definir um número de recurso')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO instance_resource (status, resource_id, instance_id, normal) VALUES (?, ?, ?, ?)', (status, resource_id, instance_id, normal))
        conn.commit()
        conn.close()

        return redirect('../home')

@app.route('/cadastro/instancias_recursos', methods=["GET"])
def getInstanciaRecurso():

    conn = get_db_connection()
    id_ambiente = conn.execute('SELECT id FROM ambientes').fetchall()
    id_instancia = conn.execute('SELECT id FROM instances').fetchall()    
    conn.close()
    return render_template('cadastroInstanciasRecursos.html', id_ambiente=id_ambiente, id_instancia=id_instancia )

    #return render_template("cadastroRecursos.html")

# --------------------------------------------------------------


# visualização de dados cadastrados





if __name__ == "__main__":
    app.run(debug=True)
