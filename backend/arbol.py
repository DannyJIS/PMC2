import heapq
from collections import Counter
import graphviz # type: ignore
import os
from nodo import NodoHuffman

class ArbolHuffman:
    def __init__(self):
        self.raiz = None
        self.codigos = {}
        self.texto_original = ""
        
    def generar_arbol(self, texto):
        self.texto_original = texto
        
        # cuenta las frecuencias de cada caracter
        frecuencias = Counter(texto)
        
        # Crea un nodo para cada caracter
        cola_prioridad = []
        for caracter, frecuencia in frecuencias.items():
            heapq.heappush(cola_prioridad, NodoHuffman(caracter, frecuencia))
        
        # Construye el árbol combinando nodos
        while len(cola_prioridad) > 1:
            nodo_izq = heapq.heappop(cola_prioridad)
            nodo_der = heapq.heappop(cola_prioridad)
            
            nodo_padre = NodoHuffman()
            nodo_padre.frecuencia = nodo_izq.frecuencia + nodo_der.frecuencia
            nodo_padre.izquierda = nodo_izq
            nodo_padre.derecha = nodo_der
            
            heapq.heappush(cola_prioridad, nodo_padre)
        
        if cola_prioridad:
            self.raiz = heapq.heappop(cola_prioridad)
            
            # Genera códigos para cada caracter
            self.codigos = {}
            self._generar_codigos(self.raiz, "")
        
        # Ordena la tabla de códigos
        return self.raiz
    
    def _generar_codigos(self, nodo, codigo_actual):
        if nodo is None:
            return
        
        # Si es un nodo hoja es decir si tiene un caracter almacena el código
        if nodo.caracter is not None:
            self.codigos[nodo.caracter] = codigo_actual
        
        # Genera los códigos de las ramas, para izquierda 0 y para derecha 1
        self._generar_codigos(nodo.izquierda, codigo_actual + "0")
        self._generar_codigos(nodo.derecha, codigo_actual + "1")
    
    def encriptar(self, texto=None):
        if texto is None:
            texto = self.texto_original
            
        if not self.codigos:
            self.generar_arbol(texto)
            
        texto_encriptado = ""
        for caracter in texto:
            texto_encriptado += self.codigos[caracter]
            
        return texto_encriptado
    
    def desencriptar(self, texto_encriptado):
        if not self.raiz:
            return "Error: El árbol no ha sido generado."
            
        texto_desencriptado = ""
        nodo_actual = self.raiz
        
        for bit in texto_encriptado:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha
                
            # Llega a un nodo hoja
            if nodo_actual.caracter is not None:
                texto_desencriptado += nodo_actual.caracter
                nodo_actual = self.raiz
                
        return texto_desencriptado
    
    def exportar_arbol(self, nombre_archivo="arbol_huffman", formato="pdf"):
        if not self.raiz:
            return "Error: El árbol Huffman no ha sido generado."
            
        dot = graphviz.Digraph(comment='Árbol de Huffman')
      
        def agregar_nodos(nodo, id_nodo=0):
            if nodo is None:
                return
                
            # Añade el ID del nodo y su frecuencia al arbol
            etiqueta = str(nodo.frecuencia) #
            if nodo.caracter is not None:
                if nodo.caracter == ' ':
                    etiqueta += "\nespacio"
                else:
                    etiqueta += f"\n{nodo.caracter}"
                    
            dot.node(str(id_nodo), etiqueta)
            
            # Añade hijos y sus ramas 
            if nodo.izquierda:
                id_izq = id_nodo * 2 + 1
                agregar_nodos(nodo.izquierda, id_izq)
                dot.edge(str(id_nodo), str(id_izq), label='0')
                
            if nodo.derecha:
                id_der = id_nodo * 2 + 2
                agregar_nodos(nodo.derecha, id_der)
                dot.edge(str(id_nodo), str(id_der), label='1')
        
        # Comienza a agregar nodos desde la raíz
        agregar_nodos(self.raiz)
        
        dot.render(nombre_archivo, format=formato, cleanup=True)
        
        return f"{nombre_archivo}.{formato}"
    
    def generar_tabla_codigos(self):
        if not self.codigos:
            return "Error: Los códigos no han sido generados."
            
        # Mantiene solo la primera aparición de cada carácter
        caracteres_vistos = {}
        orden_original = []
        
        # Recorre el texto original y registra el orden de aparición de los caracteres
        for caracter in self.texto_original:
            if caracter not in caracteres_vistos:
                caracteres_vistos[caracter] = True
                orden_original.append(caracter)
        
        # Hace la tabla usando el orden de ingreso original
        tabla = []
        for caracter in orden_original:
            nombre_caracter = "espacio" if caracter == " " else caracter
            tabla.append((nombre_caracter, self.codigos[caracter]))
            
        return tabla