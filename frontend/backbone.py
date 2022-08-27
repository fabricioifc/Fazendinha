from array import array
from datetime import datetime
from datetime import timedelta
from ast import For
import itertools
from os import environ
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
    if "id_user" in session:

        conn = get_db_connection()
        chart_temp = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style, show_x_labels=False)

        """ ---gráfico das ultimas leituras de temperatura--- """
        readings_temp = conn.execute("SELECT hour_reading, value, id_instance_FK, name FROM readings, instances WHERE readings.id_instance_FK=instances.id_instance AND number_resource_FK=3303 ORDER BY hour_reading DESC LIMIT 50").fetchall()
        readings_temp.reverse()
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
        chart_temp.title = 'Ultimas leituras de temperatura'
        chart_temp.y_labels = map(int, range(min_temp, max_temp, +5))
        chart_temp.x_labels = hour_temp
            
    
        """ ---gráfico das leituras de temperatura com alternação de 5 min--- """

        env = conn.execute("""
        SELECT id_environment FROM environment WHERE status = 1
        """).fetchall()
        id_env = 5
        qtd_readings = 5
        break_time = 5
        average_temp_hour=0
        temp = []

        chart_temp_hours = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style, show_x_labels=False)
        chartDate = datetime.now().replace(microsecond=0, second=0) + timedelta(minutes= - (break_time * qtd_readings))
        for env in env: 
            reads = conn.execute("""
            SELECT hour_reading value, environment.name FROM readings, instances, environment WHERE number_resource_FK=3303 AND readings.id_instance_FK=instances.id_instance AND instances.id_environment_FK=environment.id_environment AND environment.id_environment={} 
            ORDER BY hour_reading DESC LIMIT {}
            """.format(env[0], id_env)).fetchall()
            graph_date=[]
            if reads:
                reads.reverse()
                x = 1
                for read in reads:
                    hour_read = datetime.strptime(read[0], '%Y-%m-%d %H:%M:%S')
                    while x<qtd_readings:
                        if (hour_read >= chartDate and hour_read < (chartDate + timedelta(minutes= +break_time))):
                            """ adicionar esse horario no campo e colocar o valor dessa leitura na média que posteriormente sera colocada numa lista para então ele ser posto no gráfico """
                            graph_date.append(read[1])
                            x+=1
                            average_temp_hour+=read[1]
                            break
                        
                        else:
                            """ adicionar mais 5 minutos no chartDate e adicionar um valor None na lista, ele dira que não há leituras de temperatura nesses 5 minutos """
                            chartDate = chartDate + timedelta(minutes= +break_time)
                            graph_date.append(None)

                            """ print (chartDate + timedelta(minutes= +break_time)) """
                            if average_temp_hour:
                                temp.append()
                            temp.append(None)
                            average_temp_hour=0
                            x+=1
                """ nesse momento adiciona o chart_date """

            else:
                pass
        print (temp)
        chart_temp_hours.title = 'Ultimas horas de temperatura'
        chart_temp_hours.add("teste", temp)
        chart_temp_hours = chart_temp_hours.render_data_uri()
        del graph_date
       

        """ ---gráfico das leituras de humidade--- """
        readings_humi = conn.execute("SELECT hour_reading, value, id_instance_FK, name FROM readings INNER JOIN instances WHERE readings.id_instance_FK=instances.id_instance AND number_resource_FK=3304 ORDER BY hour_reading DESC LIMIT 50").fetchall()
        readings_humi.reverse()
        chart_humi = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style, show_x_labels=False)
        chart_humi.title='Gráfico de umidade'    
        hour_humi = []
        humi = []
        qtd_val = 0
        average_humi = 0
        
        for row in readings_humi:
            hour_humi.append(row[0])
            humi.append(row[1])
            average_humi+=row[1]
            qtd_val+=1
        average_humi/=qtd_val
        average_humi = round(average_humi, 2)
        chart_humi.add(row[3], humi )
        max_humi = int(max(humi)+10)
        min_humi = int(min(humi)-10)

        if (max_humi - min_humi >= 50):
            chart_humi.y_labels = map(int, range(min_humi, max_humi, +10))
        else:
            chart_humi.y_labels = map(int, range(min_humi, max_humi, +5))
        chart_humi.x_labels = hour_humi

        """ ---gráfico das leituras de humidade com alternação de 5 min--- """

        env = conn.execute("""
        SELECT id_environment FROM environment WHERE status = 1
        """).fetchall()
        id_env = 5
        qtd_readings = 5
        break_time = 5
        average_humi_hour=0
        humi = []

        chart_humi_hours = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style, show_x_labels=False)
        chartDate = datetime.now().replace(microsecond=0, second=0) + timedelta(minutes= - (break_time * qtd_readings))
        for env in env: 
            reads = conn.execute("""
            SELECT hour_reading value, environment.name FROM readings, instances, environment WHERE number_resource_FK=3303 AND readings.id_instance_FK=instances.id_instance AND instances.id_environment_FK=environment.id_environment AND environment.id_environment={} 
            ORDER BY hour_reading DESC LIMIT {}
            """.format(env[0], id_env)).fetchall()
            graph_date=[]
            if reads:
                reads.reverse()
                x = 1
                for read in reads:
                    hour_read = datetime.strptime(read[0], '%Y-%m-%d %H:%M:%S')
                    while x<qtd_readings:
                        if (hour_read >= chartDate and hour_read < (chartDate + timedelta(minutes= +break_time))):
                            """ adicionar esse horario no campo e colocar o valor dessa leitura na média que posteriormente sera colocada numa lista para então ele ser posto no gráfico """
                            graph_date.append(read[1])
                            x+=1
                            average_humi_hour+=read[1]
                            break
                        
                        else:
                            """ adicionar mais 5 minutos no chartDate e adicionar um valor None na lista, ele dira que não há leituras de umidade nesses 5 minutos """
                            chartDate = chartDate + timedelta(minutes= +break_time)
                            graph_date.append(None)

                            """ print (chartDate + timedelta(minutes= +break_time)) """
                            if average_humi_hour:
                                humi.append()
                            humi.append(None)
                            average_humi_hour=0
                            x+=1
                """ nesse momento adiciona o chart_date """

            else:
                pass
        print (humi)
        chart_humi_hours.title = 'Ultimas horas de umidade'
        chart_humi_hours.add("teste", humi)
        chart_humi_hours = chart_humi_hours.render_data_uri()
        del graph_date

        """ ---tabela da ultima leitura de cada ambiente--- """
        conn.row_factory = sqlite3.Row
        environment_readings = conn.execute("SELECT * FROM environment WHERE status=1").fetchall()
        last_temp = list()
        last_humi = list()
        for environment in environment_readings:
            id_environment = environment['id_environment']
            last_temp.extend(conn.execute("SELECT hour_reading, id_instance_FK, number_resource_FK, value, id_instance, id_environment_FK, id_environment, environment.name FROM readings, instances, environment WHERE readings.number_resource_FK = 3303 AND readings.id_instance_FK = instances.id_instance AND instances.id_environment_FK = environment.id_environment AND environment.id_environment={} ORDER BY hour_reading DESC LIMIT 1".format(id_environment)).fetchall())

            last_humi.extend(conn.execute("SELECT hour_reading, id_instance_FK, number_resource_FK, value, id_instance, id_environment_FK, id_environment, environment.name FROM readings, instances, environment WHERE readings.number_resource_FK = 3304 AND readings.id_instance_FK = instances.id_instance AND instances.id_environment_FK = environment.id_environment AND environment.id_environment={} ORDER BY hour_reading DESC LIMIT 1".format(id_environment)).fetchall())

        

        """ ---avisos---{fazer um for para os avisos, principalmente para a bateria} """

        chart_temp = chart_temp.render_data_uri()
        chart_humi = chart_humi.render_data_uri()

        return render_template("index.html", chart_temp = chart_temp, chart_temp_hours=chart_temp_hours, chart_humi=chart_humi,chart_humi_hours=chart_humi_hours, average_temp=average_temp, average_temp_hour=average_temp_hour, average_humi=average_humi, average_humi_hour=average_humi_hour, environment_readings=environment_readings, last_temp=last_temp, last_humi=last_humi)
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
                if instance_item['id_instance'] == id_ins:
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
                if instance_item['id_instance'] == id_ins:
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

