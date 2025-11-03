/**
 * Proyecto: Carnes del Rancho
 * Archivo: validate.js (fragmento de manejo de formularios)
 * Autor de documentación: Tatiana Matías Jiménez
 * Descripción: Script que captura el envío de formularios con clase `.php-email-form`,
 *              gestiona reCAPTCHA (si está configurado), envía los datos por fetch (AJAX)
 *              al endpoint PHP indicado en `action`, y muestra estados de carga, error y éxito.
 */

(function () {
  "use strict";// Activa modo estricto para evitar errores silenciosos y malas prácticas.

// Selecciona todos los formularios que usen la clase .php-email-form
  let forms = document.querySelectorAll('.php-email-form');

// Recorre cada formulario encontrado
  forms.forEach( function(e) {
    // Escucha el evento 'submit' del formulario
    e.addEventListener('submit', function(event) {
      event.preventDefault();// Evita el envío tradicional (recarga de página)

      let thisForm = this;// Referencia al formulario actual

      // Lee el atributo 'action' (URL del endpoint PHP que procesará el formulario)
      let action = thisForm.getAttribute('action');
      // Lee la posible llave de sitio de reCAPTCHA (si el formulario la declara)
      let recaptcha = thisForm.getAttribute('data-recaptcha-site-key');

      // Si no hay action, no se puede enviar: muestra error y termina
      if( ! action ) {
        displayError(thisForm, 'No se pudo enviar el formulario en este momento. Por favor, inténtalo de nuevo más tarde.');
        return;
      }

      // Cambia estados visuales: muestra "loading" y oculta mensajes previos de error/éxito
      thisForm.querySelector('.loading').classList.add('d-block');
      thisForm.querySelector('.error-message').classList.remove('d-block');
      thisForm.querySelector('.sent-message').classList.remove('d-block');

      // Empaqueta los datos del formulario en un objeto FormData (incluye inputs, selects, textarea, etc.)
      let formData = new FormData( thisForm );

      // Si el formulario requiere reCAPTCHA
      if ( recaptcha ) {
        // Verifica que la librería grecaptcha esté cargada
        if(typeof grecaptcha !== "undefined" ) {
          // Ejecuta reCAPTCHA de forma asíncrona
          grecaptcha.ready(function() {
            try {
              // Solicita el token para la acción 'php_email_form_submit'
              grecaptcha.execute(recaptcha, {action: 'php_email_form_submit'})
              .then(token => {
                // Inserta el token de reCAPTCHA en el FormData antes de enviar
                formData.set('recaptcha-response', token);
                // Llama a la función que realiza el envío por fetch
                php_email_form_submit(thisForm, action, formData);
              })
            } catch(error) {
              // Si falla algo al ejecutar reCAPTCHA, muestra el error
              displayError(thisForm, error);
            }
          });
        } else {
          // Si no cargó la API de reCAPTCHA, muestra error
          displayError(thisForm, 'No se pudo verificar la seguridad del formulario. Recarga la página e inténtalo de nuevo.')
        }
      } else {
        // Si no hay reCAPTCHA, envía directamente
        php_email_form_submit(thisForm, action, formData);
      }
    });
  });

    /**
   * Envía el formulario usando fetch (AJAX) al endpoint indicado en `action`.
   * Muestra mensajes según el resultado:
   *  - OK (texto exactamente 'OK'): éxito, limpia el formulario y muestra mensaje de enviado.
   *  - Cualquier otro texto o error HTTP: muestra mensaje de error.
   */

  function php_email_form_submit(thisForm, action, formData) {
    fetch(action, {
      method: 'POST',                         // Método POST para enviar los datos
      body: formData,                        // Cuerpo del request: los datos del formulario
      headers: {'X-Requested-With': 'XMLHttpRequest'}     // Cabecera para indicar que es una solicitud AJAX
    })
    .then(response => {
      // Si la respuesta es correcta en el llenado del formulario, continúa; de lo contrario muestra un error.
      if( response.ok ) {
        return response.text();
      } else {
        throw new Error("Ha ocurrido un error en el servidor. Por favor, inténtalo de nuevo más tarde.");
      }
    })
    .then(data => {
      // Quita el estado de "cargando"
      thisForm.querySelector('.loading').classList.remove('d-block');
      // Convención: si el servidor responde exactamente 'OK', se considera envío exitoso
      if (data.trim() == 'OK') {
        thisForm.querySelector('.sent-message').classList.add('d-block');   // Muestra mensaje de éxito
        thisForm.reset();   // Limpia todos los campos del formulario
      } else {
        // Si no vino 'OK', lanza error con el contenido recibido o un mensaje genérico
        throw new Error(data ? data : 'El envío del formulario falló y no se recibió un mensaje de error desde: ' + action);
      }
    })
    .catch((error) => {
      // Cualquier error en la cadena (HTTP, red, lógica, reCAPTCHA, etc.) se muestra al usuario
      displayError(thisForm, error);
    });
  }

    /**
   * Muestra un mensaje de error en el formulario actual:
   * Función de mecanismo para mostrar errores
   * - Oculta "cargando"
   * - Inyecta el texto del error en .error-message
   * - Muestra el bloque de error
   */

  function displayError(thisForm, error) {
    thisForm.querySelector('.loading').classList.remove('d-block');      // Asegura ocultar "cargando"
    thisForm.querySelector('.error-message').innerHTML = error;          // Inserta detalle del error
    thisForm.querySelector('.error-message').classList.add('d-block');  // Lo hace visible
  }

})();// IIFE: se autoejecuta para no contaminar el ámbito global BORRAR ESTO “IIFE: se autoejecuta para no contaminar el ámbito global” significa que este patrón protege tu código, lo encapsula y lo ejecuta en cuanto el navegador lo lee.
