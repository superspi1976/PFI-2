import _sqlite3 as lite  # Se importa para trabajar con sqlite

def main():  # Función principal del programa
    while True:
        print('''
        Elija una opción:

    1. Agregar Producto
    2. Mostrar Producto
    3. Actualizar Cantidad de Producto
    4. Eliminar Producto
    5. Buscar Producto
    6. Reporte de Bajo Stock
    7. Salir
        ''')
       
# Funcion principal, la funcion vuelve a ejecutrase    
        
        try:
            opcion = int(input('Elija una opción: '))
        except ValueError:
            print("Opción inválida. Debe ingresar un número entero.")
            continue  # Continuamos el bucle si no es un número válido

        if opcion == 1:
            print('Agregar Producto')
            registrar_producto()
        elif opcion == 2:
            print('Mostrar Producto')
            mostrar_productos()
        elif opcion == 3:
            print("Actualizar cantidad de producto")
            actualizar_cantidad()       
        elif opcion == 4:
            print("Eliminar producto")
            eliminar_producto()
        elif opcion == 5:
            print("Buscar producto")
            buscar_producto()
        elif opcion == 6:
            print("Reporte de bajo stock")
            bajo_stock()
        elif opcion == 7:
            print("Hasta luego...")
            break  # Salir del bucle y terminar el programa
        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")
            continue


def create_data_base(): #creamos la base de datos
    conexion = lite.connect('inventario.db')
    conexion.commit()
    conexion.close()
    
def db_crear_tabla_productos(): #creamos la tabla productos
    conexion = lite.connect('inventario.db') #creamos la base de datos
    cursor = conexion.cursor()  # siempre igual
    cursor.execute(
            """ 
            CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
            )
            """
        )
    conexion.commit()
    conexion.close()

create_data_base()
db_crear_tabla_productos()


# Funcion registrar_producto, da de alta los productos en el inventario
# Solicita los datos del producto y usa el metodo title (usa las mayusculas en las primer letra) para guardar


def registrar_producto(): 
  
   # Pedir datos al usuario
    nombre = input('Ingrese el nombre del producto: ')
    nombre = nombre.title()
    descripcion = input('Ingrese la descrición del producto: ')
    descripcion = descripcion.title()
    cantidad = int(input('Ingrese la cantida: '))
    precio = float(input('Ingrese precio: '))
    categoria = input('Ingrese la categoria: ')
    categoria = categoria.title()

    conexion = lite.connect('inventario.db')
    cursor = conexion.cursor()
    instruccion = f"INSERT INTO productos(nombre , descripcion, cantidad, precio,  categoria) VALUES(?, ? , ?, ?, ? )"
    cursor.execute(instruccion,(nombre, descripcion,cantidad,  precio, categoria))

 # Mensaje de éxito
    print(f" Producto '{nombre}' , agregado con exito " )    

    conexion.commit() # confirmar cambios
    conexion.close() # cerrar conexion

    
# Muestra el inventario de todos los productos y sus atributos


def mostrar_productos():
    conexion = lite.connect('inventario.db')
    cursor = conexion.cursor()
    instruccion = f" SELECT * FROM productos"
    cursor.execute(instruccion)
    mostrar = cursor.fetchall()

    conexion.close()


    if not mostrar:
        print('No hay productos en el inventario') # en caso la base de datos este vacia
    else:
        print('Inventario actual: ')
        
        # Mostrar los productos
        for i in mostrar:
            id, nombre, descripcion, cantidad, precio, categoria = i
            print(f'''ID: {id}
            Nombre: {nombre}
            Descripcion: {descripcion}
            Cantidad: {cantidad}
            Precio: {precio}
            Categoria: {categoria}
            ''')


# Funcion actualizar ,  
# Pide el ID del producto y la nueva cantidad que se quiere actualizar

