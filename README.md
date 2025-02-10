# J2Py


Py2J es una herramienta desarrollada en Python para la conversión de código Java a Python. Permite a los usuarios ingresar código Java directamente en la interfaz o cargar archivos `.java` para su conversión. Actualmente, el proyecto se encuentra en sus primeras etapas y **solo incluye la funcionalidad de análisis léxico**. En el futuro, se planea implementar el análisis sintáctico y la generación de código Python completo.

## Tabla de Contenidos

*   [Características](#características)
*   [Instalación](#instalación)
*   [Uso](#uso)
*   [Roadmap](#roadmap)
*   [Contribución](#contribución)
*   [Licencia](#licencia)

## Características

*   **Análisis Léxico:** Implementación inicial del análisis léxico para código Java.
*   **Interfaz Gráfica:** Interfaz de usuario para ingresar y convertir código Java.
*   **Carga de Archivos:** Permite cargar archivos `.java` para su análisis.

## Instalación

Para descargar el repositorio, ejecuta el siguiente comando (o descarga mediante la interfaz de GitHub):

```bash
git clone https://github.com/alemt19/java-compiler
```

Luego, instala las librerías necesarias para el funcionamiento del programa usando el siguiente comando (de forma global o en un entorno virtual):

```bash
pip install PyQt6 PyQt6-WebEngine ply
```

## Uso

1.  Ejecuta el archivo `main.py` para iniciar el programa.
2.  Elige el archivo `.java` a convertir (o escribe el código directamente en la interfaz).
3.  Usa el botón para iniciar la conversión.
4.  Revisa el resultado del análisis léxico en la interfaz.

## Roadmap

*   [ ] Implementación del análisis sintáctico.
*   [ ] Implementación del análisis semántico.
*   [ ] Generación de código Python completo.
*   [ ] Mejora de la interfaz de usuario.

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
