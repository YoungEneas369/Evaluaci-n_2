# Importamos la clase Cliente desde el archivo cliente.py.
from cliente import Cliente
from paquete_nacional import PaqueteNacional
from paquete_internacional import PaqueteInternacional
from crucero import Crucero
# del archivo cliente.py, trae la clase Cliente para poder usarla aquí

# Creamos los objetos y mostramos sus datos.
cliente_ana = Cliente("Ana", "RUT-DEMO-ANA", "ana@example.com", "+56912345678")
print(cliente_ana.nombre,cliente_ana.correo, cliente_ana.telefono)
Cliente_2 = Cliente("Cristopher", "RUT-DEMO-CRISTOPHER", "figueroacristopher@gmail.com", "+56993949002")
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

# S7-P06: las hijas también utilizan el constructor y las propiedades del padre.
# Precios de ejemplo en USD; dólar ficticio, todavía sin consulta a la API.
dolar_ejemplo = 950
paquete_tokio = PaqueteInternacional("Viaje a Tokio", 500)
paquete_caribe = Crucero("Crucero por el Caribe", 800, 7)
print("Nombre heredado en internacional:", paquete_tokio.nombre)
print("Nombre heredado en crucero:", paquete_caribe.nombre)
print("Precio por viajero heredado en crucero:", paquete_caribe.precio_por_viajero)
print("Dato propio del crucero, noches:", paquete_caribe.noches)

#Consultas sobre la clase PaqueteInternacional que hereda de la clase Paquete
paquete_argentina = PaqueteInternacional("Viaje a Argentina", 200000)
print("Nombre heredado en internacional:", paquete_argentina.nombre)
print("Precio por viajero en USD:", paquete_argentina.precio_por_viajero, "Precio total en CLP:", paquete_argentina.calcular_total(3, dolar_ejemplo))

# Consultas la clase Crucero que hereda de la clase Paquete
# con super() llama al constructor de la clase padre para inicializar nombre y precio.
# y luego guarda las noches en self.__noches; la propiedad noches permite leerlas.

print(paquete_caribe.nombre)              # Propiedad heredada
print(paquete_caribe.precio_por_viajero)   # Propiedad heredada
print(paquete_caribe.noches)              # Atributo añadido en Crucero

# Mismo nombre de método y mismos argumentos; cada clase aplica su cálculo.
print("Nacional, dos viajeros, CLP:", paquete_sur.calcular_total(2, dolar_ejemplo))
print("Internacional, dos viajeros, CLP:", paquete_tokio.calcular_total(2, dolar_ejemplo))
print("Crucero, dos viajeros, CLP:", paquete_caribe.calcular_total(2, dolar_ejemplo))

# El comprador y el viajero son objetos separados.
from viajero import Viajero
viajero = Viajero("Elena", "F12345678")
viajero.validar_pasaporte()
print("Viajero:", viajero.nombre, "Pasaporte:", viajero.pasaporte)
