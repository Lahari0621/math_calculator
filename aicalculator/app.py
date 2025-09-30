from flask import Flask, render_template, request, jsonify
import sympy as sp

app = Flask(__name__, template_folder="templates")

# symbols for algebra
x, y = sp.symbols("x y")
LOCAL_SYMBOLS = {
    "x": x,
    "y": y,
    "e": sp.E,
    "pi": sp.pi,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "cot": sp.cot,
    "sec": sp.sec,
    "csc": sp.csc,
    "sqrt": sp.sqrt,
    "log": sp.log,
    "diff": sp.diff,
    "integrate": sp.integrate
}

history = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    """
    Evaluate algebra/trig/differentiation/integration expressions.
    Accepts JSON:
      { expression: str, mode: "radian"|"degree", output: "dec"|"frac" }
    Returns:
      { result: str, history: [str] } (or error)
    """
    data = request.get_json() or {}
    expr = (data.get("expression") or "").strip()
    mode = data.get("mode", "radian")
    output = data.get("output", "dec")

    try:
        # normalize power
        expr = expr.replace("^", "**")

        # handle degree -> convert trig functions to radians
        if mode == "degree":
            # replace trig(name( ... ) ) with name(pi/180* ... )
            # simple replaces are usually fine because user uses sin( ... )
            expr = expr.replace("sin(", "sin(pi/180*")
            expr = expr.replace("cos(", "cos(pi/180*")
            expr = expr.replace("tan(", "tan(pi/180*")
            expr = expr.replace("cot(", "cot(pi/180*")
            expr = expr.replace("sec(", "sec(pi/180*")
            expr = expr.replace("csc(", "csc(pi/180*")

        # If expression is an equation containing '=' => solve
        if "=" in expr:
            # split only on the first '=', preserve RHS that might contain '=' incorrectly
            left, right = expr.split("=", 1)
            left_s = left.strip() or "0"
            right_s = right.strip() or "0"
            lhs = sp.sympify(left_s, locals=LOCAL_SYMBOLS)
            rhs = sp.sympify(right_s, locals=LOCAL_SYMBOLS)
            eq = sp.Eq(lhs, rhs)

            # try to solve for x first, else solve for all symbols
            try:
                sol = sp.solve(eq, x, dict=True)
                # if nothing returned for x, fallback:
                if sol == []:
                    sol = sp.solve(eq, dict=True)
            except Exception:
                sol = sp.solve(eq, dict=True)

            result = sol
            result_str = str(sol)

        else:
            # differentiation shorthand: diff(expr, x) or diff(expr)
            if expr.startswith("diff(") and expr.endswith(")"):
                inner = expr[5:-1]
                parsed = sp.sympify(inner, locals=LOCAL_SYMBOLS)
                result = sp.diff(parsed, x)
                result_str = str(result)
            # integration shorthand: integrate(expr, x) or integrate(expr)
            elif expr.startswith("integrate(") and expr.endswith(")"):
                inner = expr[10:-1]
                parsed = sp.sympify(inner, locals=LOCAL_SYMBOLS)
                result = sp.integrate(parsed, x)
                result_str = str(result)
            else:
                parsed = sp.sympify(expr, locals=LOCAL_SYMBOLS)
                if output == "frac":
                    result = sp.nsimplify(parsed, rational=True)
                    # special case like sqrt(2)/2 -> 1/sqrt(2)
                    if str(result) == "sqrt(2)/2":
                        result = sp.sympify("1/sqrt(2)")
                    result_str = str(result)
                else:
                    result = parsed.evalf()
                    result_str = str(result)

        # store history (original typed expression with clean formatting)
        hist_entry = f"{expr} = {result_str}"
        history.append(hist_entry)

        return jsonify({"result": result_str, "history": history})

    except Exception as e:
        # include history too so frontend can update display
        err = str(e)
        history.append(f"{expr} = Error: {err}")
        return jsonify({"error": err, "history": history}), 400


@app.route("/matrix", methods=["POST"])
def matrix_ops():
    """
    Perform matrix operations.
    Accepts JSON:
      {
        matrices: [ [[r,c],...] , ... ],
        operation: "add"|"sub"|"mul"|"div"|"det"|"transpose"|"inverse"
      }
    Returns:
      { result: <matrix-string-or-simple>, history: [...] } or error
    """
    data = request.get_json() or {}
    matrices = data.get("matrices", [])
    operation = data.get("operation", "add")

    try:
        if not matrices or not isinstance(matrices, list):
            raise ValueError("No matrices provided")

        # Convert each to sympy.Matrix
        sp_mats = [sp.Matrix(m) for m in matrices]

        # sanity: ensure shapes are compatible
        if operation in ("add", "sub"):
            # all same shape
            shapes = [m.shape for m in sp_mats]
            if any(s != shapes[0] for s in shapes):
                raise ValueError("All matrices must have same dimensions for add/sub")
        if operation == "mul":
            # chain multiply, check dims
            # We'll attempt and catch dimensional errors
            pass

        # compute
        if operation == "add":
            result = sp_mats[0]
            for m in sp_mats[1:]:
                result = result + m
        elif operation == "sub":
            result = sp_mats[0]
            for m in sp_mats[1:]:
                result = result - m
        elif operation == "mul":
            result = sp_mats[0]
            for m in sp_mats[1:]:
                result = result * m
        elif operation == "div":
            # multi-matrix division interpreted as A * inv(B) for 2 matrices
            if len(sp_mats) != 2:
                raise ValueError("Division currently supports exactly 2 matrices (A / B -> A * B^-1)")
            result = sp_mats[0] * sp_mats[1].inv()
        elif operation == "det":
            result = sp_mats[0].det()
        elif operation == "transpose":
            result = sp_mats[0].T
        elif operation == "inverse":
            result = sp_mats[0].inv()
        else:
            raise ValueError("Unknown matrix operation")

        # produce two friendly outputs:
        # - compact string for the main display (single-line)
        # - pretty HTML table string for history to show matrix nicely
        if isinstance(result, sp.Matrix):
            compact = "[" + "; ".join([", ".join(map(str, row)) for row in result.tolist()]) + "]"
            # build HTML table
            table_html = "<table style='border-collapse:collapse;'>"
            for r in result.tolist():
                table_html += "<tr>"
                for v in r:
                    table_html += f"<td style='border:1px solid #0ff;padding:4px 8px'>{sp.N(v)}</td>"
                table_html += "</tr>"
            table_html += "</table>"
            result_str = compact
            hist_entry = f"Matrix {operation} = {table_html}"
        else:
            # scalar result (det)
            result_str = str(sp.N(result))
            hist_entry = f"Matrix {operation} = {result_str}"

        # store in history
        history.append(hist_entry)
        return jsonify({"result": result_str, "history": history})

    except Exception as e:
        err = str(e)
        history.append(f"Matrix {operation} = Error: {err}")
        return jsonify({"error": err, "history": history}), 400


@app.route("/clear_history", methods=["POST"])
def clear_history():
    history.clear()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
