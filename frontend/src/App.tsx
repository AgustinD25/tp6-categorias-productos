import { useEffect, useState } from 'react'
import CategoriaList from './components/CategoriaList'
import CategoriaModal from './components/CategoriaModal'
import Navbar from './components/Navbar'
import type { Categoria, CategoriaInput } from './types/categoria'

const API_URL = 'http://localhost:8000/categorias'

// Convierte una respuesta no exitosa en un Error con el detalle que manda FastAPI.
async function verificar(res: Response): Promise<Response> {
  if (res.ok) return res
  let mensaje = `Error ${res.status}`
  try {
    const cuerpo = await res.json()
    if (typeof cuerpo.detail === 'string') mensaje = cuerpo.detail
  } catch {
    // la respuesta no traía JSON: se deja el mensaje genérico
  }
  throw new Error(mensaje)
}

function App() {
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [modalAbierto, setModalAbierto] = useState(false)
  const [seleccionada, setSeleccionada] = useState<Categoria | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [cargando, setCargando] = useState(true)

  // GET /categorias al montar el componente.
  useEffect(() => {
    async function cargar() {
      try {
        const res = await verificar(await fetch(API_URL))
        setCategorias(await res.json())
      } catch (e) {
        setError(e instanceof Error ? e.message : 'No se pudo conectar con el servidor')
      } finally {
        setCargando(false)
      }
    }
    cargar()
  }, [])

  const abrirNueva = () => {
    setSeleccionada(null)
    setModalAbierto(true)
  }

  const abrirEdicion = (categoria: Categoria) => {
    setSeleccionada(categoria)
    setModalAbierto(true)
  }

  const cerrarModal = () => {
    setModalAbierto(false)
    setSeleccionada(null)
  }

  const handleCreate = async (data: CategoriaInput) => {
    try {
      const res = await verificar(
        await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        }),
      )
      const creada: Categoria = await res.json()
      setCategorias((prev) => [...prev, creada])
      setError(null)
      cerrarModal()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo crear la categoría')
    }
  }

  const handleUpdate = async (id: number, data: CategoriaInput) => {
    try {
      const res = await verificar(
        await fetch(`${API_URL}/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        }),
      )
      const actualizada: Categoria = await res.json()
      setCategorias((prev) => prev.map((c) => (c.id === id ? actualizada : c)))
      setError(null)
      cerrarModal()
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo actualizar la categoría')
    }
  }

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Eliminar esta categoría? Se quitará también de sus productos.')) return
    try {
      await verificar(await fetch(`${API_URL}/${id}`, { method: 'DELETE' }))
      setCategorias((prev) => prev.filter((c) => c.id !== id))
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'No se pudo eliminar la categoría')
    }
  }

  // El modal sirve para crear y para editar: según haya categoría seleccionada se llama a uno u otro.
  const handleSubmit = (data: CategoriaInput) =>
    seleccionada ? handleUpdate(seleccionada.id, data) : handleCreate(data)

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar titulo="Tienda · Categorías" />

      <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-800">Categorías</h1>
          <button
            type="button"
            onClick={abrirNueva}
            className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
          >
            Nueva categoría
          </button>
        </div>

        {error && (
          <p role="alert" className="mb-4 rounded-md bg-red-100 px-4 py-3 text-sm text-red-700">
            {error}
          </p>
        )}

        {cargando ? (
          <p className="text-slate-500">Cargando categorías…</p>
        ) : (
          <CategoriaList categorias={categorias} onEditar={abrirEdicion} onEliminar={handleDelete} />
        )}
      </main>

      {modalAbierto && (
        <CategoriaModal categoria={seleccionada} onSubmit={handleSubmit} onClose={cerrarModal} />
      )}
    </div>
  )
}

export default App