@app.route('/verleituras', methods=["GET"])
def getVerLeituras():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        leituras = conn.execute('SELECT readings.*, resources.name r_name, instances.name i_name FROM readings, resources, instances WHERE readings.number_resource_FK=resources.number_resource AND readings.id_instance_FK=instances.id_instance ORDER BY hour_reading DESC LIMIT 50').fetchall()
        return render_template('verLeituras.html', leituras=leituras)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")

# testes de gráficos

@app.route('/testegrafico', methods=["GET"])
def testegrafico():
    if "id_user" in session:
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        env = conn.execute("""
        SELECT id_environment FROM environment WHERE status = 1
        """).fetchall()
        id_env = 5
        qtd_readings = 5
        break_time = 5
        average_temp=0
        temp = []

        chart_temp_hours = pygal.Line(inner_radius=0, legend_at_bottom=True, style=custom_style, show_x_labels=False)
        chartDate = datetime.now().replace(microsecond=0, second=0) + timedelta(minutes= - (break_time * qtd_readings))
        for env in env: 
            reads = conn.execute("""
            SELECT hour_reading value, environment.name FROM readings, instances, environment WHERE number_resource_FK=3303 AND readings.id_instance_FK=instances.id_instance AND instances.id_environment_FK=environment.id_environment AND environment.id_environment={} 
            ORDER BY hour_reading DESC LIMIT {}
            """.format(env[0], id_env)).fetchall()
            graph_date=[]
            if reads:
                reads.reverse()
                x = 1
                for read in reads:
                    hour_read = datetime.strptime(read[0], '%Y-%m-%d %H:%M:%S')
                    while x<qtd_readings:
                        if (hour_read >= chartDate and hour_read < (chartDate + timedelta(minutes= +break_time))):
                            """ adicionar esse horario no campo e colocar o valor dessa leitura na média que posteriormente sera colocada numa lista para então ele ser posto no gráfico """
                            graph_date.append(read[1])
                            x+=1
                            average_temp+=read[1]
                            break
                        
                        else:
                            """ adicionar mais 5 minutos no chartDate e adicionar um valor None na lista, ele dira que não há leituras de temperatura nesses 5 minutos """
                            chartDate = chartDate + timedelta(minutes= +break_time)
                            graph_date.append(None)

                            """ print (chartDate + timedelta(minutes= +break_time)) """
                            if average_temp:
                                temp.append()
                            temp.append(None)
                            average_temp=0
                            x+=1
                """ nesse momento adiciona o chart_date """

            else:
                pass
        print (temp)
        chart_temp_hours.add("teste", temp)
        chart_temp_hours = chart_temp_hours.render_data_uri()
        del graph_date

        return render_template('testegrafico.html', chart_temp_hours=chart_temp_hours)
    else:
        flash('Por favor insira suas credenciais','NENHUM USUÁRIO CONECTADO! ')
        return redirect("login")

if __name__ == "__main__":
    app.run(debug=True)
