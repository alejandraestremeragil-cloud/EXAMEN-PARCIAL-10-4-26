# SISTEMA DE ALMACÉN
PRODUCTOS_OFICIALES = [
    "Aceitunas Rellenas",
    "Mermelada de Naranja",
    "Galletas Digestive",
    "Frutos Secos Pistachos",
    "Legumbres Garbanzos",
    "Leche Entera",
    "Aceitunas Gourmet Artesano",
    "Té Verde Premium",
    "Harina de Avena Intenso",
    "Aceite de Oliva Suave"
]

# MOSTRAR PRODUCTOS Y ESTANTERÍAS
def mostrar_productos_y_estanterias(almacen):
    print("\n PRODUCTOS DISPONIBLES EN EL ALMACÉN:")
    for i, prod in enumerate(PRODUCTOS_OFICIALES, start=1):
        print(f"  {i}. {prod}")

    print("\n ESTANTERÍAS DISPONIBLES:")
    for est in almacen.estanterias.keys():
        print(f"  - {est}")
    print()

# IDENTIFICAR PRODUCTO
def identificar_producto(texto_usuario):
    texto_usuario = texto_usuario.lower()
    mejor = None
    max_coincidencias = 0

    for nombre in PRODUCTOS_OFICIALES:
        coincidencias = 0
        for palabra in texto_usuario.split():
            if palabra in nombre.lower():
                coincidencias += 1

        if coincidencias > max_coincidencias:
            max_coincidencias = coincidencias
            mejor = nombre

    return mejor

# NODO LISTA ENLAZADA
class NodoProducto:
    def __init__(self, producto):
        self.producto = producto
        self.siguiente = None

# ESTANTERÍA (LISTA ENLAZADA)
class Estanteria:
    def __init__(self, nombre):
        self.nombre = nombre
        self.inicio = None

    def agregar_producto(self, producto):
        existente = self.buscar_producto(producto["nombre"])

        if existente:
            existente["cantidad"] += producto["cantidad"]
        else:
            nuevo = NodoProducto(producto)
            if self.inicio is None:
                self.inicio = nuevo
            else:
                actual = self.inicio
                while actual.siguiente:
                    actual = actual.siguiente
                actual.siguiente = nuevo

    def buscar_producto(self, nombre):
        actual = self.inicio
        while actual:
            if actual.producto["nombre"] == nombre:
                return actual.producto
            actual = actual.siguiente
        return None

    def eliminar_producto(self, nombre):
        actual = self.inicio
        anterior = None

        while actual:
            if actual.producto["nombre"] == nombre:
                if anterior:
                    anterior.siguiente = actual.siguiente
                else:
                    self.inicio = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def listar_productos(self):
        lista = []
        actual = self.inicio
        while actual:
            lista.append(actual.producto)
            actual = actual.siguiente
        return lista

# ALMACÉN
class Almacen:
    def __init__(self):
        self.estanterias = {}

    def agregar_estanteria(self, nombre):
        self.estanterias[nombre] = Estanteria(nombre)

    def agregar_producto(self, estanteria, producto):
        if estanteria in self.estanterias:
            self.estanterias[estanteria].agregar_producto(producto)
        else:
            print(f"La estantería '{estanteria}' no existe.")

    def mostrar_inventario(self):
        inventario = {}
        for nombre, est in self.estanterias.items():
            inventario[nombre] = est.listar_productos()
        return inventario

# DATOS INICIALES
datos_estanterias = {
    "Estantería A": [
        {"nombre": "Aceitunas Rellenas", "cantidad": 108, "precio": 1.32},
        {"nombre": "Mermelada de Naranja", "cantidad": 53, "precio": 2.22},
        {"nombre": "Galletas Digestive", "cantidad": 84, "precio": 3.66},
        {"nombre": "Frutos Secos Pistachos", "cantidad": 95, "precio": 3.42},
        {"nombre": "Legumbres Garbanzos", "cantidad": 15, "precio": 3.77},
        {"nombre": "Leche Entera", "cantidad": 63, "precio": 2.74}
    ],
    "Estantería B": [
        {"nombre": "Aceitunas Gourmet Artesano", "cantidad": 112, "precio": 3.35},
        {"nombre": "Té Verde Premium", "cantidad": 108, "precio": 2.92},
        {"nombre": "Harina de Avena Intenso", "cantidad": 117, "precio": 3.7},
        {"nombre": "Aceite de Oliva Suave", "cantidad": 55, "precio": 11.14}
    ]
}

def cargar_datos_en_almacen(almacen, datos):
    for nombre_estanteria, lista_productos in datos.items():
        almacen.agregar_estanteria(nombre_estanteria)
        for producto in lista_productos:
            almacen.agregar_producto(nombre_estanteria, producto)

# BÚSQUEDA GLOBAL
def buscar_producto_en_almacen(almacen, nombre):
    for est, obj in almacen.estanterias.items():
        prod = obj.buscar_producto(nombre)
        if prod:
            return prod, est
    return None, None

