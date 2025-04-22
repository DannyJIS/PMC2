import React, { useState } from 'react';
import './App.css';

function App() {
  const [texto, setTexto] = useState('');
  const [textoEncriptado, setTextoEncriptado] = useState('');
  const [tablaCodigos, setTablaCodigos] = useState([]);
  const [sessionId, setSessionId] = useState('');
  const [imagenArbol, setImagenArbol] = useState('');
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');

  const API_URL = 'http://localhost:5000/api';

  // Función para encriptar el texto
  const encriptar = async () => {
    if (!texto.trim()) {
      setError('Por favor, ingresa un texto para encriptar.');
      return;
    }

    setCargando(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/encriptar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ texto }),
      });

      const data = await response.json();

      if (response.ok) {
        setTextoEncriptado(data.texto_encriptado);
        setTablaCodigos(data.tabla_codigos);
        setSessionId(data.session_id);

        // Limpia la imagen previa del árbol
        setImagenArbol('');
      } else {
        setError(data.error || 'Error al encriptar el texto.');
      }
    } catch (err) {
      setError('Error de conexión con el servidor.');
      console.error(err);
    } finally {
      setCargando(false);
    }
  };

  // Función para desencriptar el texto
  const desencriptar = async () => {
    if (!textoEncriptado || !sessionId) {
      setError('Primero debes encriptar un texto.');
      return;
    }

    setCargando(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/desencriptar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          texto_encriptado: textoEncriptado,
          session_id: sessionId,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(`Texto desencriptado: ${data.texto_desencriptado}`);
      } else {
        setError(data.error || 'Error al desencriptar el texto.');
      }
    } catch (err) {
      setError('Error de conexión con el servidor.');
      console.error(err);
    } finally {
      setCargando(false);
    }
  };

  // Función para ver el árbol
  const visualizarArbol = async () => {
    if (!sessionId) {
      setError('Primero debes encriptar un texto.');
      return;
    }

    setCargando(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/visualizar-arbol?session_id=${sessionId}`);
      const data = await response.json();

      if (response.ok) {
        setImagenArbol(`data:image/png;base64,${data.imagen_arbol}`);
      } else {
        setError(data.error || 'Error al visualizar el árbol.');
      }
    } catch (err) {
      setError('Error de conexión con el servidor.');
      console.error(err);
    } finally {
      setCargando(false);
    }
  };

  // Función para exportar el árbol en PDF
  const exportarArbol = () => {
    if (!sessionId) {
      setError('Primero debes encriptar un texto.');
      return;
    }

    // Abre una nueva ventana para descargar el PDF
    window.open(`${API_URL}/exportar-arbol?session_id=${sessionId}`, '_blank');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Encriptación con Árbol de Huffman</h1>
      </header>

      <main className="App-content">
        <section className="entrada-texto">
          <h2>Ingresa tu texto</h2>
          <textarea
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            placeholder="Escribe aquí el texto que deseas encriptar..."
            rows={5}
            cols={50}
          />
          <button onClick={encriptar} disabled={cargando || !texto.trim()}>
            {cargando ? 'Encriptando...' : 'Encriptar'}
          </button>
        </section>

        {textoEncriptado && (
          <section className="resultado">
            <h2>Resultado de la encriptación</h2>
            <div className="texto-encriptado">
              <h3>Texto encriptado:</h3>
              <p>{textoEncriptado}</p>
              <button onClick={desencriptar}>Desencriptar</button>
            </div>

            <div className="tabla-codigos">
              <h3>Tabla de códigos:</h3>
              <table>
                <thead>
                  <tr>
                    <th>Carácter</th>
                    <th>Código</th>
                  </tr>
                </thead>
                <tbody>
                  {tablaCodigos.map((item, index) => (
                    <tr key={index}>
                      <td>{item[0]}</td>
                      <td>{item[1]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="acciones-arbol">
              <button onClick={visualizarArbol}>Visualizar Árbol</button>
              <button onClick={exportarArbol}>Exportar Árbol (PDF)</button>
            </div>
          </section>
        )}

        {imagenArbol && (
          <section className="visualizacion-arbol">
            <h2>Árbol de Huffman</h2>
            <img src={imagenArbol} alt="Árbol de Huffman" style={{ maxWidth: '100%' }} />
          </section>
        )}

        {error && <div className="error-mensaje">{error}</div>}
      </main>
    </div>
  );
}

export default App;