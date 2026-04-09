class Libro:
    def __init__(self, titulo, autor, cantidad):
        self.titulo = titulo
        self.autor = autor
        self.cantidad = cantidad

class Biblioteca:
    def __init__(self):
        self.catalogo = {}

    def agregar_libro(self, titulo, autor, cantidad):
        if titulo in self.catalogo:
            self.catalogo[titulo].cantidad += cantidad
        else:
            self.catalogo[titulo] = Libro(titulo, autor, cantidad)
        print(f"\n✅ Libro '{titulo}' actualizado en el sistema.")

    def prestar_libro(self, titulo):
        libro = self.catalogo.get(titulo)
        if libro and libro.cantidad > 0:
            libro.cantidad -= 1
            print(f"\n📖 Préstamo realizado. Quedan {libro.cantidad} unidades.")
        else:
            print("\n❌ Error: No hay stock o el libro no existe.")

    def devolver_libro(self, titulo):
        if titulo in self.catalogo:
            self.catalogo[titulo].cantidad += 1
            print(f"\n🔄 Libro devuelto. Ahora hay {self.catalogo[titulo].cantidad}.")
        else:
            print("\n⚠️ Este libro no estaba en el catálogo, pero ha sido recibido.")
            self.agregar_libro(titulo, "Desconocido", 1)

    def consultar(self, titulo):
        libro = self.catalogo.get(titulo)
        if libro:
            estado = "Disponible" if libro.cantidad > 0 else "Agotado"
            print(f"\n🔍 {libro.titulo} | Autor: {libro.autor} | Stock: {libro.cantidad} ({estado})")
        else:
            print("\n🔍 El libro no se encuentra en el sistema.")

def mostrar_menu():
    biblio = Biblioteca()
    
    while True:
        print("\n" + "="*30)
        print("   GESTOR DE BIBLIOTECA")
        print("="*30)
        print("1. Agregar libro")
        print("2. Prestar libro")
        print("3. Devolver libro")
        print("4. Consultar disponibilidad")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ")

        if opcion == "1":
            t = input("Título: ")
            a = input("Autor: ")
            c = int(input("Cantidad: "))
            biblio.agregar_libro(t, a, c)
        
        elif opcion == "2":
            t = input("Título del libro a prestar: ")
            biblio.prestar_libro(t)
            
        elif opcion == "3":
            t = input("Título del libro a devolver: ")
            biblio.devolver_libro(t)
            
        elif opcion == "4":
            t = input("Título a consultar: ")
            biblio.consultar(t)
            
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opcíon no válida, intenta de nuevo.")

if __name__ == "__main__":
    mostrar_menu()