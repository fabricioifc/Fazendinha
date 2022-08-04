from array import array
from ast import For
import itertools
import sqlite3
from unicodedata import name
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
    conn = get_db_connection()
    """ ---gráfico das leituras de temperatura--- """
    readings_temp = conn.execute("SELECT hour_reading, value, id_instance_FK, name FROM readings INNER JOIN instances WHERE readings.id_instance_FK=instances.id_instance AND number_resource_FK=3303 ORDER BY hour_reading DESC LIMIT 50").fetchall()
    readings_temp.reverse()
    chart_temp = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style, show_x_labels=False)
    chart_temp.title='Média de temperatura'    
    hour_temp = []
    temp = []
    qtd_val = 0
    average_temp = 0
    
    for row in readings_temp:
        hour_temp.append(row[0])
        temp.append(row[1])
        average_temp+=row[1]
        qtd_val+=1
    average_temp/=qtd_val
    average_temp = round(average_temp, 2)
    chart_temp.add(row[3], temp )
    max_temp = int(max(temp)+10)
    min_temp = int(min(temp)-10)
    chart_temp.y_labels = map(int, range(min_temp, max_temp, +5))
    chart_temp.x_labels = hour_temp
    
    """ ---gráfico das leituras de humidade--- """
    readings_humi = conn.execute("SELECT hour_reading, value, id_instance_FK, name FROM readings INNER JOIN instances WHERE readings.id_instance_FK=instances.id_instance AND number_resource_FK=3304 ORDER BY hour_reading DESC LIMIT 50").fetchall()
    readings_humi.reverse()
    chart_humi = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style, show_x_labels=False)
    chart_humi.title='Média de humidade'    
    hour_temp = []
    temp = []
    qtd_val = 0
    average_humi = 0
    
    for row in readings_humi:
        hour_temp.append(row[0])
        temp.append(row[1])
        average_humi+=row[1]
        qtd_val+=1
    average_humi/=qtd_val
    average_humi = round(average_humi, 2)
    chart_humi.add(row[3], temp )
    max_temp = int(max(temp)+10)
    min_temp = int(min(temp)-10)
    chart_humi.y_labels = map(int, range(min_temp, max_temp, +5))
    chart_humi.x_labels = hour_temp

    """ ---tabela da ultima leitura de cada ambiente--- """
    conn.row_factory = sqlite3.Row
    environment_readings = conn.execute("SELECT * FROM environment WHERE status=1").fetchall()
    last_temp = list()
    last_humi = list()
    for environment in environment_readings:
        id_environment = environment['id_environment']
        last_temp.extend(conn.execute("SELECT hour_reading, id_instance_FK, number_resource_FK, value, id_instance, id_environment_FK, id_environment, environment.name FROM readings, instances, environment WHERE readings.number_resource_FK = 3303 AND readings.id_instance_FK = instances.id_instance AND instances.id_environment_FK = environment.id_environment AND environment.id_environment={} ORDER BY hour_reading DESC LIMIT 1".format(id_environment)).fetchall())

        last_humi.extend(conn.execute("SELECT hour_reading, id_instance_FK, number_resource_FK, value, id_instance, id_environment_FK, id_environment, environment.name FROM readings, instances, environment WHERE readings.number_resource_FK = 3304 AND readings.id_instance_FK = instances.id_instance AND instances.id_environment_FK = environment.id_environment AND environment.id_environment='{}' ORDER BY hour_reading DESC LIMIT 1".format(id_environment)).fetchall())

    

    """ ---avisos---{fazer um for para os avisos, principalmente para a bateria} """

    chart_temp = chart_temp.render_data_uri()
    chart_humi = chart_humi.render_data_uri()
    if "id_user" in session:
        return render_template("index.html", chart_temp = chart_temp, chart_humi=chart_humi, average_temp=average_temp, average_humi=average_humi, environment_readings=environment_readings, last_temp=last_temp, last_humi=last_humi)
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
    password = request.form.get("password")
    conn = get_db_connection()
    
    try:
        conn.execute('SELECT login, password FROM users WHERE login= ? AND password= ?',(login, password)).fetchall()
        if "id_user" in session:
            session.pop("id_user", None)
            session.pop("name_user", None)
            session.pop("role_user", None)
        user = conn.execute('SELECT id_user, name, role FROM users WHERE login=?', (login,)).fetchall()
        session["id_user"] = user[0][0]
        session["name_user"] = user[0][1]
        session["role_user"] = user[0][2]
        conn.close
        return redirect('home')
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
        session.pop("name_user", None)
        session.pop("role_user", None)
        return redirect("login")
    else:
        return redirect("login")


# --- páginas de cadastro ---

# cadastro de ambientes
@app.route('/cadastro/ambiente', methods=["POST"])
def cadAmbiente():

    name = request.form["name"]

    if request.form["status"] == "ativo":
        status = 1
    else:
        status = 0

    if not name:
        flash('É obrigatório inserir um nome')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO environment (name, status) VALUES (?, ?)',
                     (name, status))
        conn.commit()
        conn.close()

    return redirect('/cadastro/ambiente')

@app.route('/cadastro/ambiente', methods=["GET"])
def getAmbiente():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        environment = conn.execute('SELECT * FROM environment').fetchall()
        conn.close()
        return render_template("cadastroAmbientes.html", environment=environment)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")


