
from crypt import methods
import sqlite3
from flask import Flask, flash, render_template, redirect, request, url_for


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/visualizar/ambientes')
def visAmbientes():
    conn = get_db_connection()
    ambientes = conn.execute('SELECT * FROM ambientes').fetchall()
    conn.close()
    return render_template('visualizarAmbientes.html', ambientes=ambientes)

@app.route('/cadastro/ambiente', methods=('GET', 'POST'))
def cadAmbiente():

    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']

        if not name:#essa parte dos 'flash' não sei se é uma boa deixar, precisa alterar coisas no html para que funcione mas seria legal se funcionase.
            flash('É obrigatório inserir um nome')
        elif not status:
            flash('É obrigatório definir um status')#acho irrelevante afinal já vem definido um status mas é melhor deixar
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO ambientes (name, status) VALUES (?, ?)',
                         (name, status))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template("cadastroAmbientes.html")    

@app.route('/cadastro/recurso', methods=('GET', 'POST'))
def cadAmbiente():

    if request.method == 'POST':
        name = request.form['name']
        resource_number = request.form['resource_numnber']
        vlini = request.form['vlini']
        vlfim = request.form['vlfim']

        if not name:
            flash('É obrigatório inserir um nome')
        elif not resource_number:
            flash('É obrigatório definir um número de recurso')
        elif not vlini:
            flash('É obrigatório definir um valor inicial')
        elif not vlfim:
            flash('É obrigatório definir um valor final')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO resources (name, resource_number, vlini, vlfim) VALUES (?, ?, ?, ?)',
                         (name, resource_number, vlini, vlfim))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template("cadastroResource.html")    