# ENTRADA DE PRODUCTO
def gestionar_entrada_producto(almacen):

    print("\n--- ENTRADA DE PRODUCTO ---")
    mostrar_productos_y_estanterias(almacen)

    descripcion = input("Producto: ")
    cantidad = int(input("Cantidad (en unidades): "))
    precio = float(input("Precio por unidad: "))
    estanteria = input("Estantería: ")

    nombre_real = identificar_producto(descripcion)

    if not nombre_real:
        print("Producto no válido")
        return

    if estanteria not in almacen.estanterias:
        print("Estantería no existe")
        return

    producto = {
        "nombre": nombre_real,
        "cantidad": cantidad,
        "precio": precio
    }

    almacen.agregar_producto(estanteria, producto)

    print("Producto añadido")

# SALIDA DE PRODUCTO
def gestionar_salida_producto(almacen):

    print("\n--- SALIDA DE PRODUCTO ---")
    mostrar_productos_y_estanterias(almacen)

    est = input("Estantería: ")
    descripcion = input("Producto: ")

    nombre_real = identificar_producto(descripcion)

    if not nombre_real:
        print(" Producto no válido")
        return

    if est not in almacen.estanterias:
        print(" Estantería no existe")
        return

    producto = almacen.estanterias[est].buscar_producto(nombre_real)

    if not producto:
        print(" No existe en esta estantería")
        return

    cantidad = int(input("Cantidad a retirar (en unidades): "))

    if cantidad > producto["cantidad"]:
        print(" No hay suficiente stock")
        return

    producto["cantidad"] -= cantidad

    if producto["cantidad"] == 0:
        almacen.estanterias[est].eliminar_producto(nombre_real)

    print("Retirada completada")

# ESTADO DEL ALMACÉN
def estado_del_almacen(almacen):

    print("\n--- ESTADO DEL ALMACÉN ---")

    total = 0

    for est, obj in almacen.estanterias.items():
        print(f"\n{est}:")

        actual = obj.inicio

        if not actual:
            print("  Vacía")

        while actual:
            p = actual.producto
            print(f"  {p['nombre']} - {p['cantidad']} uds (precio: {p['precio']} €)")
            total += p["cantidad"]
            actual = actual.siguiente

    print(f"\nTOTAL UNIDADES: {total}")

def transferir_producto(almacen):

    print("\n--- TRANSFERENCIA DE PRODUCTO ENTRE ESTANTERÍAS ---")
    mostrar_productos_y_estanterias(almacen)

    descripcion = input("Producto: ")
    cantidad = int(input("Cantidad a transferir (en unidades): "))
    origen = input("Estantería origen: ")
    destino = input("Estantería destino: ")

    # Validar producto
    nombre_real = identificar_producto(descripcion)
    if not nombre_real:
        print(" Producto no válido. Debe ser uno de los productos oficiales.")
        return

    # Validar estanterías
    if origen not in almacen.estanterias:
        print(f" La estantería de origen '{origen}' no existe.")
        return

    if destino not in almacen.estanterias:
        print(f" La estantería de destino '{destino}' no existe.")
        return

    if origen == destino:
        print(" No puedes transferir a la misma estantería.")
        return

    est_origen = almacen.estanterias[origen]
    est_destino = almacen.estanterias[destino]

    # Buscar producto en origen
    producto_origen = est_origen.buscar_producto(nombre_real)
    if not producto_origen:
        print(f"El producto '{nombre_real}' no está en la estantería {origen}.")
        return

    # Validar cantidad
    if cantidad > producto_origen["cantidad"]:
        print(f" No hay suficientes unidades en {origen}. Solo hay {producto_origen['cantidad']}.")
        return

    # Guardar precio ANTES de modificar origen
    precio_unitario = producto_origen["precio"]

    # Restar en origen
    producto_origen["cantidad"] -= cantidad

    # Si queda a 0 → eliminar nodo
    if producto_origen["cantidad"] == 0:
        est_origen.eliminar_producto(nombre_real)

    # Añadir al destino
    producto_destino = est_destino.buscar_producto(nombre_real)

    if producto_destino:
        producto_destino["cantidad"] += cantidad
    else:
        est_destino.agregar_producto({
            "nombre": nombre_real,
            "cantidad": cantidad,
            "precio": precio_unitario
        })

    print(f"\n TRANSFERENCIA COMPLETADA")
    print(f"   • Producto: {nombre_real}")
    print(f"   • Cantidad transferida: {cantidad}")
    print(f"   • Desde: {origen}")
    print(f"   • Hacia: {destino}")



