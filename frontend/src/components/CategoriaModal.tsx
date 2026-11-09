import type { FormEvent } from 'react'
import { useForm } from '../hooks/useForm'
import type { Categoria, CategoriaInput } from '../types/categoria'

type CategoriaModalProps = {
  // Si viene una categoría, el modal edita; si es null, crea una nueva.
  categoria: Categoria | null
  onSubmit: (data: CategoriaInput) => void
  onClose: () => void
}

// El padre (App) lo monta solo cuando el modal está abierto, por eso el formulario
// arranca siempre con los valores correctos de la categoría seleccionada.
function CategoriaModal({ categoria, onSubmit, onClose }: CategoriaModalProps) {
  const { values, handleChange } = useForm({
    nombre: categoria?.nombre ?? '',
    descripcion: categoria?.descripcion ?? '',
  })

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    onSubmit({ nombre: values.nombre.trim(), descripcion: values.descripcion.trim() })
  }

  return (
    <div
      className="fixed inset-0 z-10 flex items-center justify-center bg-black/50 p-4"
      onClick={onClose}
    >
      <form
        onSubmit={handleSubmit}
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl"
      >
        <h2 className="text-xl font-semibold text-slate-800">
          {categoria ? 'Editar categoría' : 'Nueva categoría'}
        </h2>

        <label className="mt-4 block text-sm font-medium text-slate-700">
          Nombre
          <input
            name="nombre"
            value={values.nombre}
            onChange={handleChange}
            required
            autoFocus
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 focus:border-indigo-500 focus:outline-none"
          />
        </label>

        <label className="mt-4 block text-sm font-medium text-slate-700">
          Descripción
          <textarea
            name="descripcion"
            value={values.descripcion}
            onChange={handleChange}
            rows={3}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 focus:border-indigo-500 focus:outline-none"
          />
        </label>

        <div className="mt-6 flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
          >
            Cancelar
          </button>
          <button
            type="submit"
            className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
          >
            Guardar
          </button>
        </div>
      </form>
    </div>
  )
}

export default CategoriaModal
