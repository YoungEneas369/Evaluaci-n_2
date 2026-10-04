# Importamos la clase Cliente desde el archivo cliente.py.
from cliente import Cliente
from paquetesAgencia import PaqueteNacional
# del archivo cliente.py, trae la clase Cliente para poder usarla aquí

# Creamos los objetos y mostramos sus datos.
cliente_ana = Cliente("Ana", "ana@example.com", "+56912345678")
print(cliente_ana.nombre,cliente_ana.correo, cliente_ana.telefono)
Cliente_2 = Cliente("Cristopher", "figueroacristopher@gmail.com", "+56993949002")
print(Cliente_2.nombre, Cliente_2.correo, Cliente_2.telefono)

# Cambiamos únicamente los datos de Ana usando sus métodos.
cliente_ana.cambiar_correo("ana.nuevo@example.com")
cliente_ana.cambiar_telefono("+56987654321")

# Consultamos los atributos para ver los valores después del cambio.
print("Datos actualizados de Ana:")
print(cliente_ana.nombre, cliente_ana.correo, cliente_ana.telefono)


# Actualizar nombre de Cliente_2
Cliente_2.cambiar_nombre("Cristopher Figueroa")
Cliente_2.cambiar_telefono("+56912345678")
print(Cliente_2.nombre, Cliente_2.telefono)

# El precio de este ejemplo es por viajero y ya incluye los servicios.
paquete_sur = PaqueteNacional("Viaje a Puerto Varas", 150000)
# Guardamos el resultado que entrega el método y luego lo mostramos.
total_viaje = paquete_sur.calcular_total(2)
print("Total para dos viajeros en pesos chilenos:", total_viaje)


#Consultas sobre nombre de paquete y precio por viajero
print("Nombre del paquete:", paquete_sur.nombre)
print("Precio por viajero:", paquete_sur.precio_por_viajero)
