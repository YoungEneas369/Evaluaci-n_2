# RutaSur — versión común del equipo

Integración del 4 de octubre de 2026. Código en aprendizaje, todavía no entrega completa.

## Versión compartida

Usar la carpeta codigo_definitivo de la rama feature/desarrollo en:
https://github.com/YoungEneas369/Evaluaci-n_2/tree/feature/desarrollo/codigo_definitivo

Esta carpeta integra los paquetes de Cristopher con las personas y trabajadores de Elías (origen: eliasreyes0726/agencia-viajes, commit 95bb795). El resto del repositorio contiene el proyecto anterior.

## Ejecutar

Python 3.10 o posterior; no se necesitan librerías externas en esta etapa. Abrir una terminal en esta carpeta:

```console
python main.py
python -B -m unittest pruebas_integracion -v
```

## Archivos

- persona.py: nombre y RUT con setters y validación básica.
- cliente.py: comprador; hereda Persona y conserva correo y teléfono.
- viajero.py: nombre y pasaporte de quien viaja.
- trabajador.py, agente_viajes.py, administrador.py: jerarquía aportada por Elías.
- paquetesAgencia.py: Paquete, clase padre.
- paquete_nacional.py, paquete_internacional.py, crucero.py: herencia y cálculos propios.
- main.py: ejemplos de uso; precios, cotización y RUT de demostración.
- pruebas_integracion.py: ocho comprobaciones de compatibilidad y comportamiento.

Consultar INTEGRACION_EQUIPO.md para las correcciones y cómo obtener exactamente esta versión. Contexto_Evaluación_2.md indica cómo retomar el aprendizaje. PASO_A_PASO.md conserva los ejercicios históricos.

## Límites actuales

No hay reservas, base de datos, menú, autenticación funcional ni consulta real a la API. password_hash solo almacena un valor suministrado: no genera ni verifica un hash. Los indicadores de rol todavía no autorizan acciones reales.

El dólar 950 es ficticio. El 10 % del crucero es un supuesto didáctico pendiente de confirmar. Nacional usa CLP; internacional y crucero usan precios por viajero en USD. La cantidad se recibe para calcular, no se guarda en Paquete. Las noches aún no se validan; son de solo lectura.

El RUT solo se comprueba como texto no vacío, sin dígito verificador. Los RUT de main.py son marcadores de demostración. Correo, teléfono, precios y cantidad todavía requieren validaciones posteriores. El pasaporte se comprueba como dato presente; no es una comprobación documental oficial.