# cadastro de instâncias
@app.route('/cadastro/instancias', methods=["POST"])
def cadInstancia():
    name = request.form["name"]
    number = request.form["number"]
    id_environment_fk = request.form["id_environment_fk"]

    if request.form["status"] == "ativa":
        status = 1
    else:
        status = 0

    if not name:
        flash('É obrigatório inserir um nome')
    elif not number:
        flash('É obrigatório definir um número de instância')
    elif not id_environment_fk:
        # talvez esse seja redundante
        flash('É obrigatório definir um id de ambiente')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO instances (name, id_environment_FK, number_instance, status) VALUES (?, ?, ?, ?)',
                     (name, id_environment_fk, number, status))
        conn.commit()
        conn.close()

        return redirect('/cadastro/instancias')

@app.route('/cadastro/instancias', methods=["GET"])
def getInstancia():

    if "id_user" in session:
        try:
            id_env = int(request.args.get('id'))
        except:
            id_env = None
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        instance = conn.execute('SELECT * FROM instances').fetchall()
        environment = conn.execute('SELECT * FROM environment WHERE status==1').fetchall()
        if id_env == None:
            return render_template('cadastroInstancias.html', environment=environment, instance=instance, id_env=None)
        else:
            for environment_item in environment:
                if environment_item['id_environment'] == id_env:
                    conn.close()
                    return render_template('cadastroInstancias.html', environment=environment, instance=instance, id_env=id_env)
            return render_template('cadastroInstancias.html', environment=environment, instance=instance, id_env=None)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")

# cadastro de recursos
@app.route('/cadastro/recursos', methods=["POST"])
def cadRecurso():
    val_start = request.form["val_start"]
    val_end = request.form["val_end"]

    if val_start > val_end:
        return render_template("cadastroRecursos.html", aviso="O valor final deve ser maior que o inicial. Tente novamente.")
    else:

        name = request.form['name']
        number = request.form['number']

        if not name:
            flash('É obrigatório inserir um nome')
        elif not number:
            flash('É obrigatório definir um número de recurso')
        elif not val_start:
            flash('É obrigatório definir um valor inicial')
        elif not val_end:
            flash('É obrigatório definir um valor final')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO resources (name, number_resource, val_start, val_end) VALUES (?, ?, ?, ?)',
                         (name, number, val_start, val_end))
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
    id_resource_fk = request.form["id_resource_fk"]
    id_instance_fk = request.form["id_instance_fk"]

    if request.form["status"] == "ativo":
        status = 1
    else:
        status = 0

    if request.form["normal"] == "ativo":
        normal = 1
    else:
        normal = 0

    conn = get_db_connection()
    conn.execute('INSERT INTO instances_resources (status, id_resource_FK, id_instance_FK, normal) VALUES (?, ?, ?, ?)',
                 (status, id_resource_fk, id_instance_fk, normal))
    conn.commit()
    conn.close()

    return redirect('/cadastro/instancias_recursos')

@app.route('/cadastro/instancias_recursos', methods=["GET"])
def getInstanciaRecurso():


    if "id_user" in session:

        
        try:
            id_ins = int(request.args.get('id_ins'))
        except:
            id_ins = None
        
        try:
            id_res = int(request.args.get('id_res'))
        except:
            id_res = None
            
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        resource = conn.execute('SELECT * FROM resources').fetchall()
        instance = conn.execute(
            'SELECT * FROM instances  WHERE status==1').fetchall()
        instance_resource = conn.execute(
            'SELECT * FROM instances_resources').fetchall()
        conn.close()

        id_ins_data = None
        id_res_data = None
        if id_res == None and id_ins != None:
            for instance_item in instance:
                if instance_item['id_instance'] == id_res:
                    id_ins_data = id_ins
                    break
            return render_template('cadastroInstanciaRecurso.html', resource=resource, instance=instance, instance_resource=instance_resource, id_ins=id_ins_data, id_res=None)
        elif id_res != None and id_ins == None:
            for resource_item in resource:
                if resource_item['id_resource'] == id_res:
                    id_res_data = id_res
                    break
            return render_template('cadastroInstanciaRecurso.html', resource=resource, instance=instance, instance_resource=instance_resource, id_ins=None, id_res=id_res_data)
        elif id_res != None and id_ins != None:
            for instance_item in instance:
                if instance_item['id_instance'] == id_res:
                    id_ins_data = id_ins
            for resource_item in resource:
                if resource_item['id_resource'] == id_res:
                    id_res_data = id_res
            return render_template('cadastroInstanciaRecurso.html', resource=resource, instance=instance, instance_resource=instance_resource, id_ins=id_ins_data, id_res=id_res_data)
        else:
            return render_template('cadastroInstanciaRecurso.html', resource=resource, instance=instance, instance_resource=instance_resource, id_ins=None, id_res=None)
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
        environment = conn.execute('SELECT * FROM environment').fetchall()
        instance = conn.execute('SELECT * FROM instances').fetchall()
        resource = conn.execute('SELECT * FROM resources').fetchall()
        instance_resource = conn.execute('SELECT * FROM instances_resources').fetchall()
        users = conn.execute('SELECT * FROM users').fetchall()
        reading = conn.execute('SELECT * FROM readings ORDER BY hour_reading DESC LIMIT 4').fetchall()
        conn.close()
        return render_template('verDados.html', environment=environment, instance=instance, resource=resource, instance_resource=instance_resource, user=users, reading=reading)
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
