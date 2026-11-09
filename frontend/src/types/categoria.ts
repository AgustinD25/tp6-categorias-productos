export type Categoria = {
  id: number
  nombre: string
  descripcion: string
}

// Lo que se envía al backend al crear o editar (el id lo genera la base de datos).
export type CategoriaInput = Omit<Categoria, 'id'>
