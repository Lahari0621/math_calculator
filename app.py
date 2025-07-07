from flask import Flask, request, jsonify, render_template
from sympy import symbols, sympify, solve, diff, integrate, pi, sin, cos, tan, E, I, Function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve_route():
    data = request.get_json()
    expr = data.get('query', '')
    mode = data.get('mode', 'radian')  # 'degree' or 'radian'

    x, y, z = symbols('x y z')
    local_dict = {
        'x': x, 'y': y, 'z': z,
        'pi': pi, 'e': E, 'i': I,
        'sin': sin, 'cos': cos, 'tan': tan,
        'solve': solve, 'diff': diff, 'integrate': integrate
    }

    try:
        parsed_expr = sympify(expr, locals=local_dict)

        # ✅ Convert degrees to radians for trig functions
        if mode == 'degree':
            def convert_deg_to_rad(expr):
                return expr.replace(
                    lambda arg: isinstance(arg, Function) and arg.func in (sin, cos, tan),
                    lambda f: f.func(f.args[0] * pi / 180)
                )
            parsed_expr = convert_deg_to_rad(parsed_expr)

        # ✅ Solve or evaluate
        if hasattr(parsed_expr, 'free_symbols') and x in parsed_expr.free_symbols:
            result = solve(parsed_expr, x)
        else:
            result = parsed_expr

        # ✅ Format result
        if isinstance(result, list):
            real_results = [r.evalf(6) for r in result if r.is_real]
            if not real_results:
                return jsonify({'result': 'No real solution'})
            result = ', '.join(str(r) for r in real_results)
        else:
            result = result.evalf(6)
            if hasattr(result, 'is_real') and not result.is_real:
                return jsonify({'result': 'No real solution'})
            result = str(result)

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
