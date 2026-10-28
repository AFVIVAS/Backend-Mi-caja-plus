document.addEventListener('DOMContentLoaded', () => {

    const btnMenu = document.getElementById('btnMenu');
    const cerrarMenu = document.getElementById('cerrarMenu');
    const menuLateral = document.getElementById('menuLateral');
    const formFiltros = document.getElementById('formFiltros');
    const btnLimpiar = document.getElementById('btnLimpiar');


    btnMenu.addEventListener('click', () => {
        if (menuLateral.classList.contains('menu-cerrado')) {
            menuLateral.classList.remove('menu-cerrado');
            menuLateral.classList.add('menu-abierto');
            console.log("Menú abierto");
        }
    });

    cerrarMenu.addEventListener('click', () => {
        menuLateral.classList.remove('menu-abierto');
        menuLateral.classList.add('menu-cerrado');
        console.log("Menú cerrado desde la X");
    });

    formFiltros.addEventListener('submit', async (e) => {
        e.preventDefault(); 

        const inputsFecha = formFiltros.querySelectorAll('input[type="date"]');
        let fInicialRaw = inputsFecha[0].value;
        let fFinRaw = inputsFecha[1].value;
        
        const idTendero = "66654633"; 

        if (!fInicialRaw || !fFinRaw) {
            alert("Por favor selecciona el rango de fechas completo.");
            return;
        }

    
        const fechaInicial = `${fInicialRaw} 00:00:00`;
        const fechaFin = `${fFinRaw} 23:59:59`;

        const dataEnviar = {
            idTendero: idTendero,
            fechaInicial: fechaInicial,
            fechaFin: fechaFin
        };

        console.log("Enviando datos a Python:", dataEnviar);

        try {
            const respuesta = await fetch('/consultarEstadisticas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataEnviar)
            });

            if (!respuesta.ok) throw new Error("Error en la respuesta del servidor");

            const datosRecibidos = await respuesta.json();
            console.log("Respuesta procesada:", datosRecibidos);


            if (datosRecibidos && datosRecibidos.length > 0) {
                actualizarTarjetas(datosRecibidos[0]);
                
                menuLateral.classList.remove('menu-abierto');
                menuLateral.classList.add('menu-cerrado');
            }

        } catch (error) {
            console.error("Error al consultar estadísticas:", error);
            alert("No se pudo conectar con el servidor de Python.");
        }
    });

    function actualizarTarjetas(res) {

        const vEfectivo = parseFloat(res.ventas) || 0;
        const vCredito = parseFloat(res.valorCredito) || 0;
        const totalVentas = vEfectivo + vCredito; 
        
        const costos = parseFloat(res.costos) || 0;
        const gastos = parseFloat(res.gastos) || 0;
        const nFiados = res.ncreditos || 0;


        document.querySelector('#tarjetaUno p').textContent = `$${totalVentas.toLocaleString()}`;
        document.querySelector('#tarjetaDos p').textContent = `$${costos.toLocaleString()}`;
        document.querySelector('#tarjetaTres p').textContent = `$${gastos.toLocaleString()}`;
        document.querySelector('#tarjetaCuatro p').textContent = nFiados;


        const utilidad = totalVentas - costos - gastos;
        const txtUtilidad = document.getElementById('nUtilidad');
        
        txtUtilidad.textContent = `$${utilidad.toLocaleString()}`;

        txtUtilidad.style.color = utilidad < 0 ? "#FF5252" : "#2E7D32";
        
        console.log("Interfaz actualizada con éxito.");
    }


    btnLimpiar.addEventListener('click', () => {
        const tarjetasP = document.querySelectorAll('.tarjetas p');
        tarjetasP.forEach(p => p.textContent = "$0");
        document.getElementById('nUtilidad').textContent = "$0";
        document.getElementById('nUtilidad').style.color = "black";
        formFiltros.reset(); // Limpia los calendarios
    });
});