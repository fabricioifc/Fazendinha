import sqlite3
from this import s
from flask import Flask, flash, redirect, session, url_for, render_template, request
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = ''
Session(app)

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
    login = request.form.get("login")
    senha = request.form.get("senha")
    senhaRep = request.form.get("senhaRep")
    conn = get_db_connection()

    try:
        conn.execute('SELECT * FROM users WHERE login=$s', (login))
        flash('Login já existente, tente outro', 'ERRO! ') 
        return render_template('cadastro.html')
    except:
        if (senha==senhaRep):
            nomeUsuario = request.form.get("nomeUsuario")
            emailUsuario = request.form.get("emailUsuario")
            contatoUsuario = request.form.get("contatoUsuario")
            conn.execute('INSERT INTO users (email, contact, login, nome, password) VALUES (?, ?, ?, ?, ?)',
                                (emailUsuario, contatoUsuario, login, nomeUsuario, senha))
            conn.commit()
            return redirect(url_for('home'))
            conn.close()
        else:
            flash('Senha ou Login incorretos!', 'ERRO! ') 
            return render_template('cadastro.html')

@app.route('/cadastro', methods=["GET"])
def getCadUser():
    return render_template("cadastro.html")

@app.route('/login', methods=["POST"])
def postLogUser():
    login = request.form.get("login")
    senha = request.form.get("senha")
    conn = get_db_connection()

    try:
        user= conn.execute(f'SELECT senha FROM users WHERE login={login}')
        if (senha==user):
            return redirect(url_for('home'))
    except:
        flash('Usuário não existente!', 'ERRO! ') 
        return redirect('login')
    


    return redirect('/login')

@app.route('/login', methods=["GET"])
def getLogUser():
    return render_template("login.html")

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

    return redirect('/cadastro/ambiente')

@app.route('/cadastro/ambiente', methods=["GET"])
def getAmbiente():
    conn = get_db_connection()
    ambiente = conn.execute('SELECT * FROM ambientes').fetchall()
    return render_template("cadastroAmbientes.html", ambiente=ambiente)


# cadastro de instâncias
@app.route('/cadastro/instancias', methods=["POST"])
def cadInstancia():
    nomeInstancia = request.form["nomeInstancia"]
    instanciaNumero = request.form["instanciaNumero"]
    idAmbienteInstancia = request.form["idAmbiente"]

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

        return redirect('/cadastro/instancias')

@app.route('/cadastro/instancias', methods=["GET"])
def getInstancia():
    conn = get_db_connection()
    ambientes = conn.execute('SELECT * FROM ambientes WHERE status==1').fetchall()
    instance = conn.execute('SELECT * FROM instances').fetchall()
    conn.close()
    return render_template('cadastroInstancias.html', ambientes=ambientes, instance=instance)




# cadastro de recursos
@app.route('/cadastro/recursos', methods=["POST"])
def cadRecurso():
    valorInicial = request.form["vlIniAmb"]
    valorFinal = request.form["vlFinAmb"]

    if valorInicial>valorFinal:
        return render_template("cadastroRecursos.html", aviso="O valor final deve ser maior que o inicial. Tente novamente.")
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

            return redirect('/cadastro/recursos')

@app.route('/cadastro/recursos', methods=["GET"])
def getRecurso():
    conn = get_db_connection()
    resource = conn.execute('SELECT * FROM resources').fetchall()  
    return render_template("cadastroRecursos.html", resource=resource)

# cadastro de instancia_recursos
@app.route('/cadastro/instancias_recursos', methods=["POST"])
def cadInstanciaRecurso():
    resource_id = request.form["idResourceFK"]
    instance_id = request.form["idInstanceFK"]

    if request.form["status"]=="ativa":
        status=1
    else:
        status=0

    if request.form["normal"]=="ativa":
        normal=1
    else:
        normal=0

    conn = get_db_connection()
    conn.execute('INSERT INTO instance_resource (status, resource_id, instance_id, normal) VALUES (?, ?, ?, ?)', (status, resource_id, instance_id, normal))
    conn.commit()
    conn.close()

    return redirect('/cadastro/instancias_recursos')

@app.route('/cadastro/instancias_recursos', methods=["GET"])
def getInstanciaRecurso():

    conn = get_db_connection()
    resources = conn.execute('SELECT * FROM resources').fetchall()
    instances = conn.execute('SELECT * FROM instances  WHERE status==1').fetchall()  
    instance_resource = conn.execute('SELECT * FROM instance_resource').fetchall()  
    conn.close()
    return render_template('cadastroInstanciaRecurso.html', resources=resources, instances=instances, instance_resource=instance_resource )

    #return render_template("cadastroRecursos.html")

# --------------------------------------------------------------


# visualização de dados cadastrados

@app.route('/verdados')
def verDadosx():
    conn = get_db_connection()
    ambientes = conn.execute('SELECT * FROM ambientes').fetchall()
    instancias = conn.execute('SELECT * FROM instances').fetchall()
    recursos = conn.execute('SELECT * FROM resources').fetchall()
    instancias_recursos = conn.execute('SELECT * FROM instance_resource').fetchall()
    conn.close()
    return render_template('verDados.html', ambientes=ambientes, instancias=instancias, recursos=recursos, instancias_recursos=instancias_recursos)



if __name__ == "__main__":
    app.run(debug=True)
