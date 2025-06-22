from flask import Flask, render_template, request, redirect, url_for
from backend.glc import AnalizadorGramaticaVisual
import json
import random

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

@app.route('/', methods=['GET'])
def formulario():
    # Solo mostrar el formulario
    return render_template('index.html')

@app.route('/generar_arbol', methods=['POST'])
def generar_arbol():
    cadena = request.form.get('cadena', '').strip()

    analizador = AnalizadorGramaticaVisual(auto_abrir=False)

    if analizador.procesar_cadena(cadena):
        analizador.construir_arbol()
        analizador.generar_proceso_desde_arbol()
        
        # IMPORTANTE: Generar el archivo JS actualizado para esta cadena específica
        analizador.visualizador.visualizar_arbol(analizador.arbol)
        
        arbol = analizador.arbol
        derivaciones = analizador.proceso_arbol
        
        # Renderizar la página arbol.html con los datos
        return render_template(
            'arbol.html',
            cadena=cadena,
            arbol=json.dumps(arbol, ensure_ascii=False),
            derivaciones=derivaciones
        )
    else:
        # Si la cadena es inválida, redirigir de nuevo al formulario o mostrar error
        return redirect(url_for('formulario'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)