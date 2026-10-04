# Integración del equipo — 4 de octubre de 2026

## Qué se unió

Origen de personas/trabajadores: https://github.com/eliasreyes0726/agencia-viajes, commit 95bb795, comprobado antes de integrar. Se conservaron sus setters, jerarquías y métodos de rol, adaptando imports a la carpeta plana que usamos durante el aprendizaje. No se copió la lista de dependencias: ninguno de estos archivos usa requests todavía.

Se conservaron nuestros paquetes, fórmulas de práctica, datos de contacto y operaciones cambiar_nombre/correo/telefono. Los comentarios históricos de Cliente pueden consultarse en commits anteriores; el archivo actual describe la clase integrada.

## Cambios que ambos deben conocer

1. Cliente ahora hereda Persona. Su constructor común es Cliente(nombre, rut, correo, telefono). Reemplaza tanto nuestro constructor antiguo de tres datos como Cliente(nombre, rut, pasaporte) del compañero.
2. Nombre y RUT se inicializan mediante super y setters de Persona. cambiar_nombre usa el setter heredado: un nombre inválido se rechaza sin perder el anterior. La regla de dos caracteres es una decisión didáctica heredada del compañero, no una exigencia confirmada del profesor.
3. Cliente no tiene pasaporte. Viajero(nombre, pasaporte=None) lo conserva de forma independiente. No se obliga a todo viajero a tener RUT.
4. Vacío, espacios y None representan ausencia de pasaporte. Puede existir un viajero sin ese dato para un viaje nacional. validar_pasaporte() rechaza la ausencia cuando se necesite; la futura confirmación internacional deberá llamarlo para cada viajero. No existe todavía un proceso de confirmación.
5. Se retiró la regla de 6 a 12 caracteres, no confirmada por el guion. F12345678 se acepta. La validación actual no verifica autenticidad, país ni vencimiento.
6. Trabajador sigue recibiendo nombre, rut, usuario, password_hash. Se conserva el atributo como almacenamiento de un hash que deberá generarse externamente. No se considera completada la autenticación. Un texto no vacío no se convierte en hash por asignarlo allí.
7. AgenteViajes y Administrador devuelven True/False para puede_atender_clientes. Aún falta aplicar permisos en operaciones reales; no se atribuyen funcionalidades de venta o pagos que todavía no existen.
8. Internacional y Crucero tienen cálculo convertido con cotización entregada como argumento. La API va después. El 10 % del crucero permanece como propuesta explícita, no requisito del profesor.

## Ejemplo de los nuevos datos

```python
from cliente import Cliente
from viajero import Viajero

comprador = Cliente("Ana", "RUT-DEMO", "ana@example.com", "123")
viajero = Viajero("Elena", "F12345678")
viajero.validar_pasaporte()
```

Comprador y viajero no se vinculan automáticamente. Esa relación se construirá en Reserva.

## Cómo tener los dos la misma versión

Usar como punto común la rama feature/desarrollo del repositorio YoungEneas369/Evaluaci-n_2. No copiar archivos sueltos encima de un avance no revisado ni mezclar los dos main.py.

Para el compañero, la forma más sencilla es clonar en una carpeta nueva, conservando su repositorio anterior:

```console
git clone --branch feature/desarrollo https://github.com/YoungEneas369/Evaluaci-n_2.git RutaSur-equipo
cd RutaSur-equipo/codigo_definitivo
python main.py
python -B -m unittest pruebas_integracion -v
```

La carpeta RutaSur-equipo debe ser nueva. Ambos deben comparar git rev-parse HEAD para confirmar el mismo commit. La IA de Elías debe leer primero este archivo y Contexto_Evaluación_2.md. No se ha modificado el repositorio ni el PC de Elías: él debe obtener la versión compartida.

Para continuar colaborando, acordar quién edita cada archivo. Si no tiene permisos sobre el repositorio común, puede proponer sus cambios mediante un fork/PR; no necesita compartir contraseñas.

## Comprobación y pendientes

Ocho pruebas automatizadas y main.py ejecutados correctamente. Cubren herencia de Cliente, contacto sin pasaporte, inicialización y cambios inválidos, validación de pasaporte ausente, indicadores de rol, tres precios, tipo de cambio requerido y noches de solo lectura. No son el guion P01-P19 completo.

Quedan pendientes reservas/detalles, cupos por proveedor y fecha, anticipo del 50 %, persistencia/CRUD, autenticación efectiva y API. La ausencia de pasaporte debe bloquear la confirmación internacional cuando esa operación exista.
