from array import array
from ast import For
import sqlite3
import pygal
from pygal.style import Style
from flask import Flask, flash, redirect, session, url_for, render_template, request
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
app.config['SECRET_KEY'] = 'asd'
Session(app)


custom_style = Style(
  background='transparent',
  transition='400ms ease-in',
  legend_font_size=30,
  tooltip_font_size=30,
  major_label_font_size=30,
  label_font_size=30,
  title_font_size=30,
  font_family='arial')



def get_db_connection():
    conn = sqlite3.connect('bancoDados.db')
    """ conn.row_factory = sqlite3.Row """
    return conn


@app.route('/base')#?deletar essa rota, é inútil?
def base():
    return render_template("base.html")


@app.route('/home')
def home():
    chart = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style)
    chart.title='Média de temperatura semanal'
    chart.add('Horta 1', [22, 20, 21])
    chart.add('Horta 2', [19, 20, 18])
    chart.add('Plantação 1', [17, 12, 15])
    chart.add('Plantação 2', [24, 22, 21])
    
    
    chart = chart.render_data_uri()
    if "id_user" in session:
        return render_template("index.html", chart = chart, chart2=chart)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")




# --- páginas de usuário: login, cadastro e user ---

# cadastro de usuario
@app.route('/cadastro', methods=["POST"])
def cadUser():
    login = request.form.get("login")
    password = request.form.get("password")
    password_repet = request.form.get("password_repet")
    conn = get_db_connection()


    try:
        conn.execute('SELECT * FROM users WHERE login=?', (login))
        flash('Login já existente, tente outro', 'ERRO! ')
        return render_template('cadastro.html')
    except:
        if (password == password_repet):
            name = request.form.get("name")
            email = request.form.get("email")
            contact = request.form.get("contact")
            role = request.form.get("role")
            if (role=="USER" or role=="ADMIN"):
                conn.execute('INSERT INTO users (email, contact, login, name, password, role) VALUES (?, ?, ?, ?, ?, ?)',(email, contact, login, name, password, role))
                conn.commit()
                conn.close()
                return redirect(url_for('home'))
            else:
                flash ('Por favor atualize a página e tente novamente', 'ERRO! ')
        else:
            flash('Senhas não batem!', 'ERRO! ')
            return render_template('cadastro.html')

@app.route('/cadastro', methods=["GET"])
def getCadUser():
    if "id_user" in session:
        conn = get_db_connection()
        id_user = session["id_user"]
        print (id_user)
        role = conn.execute('SELECT role FROM users WHERE id_user=?', (id_user,)).fetchall()
        role = role[0][0]
        if role == "ADMIN":
            return render_template("cadastro.html" )
        else:
            flash('Usuario sem privilégio de cadastrar','PERMISSÃO NEGADA! ')
            return redirect("home") 
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login") 


# Login de Usuário
@app.route('/login', methods=["POST"])
def postLogUser():
    login = request.form.get("login")
    senha = request.form.get("senha")
    conn = get_db_connection()
    
    try:
        senha_user =  conn.execute('SELECT password FROM users WHERE login= ? ',(login,)).fetchall()
        if (senha == senha_user[0][0]):
            if "id_user" in session:
                session.pop("id_user", None)
                session.pop("nome_user", None)
            user = conn.execute('SELECT id_user, name FROM users WHERE login=?', (login,)).fetchall()
            session["id_user"] = user[0][0]
            session["name_user"] = user[0][1]
            conn.close
            return redirect('user')
        else:
            flash('Senha incorreta tente outra!', 'ERRO! ')
            conn.close
            return redirect('login')
    except:
        flash('Usuário não existente!', 'ERRO! ')
        conn.close
        return redirect('login')

@app.route('/login', methods=["GET"])
def getLogUser():
    if "id_user" in session:
        name_user = session["name_user"]
        flash('Você já está logado no usuário '+ name_user +' se continuar será deslogado!', 'USUARIO JÁ LOGADO! ')
    return render_template("login.html")


# página de usuário
@app.route('/user', methods=["POST"])
def postUser():
    return

@app.route('/user', methods=["GET"])
def getUser():
    if "id_user" in session:
        id_user = session["id_user"]
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        user = conn.execute('SELECT * FROM users WHERE id_user=?', (id_user,)).fetchall()
        conn.close
        return render_template("user.html", user=user)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")


# página de logout
@app.route('/logout')
def logout():
    if "id_user" in session:
        session.pop("id_user", None)
        session.pop("nome_user", None)
        return redirect("login")
    else:
        return redirect("login")


# --- páginas de cadastro ---

# cadastro de ambientes
@app.route('/cadastro/ambiente', methods=["POST"])
def cadAmbiente():

    nomeAmbiente = request.form["nomeAmbiente"]
    statusAmbiente = 2

    if request.form["status"] == "ativo":
        statusAmbiente = 1
    else:
        statusAmbiente = 0

    if not nomeAmbiente:
        flash('É obrigatório inserir um nome')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO environment (name, status) VALUES (?, ?)',
                     (nomeAmbiente, statusAmbiente))
        conn.commit()
        conn.close()

    return redirect('/cadastro/ambiente')

