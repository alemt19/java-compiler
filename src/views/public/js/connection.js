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
    }
    else if (input === "archivo") {
        archivo = document.querySelector('#input').files[0];
        if (archivo) {
            const lector = new FileReader();
    
            lector.onload = function(e) {
                pyObject.analisisLexicoJS(e.target.result, (respuesta) => {
                    agregarRespuesta(`Análisis léxico:\n${respuesta}`);
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

function recibirDesdePython(mensaje) {
    agregarRespuesta(`Mensaje push: ${mensaje}`);
}

function agregarRespuesta(texto) {
    document.querySelector('#output').innerHTML = texto;
}

function borrarInput() {
    document.querySelector('#input').innerText = '';
}