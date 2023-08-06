var modal = document.getElementById('miModal');
var btnSi = document.getElementById('confirmarSi');
var btnNo = document.getElementById('confirmarNo');
var form = document.querySelector('#formulario form'); // Capturamos el formulario dentro del div

form.addEventListener('submit', function(event) {
  event.preventDefault(); // Evita que el formulario se envíe inmediatamente
  modal.style.display = 'block';
});

btnSi.addEventListener('click', function() {
  modal.style.display = 'none';
  form.submit(); // Envía el formulario
});

btnNo.addEventListener('click', function() {
  modal.style.display = 'none';
});
