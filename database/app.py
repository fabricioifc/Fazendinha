import sqlite3
from flask import Flask, flash, render_template, redirect, request, url_for


app = Flask(__name__)
app.config['SECRET_KEY'] = ''

def get_db_connection():
    conn = sqlite3.connect('../data/database/bancoDados.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/visualizar/ambientes')
def visAmbientes():
    conn = get_db_connection()
    ambientes = conn.execute('SELECT * FROM ambientes').fetchall()
    conn.close()
    return render_template('visualizarAmbientes.html', ambientes=ambientes)


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
    elif not statusAmbiente:
        flash('É obrigatório definir um status')
    else:
        conn = get_db_connection()
        conn.execute('INSERT INTO ambientes (name, status) VALUES (?, ?)',
                        (nomeAmbiente, statusAmbiente))
        conn.commit()
        conn.close()

    return redirect(url_for('verDados'))

@app.route('/cadastro/ambiente', methods=["GET"])
def getAmbiente():
    return render_template("cadastroAmbientes.html")


# cadastro de instâncias
@app.route('/cadastro/instancias', methods=["POST"])
def cadInstancia():
    nomeInstancia = request.form["nomeInstancia"]
    instanciaNumero = request.form["instanciaNumero"]

    if request.form["status"]=="ativa":
        statusInstancia=1
    else:
        statusInstancia=0

    return redirect(url_for("verDados"))

@app.route('/cadastro/instancias', methods=["GET"])
def getInstancia():
    
    conn = get_db_connection()
    id_ambiente = conn.execute('SELECT id FROM ambientes').fetchall()
    conn.close()
    return render_template('cadastroInstancias.html', id=id_ambiente)

    # return render_template("cadastroInstancias.html")



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
            return redirect(url_for('home'))

@app.route('/cadastro/recursos', methods=["GET"])
def getRecurso():
    return render_template("cadastroRecursos.html")



if __name__ == "__main__":
    app.run(debug=True)
