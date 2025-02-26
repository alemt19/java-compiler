window.onload = function() {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyObject = channel.objects.pyObject;
    });
};

function analisisLexico(input) {
    if (input === "textarea") {
        codigo = document.querySelector('#input').value;
        pyObject.analisisLexicoJS(codigo, (respuesta) => {
            agregarRespuesta(`Análisis léxico:\n${respuesta}`);

        });
        pyObject.analisisLexicoErroresJS((errores) => {
            agregarErrores(`${errores}`);
        });
    }
    else if (input === "archivo") {
        archivo = document.querySelector('#input').files[0];
        if (archivo) {
            const lector = new FileReader();
    
            lector.onload = function(e) {
                agregarCodigo(e.target.result);
                pyObject.analisisLexicoJS(e.target.result, (respuesta) => {
                    agregarRespuesta(`${respuesta}`);
                });
                pyObject.analisisLexicoErroresJS((errores) => {
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