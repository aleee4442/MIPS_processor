class Regs:
    """ Emula una banco de registros
    Tiene que ser capaz de:
        - Devolver el valor actual de cualquier registro 
        - Escribir el valor de cualquier registro
        - Imprimir el estado del banco de registros
    Este banco de registros simplificado debe contener, exactamente, los registros:
        - PC (contiene la dirección de la siguiente instrucción que se ejecutará)
        - zero (registro 0)
        - t0 a t7 (registros del [8-15])
        - s0 a s7 (registros del [16-23])
        - Cualquier otro intento de acceder a otro registro debería dar un error.
    """

    def __init__(self):
        """ Inicializa algo, si hiciese falta """
        # TODO: Rellenad la funcion
        self.PC = None
        self.registers = {
            # TODO: añadir los registros necesarios
            # Se propone usar un diccionario pero podéis
            # cambiarlo con vuestra lógica (por ejemplo, usando
            # una lista)
        }
        pass

    def set(self, reg_idx: str, value):
        """ Escribe el valor <value> en el registro <reg_idx>, si este es válido (es uno de los de arriba)
            Lanza una excepción IndexError si no es válida.
            
            Ejemplo: reg_idx: "1000" | value: "00...0010" (32 bits) 
                Almacenará en el registro 8 ($t0) un 2 en "binario".
        """
        # TODO: Rellenad la funcion
        pass

    def get(self, reg_idx: str):
        """ Devuelve el valor actual de el registro <reg_idx> si este es válido (es uno de los de arriba)
            Lanza una excepción IndexError si no es válida 
            
            Ejemplo: reg_idx: "1001" --> value: "00...0011" (32 bits) 
                Devuelve del registro 9 ($t1) un 3 en "binario".
        """
        # TODO: Rellenad la funcion
        pass        

    def reset(self):
        """ Pone todos los registros a cero """
        # TODO: Rellenad la funcion
        pass

    def dump(self, filename):
        """ Realiza un volcado del estado de los registros  al fichero <filename> 
        El formato ha de ser el siguiente:
        PC <value>
        zero <value>
        t0 <value> 
        ...
        t1 <value>
        s0 <value>
        ...
        s7 <value>
          
        Donde value es un número cualquiera """
        # TODO: Rellenad la funcion
        pass