type NavbarProps = {
  titulo: string
}

function Navbar({ titulo }: NavbarProps) {
  return (
    <header className="bg-indigo-600 shadow">
      <nav className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4 sm:px-6">
        <span className="text-xl font-bold text-white">{titulo}</span>
        <span className="text-sm text-indigo-100">Gestión de categorías</span>
      </nav>
    </header>
  )
}

export default Navbar
