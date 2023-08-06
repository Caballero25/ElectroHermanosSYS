document.getElementById("botonRegresar").addEventListener("click", function(event) {
    event.preventDefault(); // Evitar que el enlace realice su acción predeterminada
        
    // Regresar a la página anterior
    history.back();
});

