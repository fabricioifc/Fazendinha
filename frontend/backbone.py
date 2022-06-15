import sqlite3
from flask import Flask, flash, redirect, url_for, render_template, request

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('../data/database/bancoDados.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/home')
def home():
    return render_template("index.html")

# páginas de cadastro

@app.route('/cadastro/ambiente', methods=["POST"])
def cadAmbiente():

    nomeAmbiente = request.form["nomeAmbiente"]
    statusAmbiente=2

    if request.form["status"]=="ativo":
        statusAmbiente=1
    else:
        statusAmbiente=0
    
    return redirect(url_for('verdados'))

@app.route('/cadastro/ambiente', methods=["GET"])
def getAmbiente():
    return render_template("cadastroAmbientes.html")



@app.route('/cadastro/instancias', methods=["POST"])
def cadInstancia():
    nomeInstancia = request.form["nomeInstancia"]
    instanciaNumero = request.form["instanciaNumero"]

    if request.form["status"]=="ativa":
        statusInstancia=1
    else:
        statusInstancia=0

    return redirect(url_for("verdados"))

@app.route('/cadastro/instancias', methods=["GET"])
def getInstancia():
    return render_template("cadastroInstancias.html")




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
            return redirect(url_for('home'))

       
@app.route('/cadastro/recursos', methods=["GET"])
def getRecurso():
    return render_template("cadastroRecursos.html")



@app.route('/verdados')
def verDados():
    return render_template("verDados.html")

if __name__ == "__main__":
    app.run(debug=True)
