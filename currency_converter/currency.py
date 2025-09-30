from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_currencies():
    try:
        res = requests.get("https://api.frankfurter.app/currencies")
        return res.json()
    except Exception as e:
        print("Error fetching currencies:", e)
        return {}

@app.route("/", methods=["GET", "POST"])
def index():
    currencies = get_currencies()
    result = None
    rate = None
    from_currency = "USD"
    to_currency = "INR"
    amount = 1.0

    if request.method == "POST":
        try:
            from_currency = request.form["from_currency"]
            to_currency = request.form["to_currency"]
            amount = float(request.form["amount"])
            url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
            data = requests.get(url).json()
            result = round(data["rates"][to_currency], 4)
            rate = round(data["rates"][to_currency] / amount, 4)
        except Exception as e:
            print("Conversion error:", e)

    return render_template("index.html",
                           currency_codes=currencies,
                           from_currency=from_currency,
                           to_currency=to_currency,
                           amount=amount,
                           result=result,
                           rate=rate)

@app.route("/rate")
def get_rate():
    from_currency = request.args.get("from")
    to_currency = request.args.get("to")
    try:
        url = f"https://api.frankfurter.app/latest?amount=1&from={from_currency}&to={to_currency}"
        data = requests.get(url).json()
        return jsonify({"rate": round(data["rates"][to_currency], 4)})
    except:
        return jsonify({"rate": None})

if __name__ == "__main__":
    app.run(debug=True)
