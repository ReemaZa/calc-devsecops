"""Moteur de calcul SECURISE : analyse l'expression avec `ast` et n'autorise
qu'une liste blanche d'opérations. Aucun appel à eval()/exec()."""
import ast
import math
import operator

MAX_LEN = 200
MAX_EXPONENT = 1000


class CalcError(ValueError):
    """Erreur de calcul affichable à l'utilisateur."""


def _pow(a, b):
    if abs(b) > MAX_EXPONENT:
        raise CalcError("Exposant trop grand")
    return a ** b


BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: _pow,
}
UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}
CONSTANTS = {"pi": math.pi, "e": math.e}


def _fact(x):
    if x != int(x) or x < 0 or x > 170:
        raise CalcError("Factorielle : entier entre 0 et 170")
    return float(math.factorial(int(x)))


def _functions(angle):
    to_rad = math.radians if angle == "deg" else (lambda x: x)
    from_rad = math.degrees if angle == "deg" else (lambda x: x)
    return {
        "sqrt": math.sqrt,
        "sin": lambda x: math.sin(to_rad(x)),
        "cos": lambda x: math.cos(to_rad(x)),
        "tan": lambda x: math.tan(to_rad(x)),
        "asin": lambda x: from_rad(math.asin(x)),
        "acos": lambda x: from_rad(math.acos(x)),
        "atan": lambda x: from_rad(math.atan(x)),
        "log": math.log10,
        "ln": math.log,
        "exp": math.exp,
        "abs": abs,
        "fact": _fact,
    }


def safe_eval(expression, angle="rad"):
    if len(expression) > MAX_LEN:
        raise CalcError("Expression trop longue")
    expression = expression.replace("^", "**").strip()
    funcs = _functions(angle)

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return float(node.value)
            raise CalcError("Valeur non autorisée")
        if isinstance(node, ast.Name):
            if node.id in CONSTANTS:
                return CONSTANTS[node.id]
            raise CalcError(f"Symbole inconnu : {node.id}")
        if isinstance(node, ast.BinOp) and type(node.op) in BIN_OPS:
            return BIN_OPS[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            return UNARY_OPS[type(node.op)](ev(node.operand))
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in funcs
            and len(node.args) == 1
            and not node.keywords
        ):
            return funcs[node.func.id](ev(node.args[0]))
        raise CalcError("Expression non autorisée")

    try:
        result = ev(ast.parse(expression, mode="eval"))
    except CalcError:
        raise
    except ZeroDivisionError:
        raise CalcError("Division par zéro")
    except OverflowError:
        raise CalcError("Résultat trop grand")
    except (SyntaxError, RecursionError, MemoryError):
        raise CalcError("Expression invalide")
    except ValueError:
        raise CalcError("Hors du domaine de définition")

    if not isinstance(result, float) or not math.isfinite(result):
        raise CalcError("Résultat invalide")
    if result.is_integer() and abs(result) < 1e15:
        return int(result)
    return round(result, 12)
