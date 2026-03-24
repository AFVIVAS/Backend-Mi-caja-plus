function iniciarSesion(){
    const formulario=document.getElementById("formulario");
    const cedula_tendero=document.getElementById("cedula_tendero");
    const telefono_tendero=document.getElementById("telefono_tendero");

    const validarNumeros=(liberacion)=>{
        const campo=liberacion.target;

        if(/[^0-9]/.test(campo.value)){
            campo.setCustomValidity("Solo se permiten números.");

            campo.reportValidity();
        }else{
            campo.setCustomValidity("");
        }
    };

    cedula_tendero.addEventListener("keyup", validarNumeros);
    telefono_tendero.addEventListener("keyup", validarNumeros);

    formulario.addEventListener("submit",(envio)=>{
        envio.preventDefault();

        let url = "/login"
        let data = {
            cedula: cedula_tendero.value,
            telefono: telefono_tendero.value        
        };
        fetch(url,{
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json",
            }    
        })
        .then((res)=>res.json())
        .catch((error)=> console.error("Ha ocurrido el error:",error))
        .then((response)=>{

            const cajaError=document.getElementById("mensaje");

            if (response.error){
                cajaError.textContent="Credenciales incorrectas. Verifica tus datos.";
            }else{
                window.location.href="/panel";
            }
        })
    })
}

document.addEventListener("DOMContentLoaded",(evento_ppal)=>{
    if(document.getElementById("formulario")){
        iniciarSesion()
    }
});
