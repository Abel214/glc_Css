import webbrowser
import os
from backend.logicaArbol import VisualizadorArbol


class AnalizadorGramatica:
    def __init__(self):
        self.tokens = []
        self.proceso = []
        self.proceso_arbol = []
        self.arbol = {'symbol': 'E', 'children': []}

    def tokenizar(self, cadena):
        tokens = []
        i = 0
        while i < len(cadena):
            char = cadena[i]
            if char == ' ':
                i += 1
                continue
            if char in ['+', '*', '(', ')']:
                tokens.append(char)
                i += 1
            elif char == 'i' and i + 1 < len(cadena) and cadena[i + 1] == 'd':
                tokens.append('id')
                i += 2
            else:
                print(f"❌ Error: Carácter inválido '{char}' en posición {i}")
                return None
        return tokens

    def procesar_cadena(self, cadena):
        self.tokens = self.tokenizar(cadena)
        return self.tokens is not None

    def construir_arbol(self):
        self.arbol = self._construir_nodo_arbol(''.join(self.tokens), 'E')

    def _construir_nodo_arbol(self, tokens, simbolo):
        nodo = {'symbol': simbolo, 'children': []}

        if simbolo == 'E':
            if '+' in tokens:
                pos = self._encontrar_operador_principal(tokens, '+')
                if pos != -1:
                    # E → E + T
                    nodo['children'] = [
                        self._construir_nodo_arbol(tokens[:pos], 'E'),
                        {'symbol': '+', 'children': []},
                        self._construir_nodo_arbol(tokens[pos + 1:], 'T')
                    ]
                else:
                    # E → T
                    nodo['children'] = [self._construir_nodo_arbol(tokens, 'T')]
            else:
                # E → T
                nodo['children'] = [self._construir_nodo_arbol(tokens, 'T')]

        elif simbolo == 'T':
            if '*' in tokens:
                pos = self._encontrar_operador_principal(tokens, '*')
                if pos != -1:
                    # T → T * F
                    nodo['children'] = [
                        self._construir_nodo_arbol(tokens[:pos], 'T'),
                        {'symbol': '*', 'children': []},
                        self._construir_nodo_arbol(tokens[pos + 1:], 'F')
                    ]
                else:
                    # T → F
                    nodo['children'] = [self._construir_nodo_arbol(tokens, 'F')]
            else:
                # T → F
                nodo['children'] = [self._construir_nodo_arbol(tokens, 'F')]

        elif simbolo == 'F':
            if tokens.startswith('(') and tokens.endswith(')'):
                # F → (E)
                nodo['children'] = [
                    {'symbol': '(', 'children': []},
                    self._construir_nodo_arbol(tokens[1:-1], 'E'),
                    {'symbol': ')', 'children': []}
                ]
            else:
                # F → id
                nodo['children'] = [{'symbol': 'id', 'children': []}]

        return nodo

    def _encontrar_operador_principal(self, tokens, operador):
        nivel = 0
        for i in range(len(tokens) - 1, -1, -1):
            char = tokens[i]
            if char == ')':
                nivel += 1
            elif char == '(':
                nivel -= 1
            elif char == operador and nivel == 0:
                return i
        return -1

    def generar_proceso_desde_arbol(self):
        self.proceso_arbol = []
        forma_sentencial = "E"
        self.proceso_arbol.append(forma_sentencial)
        self._generar_derivaciones_secuenciales(self.arbol, forma_sentencial)

    def _generar_derivaciones_secuenciales(self, nodo, forma_actual):
        if nodo['symbol'] not in ['E', 'T', 'F'] or not nodo['children']:
            return forma_actual
        if len(nodo['children']) == 1:
            hijo = nodo['children'][0]
            nueva_forma = forma_actual.replace(nodo['symbol'], hijo['symbol'], 1)
        else:
            lado_derecho = ' '.join([hijo['symbol'] for hijo in nodo['children']])
            nueva_forma = forma_actual.replace(nodo['symbol'], lado_derecho, 1)
        if nueva_forma != forma_actual:
            self.proceso_arbol.append(nueva_forma)
        forma_trabajo = nueva_forma
        for hijo in nodo['children']:
            if hijo['symbol'] in ['E', 'T', 'F']:
                forma_trabajo = self._generar_derivaciones_secuenciales(hijo, forma_trabajo)

        return forma_trabajo

    def imprimir_arbol(self, nodo, prefijo='', es_ultimo=True):
        simbolo = nodo['symbol']
        print(prefijo + ('└── ' if es_ultimo else '├── ') + simbolo)

        hijos = nodo['children']
        for i, hijo in enumerate(hijos):
            nuevo_prefijo = prefijo + ('    ' if es_ultimo else '│   ')
            self.imprimir_arbol(hijo, nuevo_prefijo, i == len(hijos) - 1)


class AnalizadorGramaticaVisual(AnalizadorGramatica):
    def __init__(self, auto_abrir=True):
        super().__init__()
        self.visualizador = VisualizadorArbol()
        self.auto_abrir = auto_abrir

    def abrir_html(self, archivo_html="arbol.html"):
        try:
            # Construir la ruta completa al archivo en la carpeta 'templates'
            ruta_completa = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates', archivo_html)

            # Verificar que el archivo existe
            if os.path.exists(ruta_completa):
                # Abrir en el navegador predeterminado
                webbrowser.open(f'file://{os.path.abspath(ruta_completa)}')

                return True
            else:
                print(f"❌ No se encontró el archivo {archivo_html}")
                return False
        except Exception as e:
            print(f"❌ Error al abrir el archivo: {e}")
            return False

    def mostrar_analisis(self, cadena):
        print(f"\n Analizando cadena: '{cadena}'")
        print("=" * 50)

        if not self.procesar_cadena(cadena):
            return False

        print(f" Tokens: {self.tokens}")
        print(f" Gramática:")
        print(f"   E → E + T | T")
        print(f"   T → T * F | F")
        print(f"   F → (E) | id")

        print("\n🌳 Árbol de Derivación:")
        self.construir_arbol()
        self.imprimir_arbol(self.arbol)

        print("\n🎯 Proceso de Derivación desde Árbol:")
        self.generar_proceso_desde_arbol()
        if self.proceso_arbol:
            for i, forma in enumerate(self.proceso_arbol):
                print(f"{i + 1:2}. {forma}")
        else:
            print("   No se encontraron derivaciones.")

        if self.visualizador.visualizar_arbol(self.arbol):
            if self.auto_abrir:
                self.abrir_html()
            else:
                print()
        else:
            print("❌ Error al generar visualización")

        return True

    def configurar_auto_abrir(self, activar=True):
        self.auto_abrir = activar
        estado = "activada" if activar else "desactivada"
        print()

#
#if __name__ == "__main__":
#    analizador = AnalizadorGramaticaVisual(auto_abrir=True)
#    print("Gramatica Libre De Contexto")
#    print("=" * 60)
    # Casos de prueba
#    casos_prueba = [
#        "(id)"
#    ]
#    for caso in casos_prueba:
#        analizador.mostrar_analisis(caso)
#       print("\n" + "-" * 40 + "\n")
