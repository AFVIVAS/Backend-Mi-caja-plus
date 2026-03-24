from flask import request,jsonify 
from models.operaciones import Operaciones
from models.clientes import Clientes
from models.creditos import Creditos
from models.inventario import Inventario

def cargar_rutas_operaciones(app):
    
    # probar si sirve

    @app.route("/crearventas", methods=["POST"])
    def crear_venta():
        try:
            venta = request.get_json()
            print(f"datos Venta {venta}")
            inventarioModel = Inventario()
            resultadoInv = inventarioModel.obtenerPrecio(venta)
            if resultadoInv:
                precioUnitario = resultadoInv['valorVenta']
                cantidad = venta['cantidad']
                venta['valor'] = precioUnitario * cantidad
                tipoPago=venta['tipoPago']
                if cantidad > 0:                
                    if tipoPago == "credito":
                        cedulaCliente=venta['cedulaCliente']
                        cedulaTendero=venta['idTendero']
                        clienteModel=Clientes()
                        resultadoCliente=clienteModel.ConsultarClientes(cedulaCliente,cedulaTendero)
                        if resultadoCliente:
                            ventaModel = Operaciones()
                            resultadoVenta=ventaModel.insertar_venta(venta)
                            if resultadoVenta > 0:
                                idVenta=resultadoVenta['idVenta']
                                idCliente=resultadoCliente['idCliente']
                                creditoModel= Creditos()
                                resultadoCredito=creditoModel.insertar_credito(idVenta,idCliente)
                                if resultadoCredito > 0:
                                    return jsonify({"exitoso":"credito exitoso"}),201
                                else:
                                    return jsonify({"exito":"ocurrio un problema en el credito"}),400
                            else:
                                return jsonify({"exito":"no se pudo registrar la venta"}),400
                        else:
                            return jsonify({"exito":"cliente no registrado"}),400
                    else:
                        ventaModel = Operaciones()
                        resultadoVenta=ventaModel.insertar_venta(venta)
                        if resultadoVenta > 0:
                            return jsonify ({"exito": True, "total": venta['valor']}),201
                        
                        else:
                            return jsonify({"error": "error venta"}),500
                else:
                    return jsonify({"error":"no hay stock"}),404   
            else:
                return jsonify({"error":"fallo inventario"}) ,400        
                            
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error": "error interno"}), 500
        
    @app.route("/registrar_credito", methods = ['POST'])
    def registrar_credito():
        try:

            data = request.get_json()

            print(data)

            nombre = data['nombre']

            presentacion = data['presentacion']

            cantidad = data['cantidad']

            cedulaTendero = data['idTendero']

            cedulaCliente = data['cedula']

            mensaje = data["mensaje"]

            inventario = Inventario()

            sinonimo = inventario.buscarSinonimoProducto(data)

            if sinonimo :

                nombre = sinonimo["nombre"]

            producto_inventario = inventario.buscarProducto(cedulaTendero,nombre,presentacion)


            if producto_inventario:

                cantidad_stock = producto_inventario["cantidad"]

                if cantidad > cantidad_stock:

                    return jsonify("La cantidad de venta es mayor a la cantidad en stock. Por favor actualice el inventario.")

                else:

                    cantidad_total = cantidad_stock - cantidad

                    producto = {"cantidad": cantidad_total, "idInventario": producto_inventario["idInventario"]}

                    inventario.actualizarUnidades(producto, "descontar")

                    data["valor"] = producto_inventario["valorVenta"] * cantidad  

                    operacion = Operaciones()

                    venta = operacion.insertar_venta(data)

                    if venta:

                        creditoModel= Creditos()

                        cliente = Clientes()

                        resultado_cliente = cliente.ConsultarClientes(data)

                        idCliente = int(resultado_cliente["idCliente"])

                        creditoModel.insertar_credito(int(venta), int(idCliente))

                        saldo = creditoModel.aumentar_saldo(data,idCliente)

                        if saldo == True:

                            return jsonify("La venta a crédito ha sido registrado con éxito. ¿Algo más? para finalizar di fin.")

                        else:

                            return jsonify("Ha ocurrido un error. Intentelo de nuevo.")

                    else:

                        return jsonify("Ha ocurrido un error a la hora de registrar la venta por favor intentelo de nuevo.")

            else:

                return jsonify("El producto no esta registrado. Por favor agregalo al inventario. Para finalizar el crédito di fin.")

        except Exception as e:
            print(f"Error detectado: {e}")
    # SIEMPRE usa str(e) para que jsonify funcione
        return jsonify({"Error interno": str(e)}), 500
    
    @app.route("/crearcosto", methods=["POST"])
    def crear_costo():
        try:
            costo = request.get_json()
            idTendero = costo.get('idTendero')
            nombre = costo.get('nombre')
            presentacion = costo.get('presentacion')
            cantidadStock = int(costo.get('cantidadStock', 0))
            proveedor = costo.get('proveedor')

            inventario_model = Inventario()
            productoInventario = inventario_model.buscarProducto(idTendero, nombre, presentacion)

            if not productoInventario:
                return jsonify({"error": "producto no existente en el inventario, por favor agregue primero el producto antes de registrar la compra de mercancía"}), 404

            precio_compra_unitario = int(productoInventario.get('valorCompra', 0))
            total_costo = precio_compra_unitario * cantidadStock
            mensaje_historial = f"Compra de {cantidadStock} {presentacion} de {nombre}"

            data_costo = {
                'idTendero': idTendero,
                'mensaje': mensaje_historial,
                'precioCompra': total_costo, 
                'proveedor': proveedor
        }

            costo_model = Operaciones()
            resultado = costo_model.insertar_costo(data_costo)

            if resultado > 0:
                cantidad_actual = int(productoInventario.get('cantidad', 0))
                productoInventario['cantidad'] = cantidad_actual + cantidadStock
                inventario_model.actualizarUnidades(productoInventario, "agregar")
            
                return jsonify({"exito": True}), 201
            else:
                return jsonify({"error": "no se logro registrar"}), 500

        except Exception as e:
            print(f"error crítico en crearcosto: {e}")
        return jsonify({"error": "error interno"}), 500
        
    @app.route("/creargasto", methods=["POST"])    
    def crear_gasto():
        try:
            gasto=request.get_json()
            gasto_model=Operaciones()
            resultado=gasto_model.insertar_gasto(gasto)

            if resultado==1:
                return jsonify({"exito":True}),201
            else:
                return jsonify({"error":"no se logro registrar"}),500
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error":"error interno"}),500
        

    @app.route("/agregarBase", methods= ["POST"])
    def agregarBase():
        try:
            base = request.get_json()
            print(f"La base inicial es de {base}")
            base_model = Operaciones()
            resultado=base_model.insertarBase(base)
            if resultado > 0:
                return jsonify({"exito":True}),201
            else:
                return jsonify({"no se logro registrar"}),500
        except Exception as e:
            print(f"error: {e}")
            return jsonify({"error interno"}),500
            
    @app.route("/cantidadProducto", methods= ["POST"])
    def cantidadProducto():
        try:
            conexion = request.get_json()
            modelCantidad= Inventario()
            cantidad = conexion.get('cantidad')
            resultado = modelCantidad.obtenerPrecio(conexion)
            precioUnitario = resultado['cantidad']
            
            if precioUnitario >= cantidad:
                return jsonify({"exito": True}),200
            else:
                return jsonify({"error": False}),500
            
        except Exception as e:
            return jsonify({"Error": e}),500