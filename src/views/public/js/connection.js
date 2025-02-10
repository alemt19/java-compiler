
window.onload = function() {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.pyObject = channel.objects.pyObject;
    });
};

function analisisLexico(input) {
    let codigo = "";
    if (input === "textarea") {
        codigo = document.querySelector('.input').innerHTML;
    }
    else if (input === "archivo") {
        archivos = document.querySelector('.input').files;
        if (archivos.length > 0) {
            const lector = new FileReader();
    
            lector.onload = () => {
                document.querySelector('.output').innerText = (archivos[0]);
                const contenido = archivos[0].result;
                codigo = contenido; 
            };
    
            lector.onerror = function(e) {
                document.querySelector('.output').innerText = ("Error al leer el archivo:", e);
            };
    
            lector.readAsText(archivos[0]); // Leer el archivo como texto
        }
        else {
            document.querySelector('.output').innerText = "No se ha seleccionado un archivo";
            return;
        }
    
    }
    pyObject.analisisLexicoJS(codigo, (respuesta) => {
        agregarRespuesta(`Análisis léxico:\n${respuesta}`);
    });
}

function recibirDesdePython(mensaje) {
    agregarRespuesta(`Mensaje push: ${mensaje}`);
}

function agregarRespuesta(texto) {
    document.querySelector('.output').innerHTML = texto;
}

function borrarInput() {
    document.querySelector('.input').innerText = '';
}