def actualizar_cantidad():
    conexion = lite.connect('inventario.db')
    cursor = conexion.cursor()

    try:
        id_producto = int(input("Ingrese el ID del producto a actualizar: "))
        nueva_cantidad = int(input("Ingrese la nueva cantidad: "))

        # Ejecutar la consulta con parámetros 
        cursor.execute("UPDATE productos SET cantidad=? WHERE id=?", (nueva_cantidad, id_producto,))

        # Comprobar si se actualizaron filas
        filas_afectadas = cursor.rowcount
        if filas_afectadas > 0:
            print(f"Se actualizó la cantidad del producto con ID {id_producto}")
        else:
            print(f"No se encontró ningún producto con ID {id_producto}")

    except ValueError:
        print("Error: Debe ingresar un ID y una cantidad válidos (números enteros)")
    except lite.Error as e:
        print(f"Error al actualizar la cantidad: {e}")
    finally:
        conexion.commit()
        conexion.close()


# Elimina un producto de la base de datos basándose en el ID del producto
# Muestra el código y el nombre del producto eliminado
def eliminar_producto():
    conexion = lite.connect('inventario.db')
    cursor = conexion.cursor()
        
    try:
        id_producto = int(input("Ingrese el código del producto a eliminar: "))

        # Verificar si el producto existe y obtener su nombre
        cursor.execute("SELECT nombre FROM productos WHERE id =?", (id_producto,))
        producto = cursor.fetchone()
        if producto:
            nombre = producto[0]  # Obtener el nombre del producto
            # Eliminar el producto
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conexion.commit()  # Confirmar la eliminación
            print(f"Producto eliminado: id: {id_producto}, Nombre: {nombre}")
        else:
            print("No se encontró un producto con ese código.")
    except ValueError:
        print("Por favor, ingrese un número válido para el código.")
    except lite.Error as e:
        print(f"Error al eliminar producto: {e}")
    finally:
        conexion.close()

# Funcion buscar_producto, busca un producto por nombre, categoria o ID
# Pide al usuario que ingrese el campo por el cual quiere buscar el producto

def buscar_producto():
    """Busca un producto en la base de datos por nombre, categoría o ID."""

    def buscar(campo, valor):
        """Función auxiliar para realizar la consulta a la base de datos."""
        conn = lite.connect('inventario.db')
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM productos WHERE {campo} LIKE ?"
        cursor.execute(instruccion, (f"%{valor}%",))
        resultados = cursor.fetchall()
        conn.close()
        return resultados

    while True:
        print("Desea buscar un producto por:")
        print("1. ID")
        print("2. Nombre")
        opcion = input("Seleccione una opción (o presione Enter para salir): ")

        if not opcion:
            break

        if opcion in ('1', '2'):
            if opcion == '1':
                campo = 'id'
                
            valor = input(f"Ingrese el {campo} del producto: ")
            resultados = buscar(campo, valor)

            if not resultados:
                print(f"No se encontraron productos con el {campo} '{valor}'.")
            else:
                print("Productos encontrados:")
                for producto in resultados:
                    id, nombre, descripcion, precio, cantidad, categoria = producto
                    print(f"ID: {id}")
                    print(f"Nombre: {nombre}")
                    print(f"Descripcion: {descripcion}")
                    print(f"Precio: {precio}")
                    print(f"Cantidad: {cantidad}")
                    print(f"Categoria: {categoria}")
        else:
            print("Opción inválida.")

# Funcion bajo_stock, muestra los productos que tienen stock por debajo de un limite
# Pide al usuario que ingrese el limite de stock que quiere revisar

def bajo_stock():
    conexion = lite.connect('inventario.db')
    cursor = conexion.cursor()

    try:
        limite = int(input('¿Cuál es el límite de stock que quieres revisar? '))
        if limite < 0:
            print("El límite de stock no puede ser negativo.")
            return

        cursor.execute("SELECT * FROM productos WHERE cantidad < ?", (limite,))
        productos_bajo_stock = cursor.fetchall()

        if not productos_bajo_stock:
            print(f"No hay productos con stock por debajo de {limite}.")
        else:
            print(f"Productos con stock por debajo de {limite}:")
            for producto in productos_bajo_stock:
                id, nombre, descripcion, precio, cantidad, categoria = producto
                print(f"ID: {id}")
                print(f"Nombre: {nombre}")
                print(f"Descripcion: {descripcion}")
                print(f"Precio: {precio}")
                print(f"Cantidad: {cantidad}")
                print(f"Categoria: {categoria}")

    except ValueError:
        print("Por favor, ingrese un número válido para el límite de stock.")

    finally:
        conexion.close()    
        
# Ejecución de la función main()

if __name__ == "__main__":
    main()