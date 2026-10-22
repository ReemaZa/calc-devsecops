import pytest

from app import app
from calculator import CalcError, safe_eval


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index(client):
    assert client.get("/").status_code == 200


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("2+3*4", 14),
        ("(2+3)*4", 20),
        ("2^10", 1024),
        ("-5 + 8 / 2", -1),
        ("10 % 4", 2),
        ("sqrt(16) + abs(-3)", 7),
        ("fact(5)", 120),
        ("log(1000)", 3),
        ("ln(e)", 1),
        ("2*pi", pytest.approx(6.283185307179)),
    ],
)
def test_expressions(expr, expected):
    assert safe_eval(expr) == expected


def test_angle_modes():
    assert safe_eval("sin(90)", "deg") == 1
    assert safe_eval("sin(pi/2)", "rad") == 1
    assert safe_eval("asin(1)", "deg") == 90


@pytest.mark.parametrize(
    "bad",
    [
        "1/0",
        "sqrt(-1)",
        "2**100000",
        "9**9**9",
        "__import__('os').system('id')",
        "().__class__",
        "open('/etc/passwd')",
        "[x for x in range(3)]",
        "1+",
        "a+1",
        "1" * 300,
    ],
)
def test_rejects_dangerous_or_invalid(bad):
    with pytest.raises(CalcError):
        safe_eval(bad)


def test_api_ok(client):
    r = client.post("/api/evaluate", json={"expression": "2*(3+4)^2", "angle": "rad"})
    assert r.status_code == 200
    assert r.get_json()["result"] == 98


def test_api_rejects_injection(client):
    r = client.post("/api/evaluate", json={"expression": "__import__('os').getcwd()"})
    assert r.status_code == 400


def test_api_empty_and_bad_angle(client):
    assert client.post("/api/evaluate", json={"expression": ""}).status_code == 400
    assert client.post("/api/evaluate", json={"expression": "1", "angle": "x"}).status_code == 400