# ANÁLISIS AVANZADO DE ESTANTERÍAS
# -----------------------------
def analizar_estanterias(almacen):

    print("\n--- ANÁLISIS AVANZADO DE ESTANTERÍAS ---")

    mayor_valor = None
    menor_productos = None

    valor_max = -1
    productos_min = float("inf")

    for nombre, est in almacen.estanterias.items():

        actual = est.inicio
        valor_total = 0
        cantidad_productos = 0

        while actual:
            prod = actual.producto
            valor_total += prod["cantidad"] * prod["precio"]
            cantidad_productos += 1
            actual = actual.siguiente

        if valor_total > valor_max:
            valor_max = valor_total
            mayor_valor = nombre

        if cantidad_productos < productos_min:
            productos_min = cantidad_productos
            menor_productos = nombre

    print(f"\n Estantería con MAYOR valor acumulado: {mayor_valor} ({valor_max:.2f} €)")
    print(f" Estantería con MENOS productos: {menor_productos} ({productos_min} productos)")

# PARTE 2: GRAFOS + VISUALIZACIÓN + RUTAS INTELIGENTES
import networkx as nx
import matplotlib.pyplot as plt

def crear_grafo_almacen():

    G = nx.Graph()

    G.add_node("Entrada")
    G.add_node("Estantería A")
    G.add_node("Estantería B")

    G.add_edge("Entrada", "Estantería A", weight=5)
    G.add_edge("Entrada", "Estantería B", weight=7)
    G.add_edge("Estantería A", "Estantería B", weight=3)

    return G

def dibujar_grafo(G):

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, "weight")

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2500,
        node_color="lightblue"
    )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("MAPA DEL ALMACÉN")
    plt.show()

def ruta_mas_corta(G, destino):

    origen = "Entrada"

    if destino not in G.nodes:
        print("❌ El destino no existe en el mapa del almacén.")
        return None

    camino = nx.dijkstra_path(G, origen, destino)
    distancia = nx.dijkstra_path_length(G, origen, destino)

    print("\n--- RUTA ÓPTIMA ---")
    print("Camino:", " -> ".join(camino))
    print("Distancia:", distancia, "unidades")

    return camino

def dibujar_ruta(G, camino):

    if not camino:
        return

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2500,
        node_color="lightblue"
    )

    edges = list(zip(camino, camino[1:]))

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=edges,
        width=4,
        edge_color="red"
    )

    plt.title("RUTA ÓPTIMA EN EL ALMACÉN")
    plt.show()

def buscar_con_ruta(almacen, grafo):

    print("\n--- BÚSQUEDA INTELIGENTE ---")

    descripcion = input("Producto: ")

    nombre = identificar_producto(descripcion)

    if not nombre:
        print(" Producto no válido")
        return

    prod, est = buscar_producto_en_almacen(almacen, nombre)

    if not prod:
        print(" No encontrado")
        return

    print(f"\n Producto en: {est}")
    print(f" Cantidad: {prod['cantidad']}")

    camino = ruta_mas_corta(grafo, est)

    if camino:
        dibujar_ruta(grafo, camino)


# MENÚ PRINCIPAL
def menu(almacen, grafo):

    while True:

        mostrar_productos_y_estanterias(almacen)

        print("     SISTEMA DE ALMACÉN")

        print("1. Entrada de producto")
        print("2. Salida de producto")
        print("3. Buscar producto")
        print("4. Estado del almacén")
        print("5. Inventario completo")
        print("6. Transferir producto")
        print("7. Mostrar mapa del almacén")
        print("8. Buscar producto con ruta óptima")
        print("9. Análisis avanzado de estanterías")
        print("10. Salir")

        opcion = input("Opción: ")

        if opcion == "1":
            gestionar_entrada_producto(almacen)

        elif opcion == "2":
            gestionar_salida_producto(almacen)

        elif opcion == "3":
            descripcion = input("Producto: ")
            nombre = identificar_producto(descripcion)
            if not nombre:
                print(" Producto no válido")
            else:
                prod, est = buscar_producto_en_almacen(almacen, nombre)
                if prod:
                    print(f" Encontrado en {est}: {prod['nombre']} - {prod['cantidad']} uds")
                else:
                    print("No encontrado")

        elif opcion == "4":
            estado_del_almacen(almacen)

        elif opcion == "5":
            print("\n--- INVENTARIO COMPLETO ---")
            print(almacen.mostrar_inventario())

        elif opcion == "6":
            transferir_producto(almacen)

        elif opcion == "7":
            dibujar_grafo(grafo)

        elif opcion == "8":
            buscar_con_ruta(almacen, grafo)

        elif opcion == "9":
            analizar_estanterias(almacen)

        elif opcion == "10":
            print("\nAntes de salir, recuerda que el almacén trabaja con estos productos y estanterías:")
            mostrar_productos_y_estanterias(almacen)
            print("Saliendo...")
            break

        else:
            print(" Opción no válida")

# -----------------------------
# EJECUCIÓN FINAL DEL PROGRAMA
# -----------------------------
if __name__ == "__main__":
    almacen = Almacen()
    cargar_datos_en_almacen(almacen, datos_estanterias)

    grafo = crear_grafo_almacen()

    menu(almacen, grafo)