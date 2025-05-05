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
            "zero": "0" * 32,
            "t0": "0" * 32,
            "t1": "0" * 32,
            "t2": "0" * 32,
            "t3": "0" * 32,
            "t4": "0" * 32,
            "t5": "0" * 32,
            "t6": "0" * 32,
            "t7": "0" * 32,
            "s0": "0" * 32,
            "s1": "0" * 32,
            "s2": "0" * 32,
            "s3": "0" * 32,
            "s4": "0" * 32,
            "s5": "0" * 32,
            "s6": "0" * 32,
            "s7": "0" * 32,
        }
        self.index_map = {
            "00000": "zero",
            "01000": "t0", "01001": "t1", "01010": "t2", "01011": "t3",
            "01100": "t4", "01101": "t5", "01110": "t6", "01111": "t7",
            "10000": "s0", "10001": "s1", "10010": "s2", "10011": "s3",
            "10100": "s4", "10101": "s5", "10110": "s6", "10111": "s7"
        }

    def set(self, reg_idx: str, value):
        """ Escribe el valor <value> en el registro <reg_idx>, si este es válido (es uno de los de arriba)
            Lanza una excepción IndexError si no es válida.
            
            Ejemplo: reg_idx: "1000" | value: "00...0010" (32 bits) 
                Almacenará en el registro 8 ($t0) un 2 en "binario".
        """
        if reg_idx not in self.index_map:
            raise IndexError(f"Registro inválido: {reg_idx}")
        if len(value) != 32 or not set(value).issubset({"0", "1"}):
            raise ValueError("El valor debe ser una cadena binaria de 32 bits.")
        reg_name = self.index_map[reg_idx]
        if reg_name == "zero":
            return  # zero es inmutable
        self.registers[reg_name] = value

    def get(self, reg_idx: str):
        """ Devuelve el valor actual de el registro <reg_idx> si este es válido (es uno de los de arriba)
            Lanza una excepción IndexError si no es válida 
            
            Ejemplo: reg_idx: "1001" --> value: "00...0011" (32 bits) 
                Devuelve del registro 9 ($t1) un 3 en "binario".
        """
        if reg_idx == "00000":  # El registro zero es especial
            return "0" * 32  # El valor del registro zero siempre es 0
        if reg_idx not in self.index_map:
            raise IndexError(f"Registro inválido: {reg_idx}")
        reg_name = self.index_map[reg_idx]
        return self.registers[reg_name]

    def reset(self):
        """ Pone todos los registros a cero """
        self.PC = "0" * 32
        for reg in self.registers:
            self.registers[reg] = "0" * 32

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
        with open(filename, "w") as f:
            f.write(f"PC {int(self.PC, 2)}\n")
            f.write(f"zero {int(self.registers['zero'], 2)}\n")
            for i in range(8):
                f.write(f"t{i} {int(self.registers[f't{i}'], 2)}\n")
            for i in range(8):
                f.write(f"s{i} {int(self.registers[f's{i}'], 2)}\n")