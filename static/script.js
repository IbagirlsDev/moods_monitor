
function redirectToLogin() {
    window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');

    const emotionOptionsContainer = document.getElementById('emotion-options-container');
    const emotionOptionsSelect = document.getElementById('emotion-options');
    const reasonTextarea = document.getElementById('reason');
    const otherReasonContainer = document.getElementById('other-reason-container');

    const emotions = {
        1: ['Reconocimiento formal por un desempeño sobresaliente', 'Superación de un reto profesional importante.', 'Promoción o nueva oportunidad laboral.', 'Logro de un objetivo personal significativo (ej., graduación, meta financiera).', 'Relaciones interpersonales fortalecidas gracias a la comunicación efectiva.', 'Otro'],
        2: ['Falta de alineación con la misión o valores de la organización.', 'Sensación de estancamiento profesional o ausencia de crecimiento.', 'Pérdida de un proyecto importante debido a decisiones externas.', 'Desequilibrio entre la vida laboral y personal que afecta la salud emocional.', 'Dificultades para manejar cambios o transiciones personales.', 'Otro'],
        3: ['Percepción de trato injusto en el lugar de trabajo.', 'Falta de comunicación efectiva dentro del equipo.', 'Sensación de desorganización en procesos laborales que genera frustración.', 'Incapacidad para desconectarse del trabajo en momentos de descanso personal.', 'Frustración por no lograr balancear responsabilidades familiares y laborales.', 'Otro'],
        4: ['Sobrecarga por la asignación constante de tareas adicionales sin redistribución.', 'Participación en reuniones o actividades poco productivas que desgastan el tiempo.', 'Ausencia de programas de bienestar para apoyar el descanso del equipo.', 'Falta de planificación en la rutina diaria que ocasiona agotamiento continuo.', 'Dificultad para establecer límites entre tiempo laboral y personal.', 'Otro'],
        5: ['Falta de claridad en los roles y responsabilidades dentro del equipo.', 'Cambios en las metas organizacionales sin previo aviso o consulta.', 'Inexperiencia en el manejo de nuevas herramientas tecnológicas introducidas sin capacitación.', 'Dudas sobre decisiones importantes relacionadas con el desarrollo personal o profesional.', 'Sensación de inseguridad frente a cambios imprevistos en la rutina diaria.', 'Otro']
    };

    // Lógica para mostrar el textarea cuando se selecciona "Otro"
    emotionOptionsSelect.addEventListener('change', function () {
        if (emotionOptionsSelect.value === 'Otro') {
            otherReasonContainer.style.display = 'block'; // Muestra el contenedor del textarea
            reasonTextarea.setAttribute('required', 'required'); // Hace que el textarea sea obligatorio
        } else {
            otherReasonContainer.style.display = 'none'; // Oculta el contenedor
            reasonTextarea.removeAttribute('required'); // Elimina el requisito de que sea obligatorio
        }
    })

    // Lógica de actualización de opciones de emoción
    document.querySelectorAll('input[name="emoji"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            const selectedEmotion = this.value;
            updateEmotionOptions(selectedEmotion);
        });
    });

    function updateEmotionOptions(emotion) {
        while (emotionOptionsSelect.firstChild) {
            emotionOptionsSelect.removeChild(emotionOptionsSelect.firstChild);
        }

        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Seleccione una opción';
        emotionOptionsSelect.appendChild(defaultOption);

        emotions[emotion].forEach(function (optionText) {
            const option = document.createElement('option');
            option.value = optionText;
            option.textContent = optionText;
            emotionOptionsSelect.appendChild(option);
        });

        emotionOptionsContainer.style.display = 'block';
    }

    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            if (!validateRegisterForm()) {
                event.preventDefault();
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            if (!validateLoginForm()) {
                event.preventDefault();
            }
        });
    }

    if (moodForm) {
        moodForm.addEventListener('submit', function (event) {
            if (!validateMoodForm()) {
                event.preventDefault();
            }
        });
    }

    function validateRegisterForm() {
        const firstName = document.getElementById('first_name').value.trim();
        const lastName = document.getElementById('last_name').value.trim();
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!firstName || !lastName || !username || !email || !password) {
            alert('Por favor, complete todos los campos.');
            return false;
        }

        if (!email || !validateEmail(email)) {
            alert('Por favor, ingrese un correo electrónico válido.');
            return false;
        }
    
        if (!password || !validatePassword(password)) {
            alert('La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, minúsculas, números y caracteres especiales.');
            return false;
        }

        return true;
    }

    function validateLoginForm() {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            alert('Por favor, complete todos los campos.');
            return false;
        }

        return true;
    }

    function validateMoodForm() {
        const email = document.getElementById('email').value.trim();       
        const emojiSelected = document.querySelector('input[name="emoji"]:checked');
        const opcionSelected = document.getElementById('emotion-options').value.trim();

        if (!email || !emojiSelected || !opcionSelected) {
            alert('Por favor, complete todos los campos.');
            return false;
        }

        if (opcionSelected === 'Otro' && !reason) {
            alert('Por favor, explique su estado de ánimo si ha seleccionado "Otro".');
            return false;
        }

        if (!validateEmail(email)) {
            alert('Por favor, ingrese un correo electrónico válido.');
            return false;
        }

        return true;
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePassword(password) {
        const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
        return re.test(password);
    }
    

});

