document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessages = document.getElementById('errorMessages');

    form.addEventListener('submit', function(event) {
        errorMessages.innerHTML = ''; // Limpiar mensajes de error

        // Validación del correo
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value)) {
            event.preventDefault();
            errorMessages.innerHTML += '<p>Por favor, ingresa un correo válido.</p>';
        }

        // Validación de la contraseña
        const password = passwordInput.value;
        const passwordRegex = /^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*\d).{8,}$/;
        if (!passwordRegex.test(password)) {
            event.preventDefault();
            errorMessages.innerHTML += '<p>La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, un número y un carácter especial.</p>';
        }
    });
});