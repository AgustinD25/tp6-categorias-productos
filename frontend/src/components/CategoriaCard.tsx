import type { Categoria } from '../types/categoria'

type CategoriaCardProps = {
  categoria: Categoria
  onEditar: (categoria: Categoria) => void
  onEliminar: (id: number) => void
}

function CategoriaCard({ categoria, onEditar, onEliminar }: CategoriaCardProps) {
  return (
    <article className="flex flex-col justify-between rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div>
        <h3 className="text-lg font-semibold text-slate-800">{categoria.nombre}</h3>
        <p className="mt-1 text-sm text-slate-600">
          {categoria.descripcion || 'Sin descripción'}
        </p>
      </div>
      <div className="mt-4 flex gap-2">
        <button
          type="button"
          onClick={() => onEditar(categoria)}
          className="rounded-md bg-amber-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-amber-600"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onEliminar(categoria.id)}
          className="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700"
        >
          Eliminar
        </button>
      </div>
    </article>
  )
}

export default CategoriaCard
