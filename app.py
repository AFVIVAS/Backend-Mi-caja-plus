import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_cors import CORS

load_dotenv()

from routes.clientes import cargar_rutas_clientes
from routes.tenderos import cargar_rutas_Tenderos
from routes.operaciones import cargar_rutas_operaciones
from routes.estadisticas import cargar_rutas_estadisticas
from routes.inventario import cargar_rutas_inventario
from routes.abonos import cargar_ruta_abonos
from routes.sesion import cargar_rutas_sesion


app=Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE=os.environ.get("SESSION_COOKIE_SAMESITE", "Lax"),
    SESSION_COOKIE_SECURE=os.environ.get("SESSION_COOKIE_SECURE", "0") == "1",
)

app.permanent_session_lifetime = timedelta(hours=12)

CORS(
    app,
    supports_credentials=True,
    origins=os.environ.get("CORS_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500").split(",")
)

RUTAS_PUBLICAS = {"/", "/inicioSesion", "/login", "/logout", "/sesion",
                  "/addtendero", "/consultaCedulaTendero"}


@app.before_request
def exigir_sesion():
    """Bloquea todo endpoint no público sin sesión vigente y fuerza que el
    tendero sea siempre el de la sesión, ignorando el que mande el cliente."""
    if request.method == "OPTIONS" or request.path in RUTAS_PUBLICAS             or request.path.startswith("/static/"):
        return None

    cedula = session.get("cedula")
    if not cedula:
        if request.path == "/dashboard":
            return redirect("/inicioSesion")
        return jsonify({"error": "Sesión no válida o expirada"}), 401

    datos = request.get_json(silent=True)
    if isinstance(datos, dict):
        datos["idTendero"] = cedula
        if "cedulaTendero" in datos:
            datos["cedulaTendero"] = cedula
    return None


cargar_rutas_operaciones(app)
cargar_rutas_clientes(app)
cargar_rutas_Tenderos(app)
cargar_rutas_estadisticas(app)
cargar_rutas_inventario(app)
cargar_ruta_abonos(app)
cargar_rutas_sesion(app)

if __name__== '__main__':
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "4000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )