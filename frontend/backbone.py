from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


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
        nomeRecurso = "nomeRecurso"
        recursoNumero = "recursoNumero"
        valorInicial = request.form["vlIniAmb"]
        valorFinal = request.form["vlFinAmb"]
        return redirect(url_for("/verdados"))

@app.route('/cadastro/recursos', methods=["GET"])
def getRecurso():
    return render_template("cadastroRecursos.html")



@app.route('/verdados')
def verDados():
    return render_template("verDados.html")

if __name__ == "__main__":
    app.run(debug=True)
