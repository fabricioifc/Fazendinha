from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/cadastro/ambiente')
def cadAmbiente():
    return render_template("cadastroAmbientes.html")

if __name__ == "__main__":
    app.run(debug=True)
