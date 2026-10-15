
from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

MODEL_PATH = "spam_model.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model not found. Run: python train_model.py"
    )

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Please enter an email message."
        }), 400

    prediction = model.predict([message])[0]

    if prediction == "spam":
        result = "Spam"
        explanation = "This message may be unwanted or suspicious."
    else:
        result = "Not Spam"
        explanation = "This message appears legitimate."

    return jsonify({
        "prediction": result,
        "message": explanation
    })


if __name__ == "__main__":
    app.run(debug=True)
