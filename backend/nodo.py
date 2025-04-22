class NodoHuffman:
    def __init__(self, caracter=None, frecuencia=0):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None
        self.id = id(self)
        
    def __lt__(self, otro):
        # Cantidad de veces que aparece un caracter en el texto
        if self.frecuencia != otro.frecuencia:
            return self.frecuencia < otro.frecuencia
        
        # Si uno es un nodo hoja, pero el otro no
        if self.caracter is not None and otro.caracter is None:
            return True
        if self.caracter is None and otro.caracter is not None:
            return False
            
        # Si ambos tienen carácter solo compara los caracteres
        if self.caracter is not None and otro.caracter is not None:
            # Comparación basada en el código ASCII 
            return self.caracter < otro.caracter
            
        # Usa el ID para el orden de la tabla
        return self.id < otro.id