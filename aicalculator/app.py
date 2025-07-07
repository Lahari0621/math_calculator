from flask import Flask, request, jsonify, render_template
from sympy import *
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # frontend UI

@app.route('/solve', methods=['POST'])
def solve_route():
    data = request.get_json()
    expr = data.get('query')
    mode = data.get('mode', 'radian')

    x, y, z = symbols('x y z')
    local_dict = {'x': x, 'y': y, 'z': z, 'pi': pi, 'e': E}

    try:
        parsed_expr = sympify(expr, locals=local_dict)

        if mode == 'degree':
            def deg_wrap(e):
                return e.replace(
                    lambda expr: isinstance(expr, Function) and expr.func in (sin, cos, tan),
                    lambda f: f.func(f.args[0] * pi / 180)
                )
            parsed_expr = deg_wrap(parsed_expr)

        result = solve(parsed_expr, x)

        return jsonify({'result': str(result)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
