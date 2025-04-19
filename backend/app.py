from flask import Flask, request, jsonify, send_file # type: ignore
from flask_cors import CORS # type: ignore
import os
import base64
from huffman import ArbolHuffman  

app = Flask(__name__)
CORS(app) 

session_trees = {}

@app.route('/api/encriptar', methods=['POST'])
def encriptar():
    data = request.get_json()
    texto = data.get('texto', '')
    
    if not texto:
        return jsonify({'error': 'El texto no puede estar vacío'}), 400
    
    # Crea el árbol de Huffman
    huffman = ArbolHuffman()
    huffman.generar_arbol(texto)
    
    # Encripta el texto
    texto_encriptado = huffman.encriptar()
    
    # ID único para esta sesión
    import uuid
    session_id = str(uuid.uuid4())
    session_trees[session_id] = huffman
    
    # Genera la tabla de códigos
    tabla_codigos = huffman.generar_tabla_codigos()
    
    return jsonify({
        'session_id': session_id,
        'texto_original': texto,
        'texto_encriptado': texto_encriptado,
        'tabla_codigos': tabla_codigos
    })

@app.route('/api/desencriptar', methods=['POST'])
def desencriptar():
    data = request.get_json()
    texto_encriptado = data.get('texto_encriptado', '')
    session_id = data.get('session_id', '')
    
    if not texto_encriptado or not session_id:
        return jsonify({'error': 'Faltan parámetros necesarios'}), 400
    
    huffman = session_trees.get(session_id)
    if not huffman:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    # Desencripta el texto
    texto_desencriptado = huffman.desencriptar(texto_encriptado)
    
    return jsonify({
        'texto_desencriptado': texto_desencriptado
    })

@app.route('/api/exportar-arbol', methods=['GET'])
def exportar_arbol():
    session_id = request.args.get('session_id', '')
    
    if not session_id:
        return jsonify({'error': 'ID de sesión requerido'}), 400
    
    huffman = session_trees.get(session_id)
    if not huffman:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    # Exporta el árbol a un archivo PDF
    nombre_archivo = f"arbol_huffman_{session_id}"
    ruta_archivo = huffman.exportar_arbol(nombre_archivo)
    
    # Envia el archivo al cliente
    return send_file(ruta_archivo, mimetype='application/pdf')

@app.route('/api/visualizar-arbol', methods=['GET'])
def visualizar_arbol():
    session_id = request.args.get('session_id', '')
    
    if not session_id:
        return jsonify({'error': 'ID de sesión requerido'}), 400
    
    huffman = session_trees.get(session_id)
    if not huffman:
        return jsonify({'error': 'Sesión no encontrada'}), 404
    
    # Exporta el árbol a un archivo PNG para visualización
    nombre_archivo = f"arbol_huffman_{session_id}"
    ruta_archivo = huffman.exportar_arbol(nombre_archivo, formato="png")
    
    # Lee el archivo y lo convierte a base64 para enviar al frontend
    with open(ruta_archivo, 'rb') as img_file:
        img_data = base64.b64encode(img_file.read()).decode('utf-8')
    
    return jsonify({
        'imagen_arbol': img_data
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)