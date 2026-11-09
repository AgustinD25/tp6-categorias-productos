import type { Categoria } from '../types/categoria'
import CategoriaCard from './CategoriaCard'

type CategoriaListProps = {
  categorias: Categoria[]
  onEditar: (categoria: Categoria) => void
  onEliminar: (id: number) => void
}

function CategoriaList({ categorias, onEditar, onEliminar }: CategoriaListProps) {
  if (categorias.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-slate-300 p-8 text-center text-slate-500">
        Todavía no hay categorías. Creá la primera con el botón «Nueva categoría».
      </p>
    )
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          onEditar={onEditar}
          onEliminar={onEliminar}
        />
      ))}
    </div>
  )
}

export default CategoriaList
