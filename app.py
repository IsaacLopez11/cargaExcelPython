from services.ventas_service import procesar_ventas
import json
from flask import Flask, render_template, request
import os
import pandas as pd
from services.excel_service import calcular


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

if not os.path.exists("uploads"):
    os.makedirs("uploads")


@app.route("/", methods=["GET", "POST"])
def index():
    personas = []
    resultados = {}

    if request.method == "POST":
        archivo = request.files.get("archivo")

        if archivo:
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
            archivo.save(ruta)

            df = pd.read_excel(ruta)
                       
            personas = df.to_dict(orient="records")
            
    return render_template("index.html",
                           personas=personas,
                           )

@app.route("/ventas", methods=["GET", "POST"])
def ventas():

    datos = []
    resultados = {}

    if request.method == "POST":
        archivo = request.files.get("archivo")

        if archivo:
            ruta = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
            archivo.save(ruta)

            df = pd.read_excel(ruta)

            resultados, datos = procesar_ventas(df)

    return render_template(
        "ventas.html",
        datos=datos,
        resultados=resultados,
        ventas_mes=resultados.get("ventas_mes", {}),
        ventas_categoria=resultados.get("ventas_categoria", {}),
        top_vendedor=resultados.get("top_vendedor", "")
    )

if __name__ == "__main__":
    app.run(debug=True)