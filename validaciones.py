"""Validaciones pequeñas compartidas por los modelos y la interfaz."""
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from excepciones import DatosInvalidosError


def texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise DatosInvalidosError(f'{campo} no puede estar vacío.')
    return valor.strip()


def numero_decimal(valor, campo, permitir_cero=False):
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError):
        raise DatosInvalidosError(f'{campo} debe ser un número.') from None
    if not numero.is_finite() or numero < 0 or (numero == 0 and not permitir_cero):
        raise DatosInvalidosError(f'{campo} debe ser positivo y finito.')
    return numero


def entero(valor, campo, permitir_cero=False):
    numero = numero_decimal(valor, campo, permitir_cero)
    if numero != numero.to_integral_value():
        raise DatosInvalidosError(f'{campo} debe ser entero.')
    return int(numero)


def pesos(valor):
    return int(Decimal(str(valor)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def fecha_iso(valor):
    try:
        return date.fromisoformat(valor).isoformat()
    except (TypeError, ValueError):
        raise DatosInvalidosError('La fecha debe ser válida y usar AAAA-MM-DD.') from None
