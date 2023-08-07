$(document).ready(function () {
    $("#despedirEmpleado").click(function (e) {
        e.preventDefault();
        $("#despedirModal").modal("show");

        $("#confirmAction").click(function () {
            window.location.href = $(this).attr("href");
        });
    });
});

$(document).ready(function () {
    $("#recontratarEmpleado").click(function (e) {
        e.preventDefault();
        $("#recontratarModal").modal("show");

        $("#confirmAction").click(function () {
            window.location.href = $(this).attr("href");
        });
    });
});


