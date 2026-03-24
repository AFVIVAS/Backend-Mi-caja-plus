function iniciarSesion(){
    const formulario=document.getElementById("formulario");
    const cedula_tendero=document.getElementById("cedula_tendero");
    const telefono_tendero=document.getElementById("telefono_tendero");

    const validarNumeros=(liberacion)=>{
        const campo=liberacion.target;

        if(/[^0-9]/.test(campo.value)){
            campo.setCustomValidity("Solo se permiten números.");
            campo.reportValidity();
            campo.value = campo.value.slice(0, -1);
        }else{
            campo.setCustomValidity("");
        }
    };

    cedula_tendero.addEventListener("keyup", validarNumeros);
    telefono_tendero.addEventListener("keyup", validarNumeros);

    formulario.addEventListener("submit",(envio)=>{
        envio.preventDefault();

        const mensajeError=document.getElementById("mensaje");
        if(mensajeError) mensajeError.textContent = "";

        let url = "/login";
        let data = {
            cedula: cedula_tendero.value,
            telefono: telefono_tendero.value        
        };
        fetch(url,{method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json",}    
        })
        .then((res)=>{
            if (!res.ok && res.status !== 400 && res.status !== 401) {
            }
            return res.json();
        })
        .then((response)=>{
            const cajaError=document.getElementById("mensaje");
            if (response.error){
                cajaError.textContent="Credenciales incorrectas. Verifica tus datos.";
            }else{
                const datosUsuario={cedula:response.cedula,
                    fechaCreacion: response.fechaCreacion,
                    nombre: response.nombre
                };
                sessionStorage.setItem("usuarioMiCaja", JSON.stringify(datosUsuario));
                formulario.reset(); 
                window.location.href="/dashboard";
            }
        })
        .catch((error)=> {
            console.error("Ha ocurrido un fallo de red:", error);
            if (cajaError) {
                cajaError.textContent = "Error de conexión. Intenta más tarde.";
            }
        });
    });
}
document.addEventListener("DOMContentLoaded",(evento_ppal)=>{
    if(document.getElementById("formulario")){
        iniciarSesion()
    }
});