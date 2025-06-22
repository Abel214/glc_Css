import os

class VisualizadorArbol:
    def __init__(self):
        # Cambiar la ruta para apuntar al directorio static
        self.url_js = os.path.join("frontend", "static", "js", "arbol.js")
        self.contador_nodos = 0
        self.nodos_js = []
        self.edges_js = []

    def generar_nodos_edges(self, nodo, padre_id=None):
        nodo_id = self.contador_nodos
        self.contador_nodos += 1
        simbolo = nodo['symbol']
        color = self._obtener_color_nodo(simbolo)

        nodo_js = {
            'id': nodo_id,
            'label': simbolo,
            'color': color,
            'font': {'size': 16, 'color': 'white' if simbolo in ['E', 'T', 'F'] else 'black'},
            'shape': 'circle' if simbolo in ['E', 'T', 'F'] else 'box'
        }
        self.nodos_js.append(nodo_js)
        
        if padre_id is not None:
            edge_js = {
                'from': padre_id,
                'to': nodo_id,
                'arrows': 'to',
                'color': {'color': '#2B7CE9'},
                'width': 2
            }
            self.edges_js.append(edge_js)
        
        for hijo in nodo.get('children', []):
            self.generar_nodos_edges(hijo, nodo_id)

        return nodo_id

    def _obtener_color_nodo(self, simbolo):
        colores = {
            'E': '#FF6B6B',
            'T': '#4ECDC4',
            'F': '#45B7D1',
            '+': '#96CEB4',
            '*': '#FECA57',
            '(': '#DDA0DD',
            ')': '#DDA0DD',
            'id': '#A8E6CF'
        }
        return colores.get(simbolo, '#D3D3D3')

    def generar_archivo_js(self, arbol):
        # Resetear contadores para cada nuevo árbol
        self.contador_nodos = 0
        self.nodos_js = []
        self.edges_js = []
        
        # Generar los nodos y edges para el nuevo árbol
        self.generar_nodos_edges(arbol)
        
        # Construir el string de nodos
        nodes_str = "var nodes = new vis.DataSet([\n"
        for nodo in self.nodos_js:
            nodes_str += f"  {{ id: {nodo['id']}, label: \"{nodo['label']}\", "
            nodes_str += f"color: \"{nodo['color']}\", "
            nodes_str += f"font: {{ size: {nodo['font']['size']}, color: \"{nodo['font']['color']}\" }}, "
            nodes_str += f"shape: \"{nodo['shape']}\" }},\n"
        nodes_str += "]);\n\n"

        # Construir el string de edges
        edges_str = "var edges = new vis.DataSet([\n"
        for edge in self.edges_js:
            edges_str += f"  {{ from: {edge['from']}, to: {edge['to']}, "
            edges_str += f"arrows: \"{edge['arrows']}\", "
            edges_str += f"color: {{ color: \"{edge['color']['color']}\" }}, "
            edges_str += f"width: {edge['width']} }},\n"
        edges_str += "]);\n\n"

        # Configuración de vis.js
        config_str = """var container = document.getElementById("mynetwork");
var data = {
  nodes: nodes,
  edges: edges,
};
var options = {
  layout: {
    hierarchical: {
      direction: 'UD',        // Up-Down (de arriba hacia abajo)
      sortMethod: 'directed', // Ordenamiento dirigido
      levelSeparation: 150,   // Separación entre niveles
      nodeSpacing: 200,       // Espaciado entre nodos
      treeSpacing: 200,       // Espaciado entre árboles
      blockShifting: true,    // Permitir movimiento de bloques
      edgeMinimization: true, // Minimizar cruces de edges
      parentCentralization: true, // Centralizar padres
      shakeTowards: 'leaves'  // Sacudir hacia las hojas
    }
  },
  physics: {
    enabled: false // Desactivar física para mantener estructura jerárquica
  },
  nodes: {
    borderWidth: 2,
    borderWidthSelected: 3,
    chosen: true,
    shadow: {
      enabled: true,
      color: 'rgba(0,0,0,0.2)',
      size: 10,
      x: 3,
      y: 3
    }
  },
  edges: {
    smooth: {
      enabled: true,
      type: 'cubicBezier',
      forceDirection: 'vertical',
      roundness: 0.4
    }
  }
};

// Verificar que vis.js esté disponible
if (typeof vis === 'undefined') {
    document.getElementById('mynetwork').innerHTML = 
        '<div style="padding: 50px; text-align: center; color: red; font-size: 18px;">' +
        '❌ Error: La librería vis.js no se ha cargado correctamente.<br>' +
        '🔧 Verifica tu conexión a internet o descarga vis.js localmente.' +
        '</div>';
} else {
    try {
        var network = new vis.Network(container, data, options);
        console.log("✅ Red generada exitosamente");
    } catch (error) {
        console.error("❌ Error al crear la red:", error);
        document.getElementById('mynetwork').innerHTML = 
            '<div style="padding: 50px; text-align: center; color: red; font-size: 18px;">' +
            '❌ Error al generar la visualización: ' + error.message +
            '</div>';
    }
}"""

        contenido_completo = nodes_str + edges_str + config_str
        
        try:
            # Crear el directorio si no existe
            directorio = os.path.dirname(self.url_js)
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Escribir el archivo JavaScript actualizado
            with open(self.url_js, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_completo)
            
            print(f"✅ Archivo {self.url_js} generado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error al generar archivo: {e}")
            return False

    def visualizar_arbol(self, arbol):
        return self.generar_archivo_js(arbol)

    def verificar_dependencias(self):
        archivos_necesarios = [self.url_js]
        for archivo in archivos_necesarios:
            if os.path.exists(archivo):
                print(f"✅ {archivo} encontrado")
            else:
                print(f"❌ {archivo} no encontrado")

        print("💡 El archivo vis.js se carga desde CDN (requiere internet)")
        return True