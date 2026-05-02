from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.bayes_model import BayesModel
import os

app = Flask(__name__)
CORS(app)

# ruta correcta al XML
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XML_PATH = os.path.join(BASE_DIR, "model", "red_bayesiana_clean.xml")

# cargar modelo UNA VEZ
modelo = BayesModel(XML_PATH, "Estabilidad_Laboral")


@app.route("/")
def home():
    return "API de predicción funcionando"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    print("\n===== DATA QUE LLEGA DEL FRONT =====")
    print(data)

    try:
        resultado = modelo.query(data)

        print("===== RESULTADO DEL MODELO =====")
        print(resultado)

        # convertir a porcentaje
        resultado = {
            k: round(v * 100, 2) for k, v in resultado.items()
        }

        return jsonify(resultado)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)