@app.route('/cadastro/ambiente', methods=["GET"])
def getAmbiente():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        ambientes = conn.execute('SELECT * FROM environment WHERE status==1').fetchall()
        conn.close()
        return render_template("cadastroAmbientes.html", ambiente=ambientes)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")


# cadastro de instâncias
@app.route('/cadastro/instancias', methods=["POST"])
def cadInstancia():
    nomeInstancia = request.form["nomeInstancia"]
    instanciaNumero = request.form["instanciaNumero"]
    idAmbienteInstancia = request.form["idAmbiente"]

    if request.form["status"] == "ativa":
        statusInstancia = 1
    else:
        statusInstancia = 0

    if not nomeInstancia:
        flash('É obrigatório inserir um nome')
    elif not instanciaNumero:
        flash('É obrigatório definir um número de instância')
    elif not idAmbienteInstancia:
        # talvez esse seja redundante
        flash('É obrigatório definir um id de ambiente')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO instances (name, id_environment_FK, number_instance, status) VALUES (?, ?, ?, ?)',
                     (nomeInstancia, idAmbienteInstancia, instanciaNumero, statusInstancia))
        conn.commit()
        conn.close()

        return redirect('/cadastro/instancias')

@app.route('/cadastro/instancias', methods=["GET"])
def getInstancia():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        ambientes = conn.execute(
            'SELECT * FROM environment WHERE status==1').fetchall()
        instance = conn.execute('SELECT * FROM instances').fetchall()
        conn.close()
        return render_template('cadastroInstancias.html', ambientes=ambientes, instance=instance)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")


# cadastro de recursos
@app.route('/cadastro/recursos', methods=["POST"])
def cadRecurso():
    valorInicial = request.form["vlIniAmb"]
    valorFinal = request.form["vlFinAmb"]

    if valorInicial > valorFinal:
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
            conn.execute('INSERT INTO resources (name, number_resource, val_start, val_end) VALUES (?, ?, ?, ?)',
                         (name, resource_number, valorInicial, valorFinal))
            conn.commit()
            conn.close()

            return redirect('/cadastro/recursos')

@app.route('/cadastro/recursos', methods=["GET"])
def getRecurso():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        resource = conn.execute('SELECT * FROM resources').fetchall()
        return render_template("cadastroRecursos.html", resource=resource)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")


# cadastro de instancia_recursos
@app.route('/cadastro/instancias_recursos', methods=["POST"])
def cadInstanciaRecurso():
    resource_id = request.form["idResourceFK"]
    instance_id = request.form["idInstanceFK"]

    if request.form["status"] == "ativa":
        status = 1
    else:
        status = 0

    if request.form["normal"] == "ativa":
        normal = 1
    else:
        normal = 0

    conn = get_db_connection()
    conn.execute('INSERT INTO instances_resources (status, id_resource_FK, id_instance_FK, normal) VALUES (?, ?, ?, ?)',
                 (status, resource_id, instance_id, normal))
    conn.commit()
    conn.close()

    return redirect('/cadastro/instancias_recursos')

@app.route('/cadastro/instancias_recursos', methods=["GET"])
def getInstanciaRecurso():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        resources = conn.execute('SELECT * FROM resources').fetchall()
        instances = conn.execute(
            'SELECT * FROM instances  WHERE status==1').fetchall()
        instance_resource = conn.execute(
            'SELECT * FROM instances_resources').fetchall()
        conn.close()
        return render_template('cadastroInstanciaRecurso.html', resources=resources, instances=instances, instance_resource=instance_resource)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")

# --------------------------------------------------------------


# visualização de dados cadastrados

@app.route('/verdados')
def verDadosx():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        ambientes = conn.execute('SELECT * FROM environment').fetchall()
        instancias = conn.execute('SELECT * FROM instances').fetchall()
        recursos = conn.execute('SELECT * FROM resources').fetchall()
        instancias_recursos = conn.execute('SELECT * FROM instances_resources').fetchall()
        users = conn.execute('SELECT * FROM users').fetchall()
        leituras = conn.execute('SELECT * FROM readings').fetchall()
        conn.close()
        return render_template('verDados.html', ambientes=ambientes, instancias=instancias, recursos=recursos, instancias_recursos=instancias_recursos, user=users, leituras=leituras)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")

@app.route('/verleituras', methods=["GET"])
def getVerLeituras():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        leituras = conn.execute('SELECT * FROM readings ORDER BY hour_reading DESC LIMIT 50').fetchall()
        return render_template('verLeituras.html', leituras=leituras)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")


if __name__ == "__main__":
    app.run(debug=True)
