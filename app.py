from flask import Flask, render_template, redirect, url_for
from main_logic import listar_drive_files, listar_destino_blob, migrar_arquivos

app = Flask(__name__)

@app.route("/")
def index():
    drive_files = listar_drive_files()
    blob_files = listar_destino_blob()
    return render_template("index.html", drive=drive_files, blob=blob_files)

@app.route("/migrar")
def migrar():
    logs = migrar_arquivos()
    return render_template("resultado.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
