from flask import request, jsonify,render_template,url_for,redirect,session
from models.tenderos import Tenderos
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError

hp=PasswordHasher(hash_len=32)

def cargar_rutas_Tenderos(app):

    @app.route("/")
    def index():
        return redirect(url_for("inicio"))
    
    @app.route("/inicioSesion")
    def inicio():
        return render_template("index.html")
        

    @app.route("/login", methods=["POST"])
    def login():
        try:
            
            data = request.get_json()
            cedula = data.get("cedula")
            telefono = data.get("telefono")
    

            if not cedula or not telefono:
                return jsonify({"error": "Faltan datos"}), 400

            tendero_model = Tenderos()
            usuario = tendero_model.validar_login(cedula)
            if not usuario:
                return jsonify({"error": "Credenciales incorrectas"}), 401
            try:
                hp.verify(usuario["llave"], telefono)
            except (VerificationError, InvalidHashError):
                return jsonify({"error":"Credenciales incorrectas"}), 401

            session.clear()
            session.permanent = True
            session['cedula'] = usuario["cedula"]
            session['nombre'] = usuario["nombre"]

            usuario.pop("llave", None)
            return jsonify(usuario), 200

        except Exception as e:
            print("Error en login:", e)
            return jsonify({"error": str(e)}), 500
        
    @app.route("/consultaCedulaTendero", methods=["POST"])
    def consultaTendero():
        try:
            data = request.get_json()
            print(data)
            cedula=data['cedula']
            if not cedula:
                return jsonify({"error":"Faltan datos"}),400
            modelTendero =  Tenderos()
            resultado = modelTendero.consultarCedulaTendero(cedula)
            if resultado:
                return jsonify (resultado)
            else:
                return jsonify({"mensaje": "Cédula disponible"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

    @app.route("/addtendero", methods=["POST"])
    def crear_tendero():
        try:
            data = request.get_json()
            cedula = data.get("cedula")
            telefono = data.get("telefono")
            nombre = data.get("nombre")

            if not cedula or not telefono or not nombre:
                return jsonify({"error": "Faltan datos"}), 400

            hash_telefono=hp.hash(telefono)

            tendero_model = Tenderos()
            resultado=tendero_model.crear_tendero(cedula,hash_telefono,nombre)
            if resultado==1:
                return jsonify({"mensaje": "Tendero creado"}), 200
            else:
                return jsonify({"error":"Error al crear"}),500

        except Exception as e:
            print("Error al crear tendero:", e)
            return jsonify({"error": "No se pudo crear el tendero"}), 500   
