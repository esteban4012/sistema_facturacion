$(document).ready(function() {
    $('.eliminar-factura').click(function(event) {
        event.preventDefault();
        var url = $(this).attr('href');
        if (confirm('¿Seguro que quieres eliminar esta factura?')) {
            window.location.href = url;
        }
    });
});
