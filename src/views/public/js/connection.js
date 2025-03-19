window.onload = function() {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyObject = channel.objects.pyObject;
    });
};

function ejecutar(input) {
    fase = document.querySelector('#fase').value;
    let generarRespuesta = null;
    let generarErrores = null;
    if (fase === "Léxico") {
        generarRespuesta = pyObject.analisisLexicoJS;
        generarErrores = pyObject.analisisLexicoErroresJS;
    }
    else if (fase === "Sintáxis") {
        generarRespuesta = pyObject.analisisSintacticoJS;
        generarErrores = pyObject.analisisSintacticoErroresJS;
    }
    
    if (input === "textarea") {
        codigo = document.querySelector('#input').value;
        generarRespuesta(codigo, (respuesta) => {
            agregarRespuesta(`${respuesta}`);

        });
        generarErrores((errores) => {
            agregarErrores(`${errores}`);
        });
    }
    else if (input === "archivo") {
        archivo = document.querySelector('#input').files[0];
        if (archivo) {
            const lector = new FileReader();
    
            lector.onload = function(e) {
                agregarCodigo(e.target.result);
                generarRespuesta(e.target.result, (respuesta) => {
                    agregarRespuesta(`${respuesta}`);
                });
                generarErrores((errores) => {
                    agregarErrores(`${errores}`);
                });
            };
            
            lector.readAsText(archivo, 'UTF-8'); // Especifica codificación

        }
        else {
            document.querySelector('#output').innerText = "No se ha seleccionado un archivo";
            return;
        }
    
    }
}

function agregarRespuesta(texto) {
    document.querySelector('#output').innerHTML = texto;
}

function agregarErrores(texto) {
    document.querySelector('#console').innerHTML = texto;
}

function agregarCodigo(texto) {
    document.querySelector('#code').innerHTML = texto;
}

function borrarInput() {
    document.querySelector('#input').innerText = '';
}