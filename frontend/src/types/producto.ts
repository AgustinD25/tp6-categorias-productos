import type { Categoria } from './categoria'

export type Producto = {
  id: number
  nombre: string
  descripcion: string
  precio_base: number
  imagen_url: string[]
  disponible: boolean
  categorias: Categoria[]
}
