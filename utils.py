def decimal_a_binario(decimal: int, length: int) -> str:
    """
    # TODO: Implementa una función que convierta un número decimal POSITIVO a su representación binaria de longitud fija.
    La función debe:
      - Validar que 'decimal' sea un número positivo.
      - Convertir 'decimal' a binario sin el prefijo "0b".
      - Rellenar con ceros a la izquierda hasta alcanzar la longitud 'length'.
      - Lanzar un ValueError (raise ValueError(...)) si la representación binaria 
      del número no cabe en 'length' bits.
    """

def decimal_a_binario_con_signo(decimal: int, length: int) -> str:
    """
    # TODO: Implementa una función que convierta un número decimal, que puede ser negativo, 
    a su representación binaria usando extensión del signo.
    La función debe:
      - Para números positivos, comportarse como la función decimal_a_binario (rellenado con ceros).
      - Para números negativos, obtener la representación binaria en Ca2 
      - Lanzar un ValueError (raise ValueError(...)) si la representación binaria 
      del número no cabe en 'length' bits.
    """

def binario_a_decimal(bin_string: str) -> int:
    """
    # TODO: Implementa una función que convierta una cadena en formato binario (sin signo) a un número decimal.
    La función debe:
      - Validar que 'bin_string' contenga solo los caracteres '0' y '1'.
      - Convertir la cadena binaria a su valor decimal.
      - Lanzar un ValueError si 'bin_string' no es una cadena binaria válida.
    """

def binario_a_decimal_con_signo(bin_string: str) -> int:
    """
    # TODO: Implementa una función que convierta una cadena binaria su valor decimal con signo.
    La representación del signo es Ca2.
    La función debe:
      - Interpretar la cadena: si es positivo o negativo.
      - Obtener su equivalente en decimal (los negativos se usa Ca2)
      - Lanzar un ValueError si la cadena no sigue el formato esperado.
    """
