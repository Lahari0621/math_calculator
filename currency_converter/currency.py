from flask import Flask, render_template, request, jsonify
from forex_python.converter import CurrencyRates

app = Flask(__name__)
c = CurrencyRates()

currency_codes = ['USD', 'INR', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    default_from = 'USD'
    default_to = 'INR'

    if request.method == 'POST':
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = float(request.form['amount'])

        try:
            converted = round(c.convert(from_currency, to_currency, amount))
            result = f"{int(amount)} {from_currency} = {int(converted)} {to_currency}"
        except Exception as e:
            result = f"Error: {e}"

        return render_template('index.html', result=result, currency_codes=currency_codes,
                               default_from=from_currency, default_to=to_currency)

    return render_template('index.html', currency_codes=currency_codes,
                           default_from=default_from, default_to=default_to)

@app.route('/rate')
def get_rate():
    from_curr = request.args.get('from')
    to_curr = request.args.get('to')
    try:
        rate = c.get_rate(from_curr, to_curr)
        return jsonify({'rate': round(rate, 2)})
    except Exception:
        return jsonify({'rate': None})

if __name__ == '__main__':
    app.run(debug=True)
