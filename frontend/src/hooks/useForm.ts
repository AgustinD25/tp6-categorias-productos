import { useState } from 'react'
import type { ChangeEvent } from 'react'

// Hook genérico para formularios: guarda los valores y expone un handleChange reutilizable.
// Cada input debe tener un atributo name igual a la clave del objeto de valores.
export function useForm<T extends Record<string, string>>(valoresIniciales: T) {
  const [values, setValues] = useState<T>(valoresIniciales)

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setValues((prev) => ({ ...prev, [name]: value }))
  }

  return { values, handleChange }
}
