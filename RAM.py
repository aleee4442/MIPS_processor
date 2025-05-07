class RAM:
    """ Emula una memoria con direcciones de 32 bits y dirección a nivel de byte. 
        Es decir, una memoria de 4GB
        Tiene que ser capaz de:
            - Devolver el valor actual de una dirección de memoria 
            - Escribir el valor de cualquier dirección de memoria 
            - Imprimir la memoria a un fichero
        Las primeras 1000 direcciones de memoria se usarán para instrucciones, el 
        resto para datos
    """

    # TODO: Buscad una estructura de datos que almacene información para las direcciones a las que se ha
    # accedido con anterioridad. No seais brutos! Para esta práctica queremos algo que emule una memoria, 
    # no necesitais cargar de golpe "una memoria" de 4GB.

    def __init__(self):
        """ Inicializa algo, si hiciera falta """
        self.memory = {}

    def set(self, addr: str, value: str):
        """ Escribe el valor <value> en la direccion <addr>, si esta es valida (tiene 32 bits)
            Lanza una excepción IndexError si no es válida
        
            Tanto addr como value son representaciones en binario de 32 bits, por ejemplo:
                value = "00....0010" representa el 2 en binario.     
        """
        if not isinstance(addr, str) or len(addr) != 32 or not set(addr).issubset({"0", "1"}):
            raise IndexError("Dirección no válida. Debe ser una cadena binaria de 32 bits.")
        if not isinstance(value, str) or len(value) != 32 or not set(value).issubset({"0", "1"}):
            raise ValueError("Valor no válido. Debe ser una cadena binaria de 32 bits.")

        addr_int = int(addr, 2)
        self.memory[addr_int] = value

    def get(self, addr: str):
        """ Devuelve el valor actual de la dirección <addr> si esta es valida (tiene 32 bits).
            Lanza una excepción IndexError (raise IndexError...) si no es válida. Cuando se intente acceder a una 
            dirección válida que no haya sido escrita con anterioridad, el resultado a de ser 0 
        """
        if not isinstance(addr, str) or len(addr) != 32 or not set(addr).issubset({"0", "1"}):
            raise IndexError("Dirección no válida. Debe ser una cadena binaria de 32 bits.")
        dir_int = int(addr, 2)
        return self.memory.get(dir_int, "0" * 32)

    def reset(self):
        """ Limpia el estado de la memoria """
        self.memory.clear()

    def dump_instr(self, filename: str):
        """ Realiza un volcado de memoria al fichero <filename> del segmento de instrucciones.
            El formato ha de ser el siguiente:
            <addr> <value>
            <addr> <value> 
            ...
            
            Donde addr está en hexadecimal (es decir, de la forma 0x12345678) 
            y value será una cadena de 32 bits. """
        with open(filename, "w") as f:
            for addr in sorted(self.memory.keys()):
                if addr < 1000:  # Solo instrucciones (en el rango de 0 a 999)
                    # Asegúrate de que el valor esté en formato de 32 bits
                    value = self.memory[addr].zfill(32)
                    f.write(f"{hex(addr)} {value}\n")

    def dump_data(self, filename: str):
        """ Realiza un volcado de memoria al fichero <filename> del segmento de datos.
            El formato ha de ser el siguiente:
            <addr> <value>
            <addr> <value> 
            ...
            
            Donde addr está en hexadecimal (es decir, de la forma 0x12345678) 
            y value puede ser un número cualquiera. """
        with open(filename, "w") as f:
            for addr in sorted(self.memory.keys()):
                if addr >= 1000:  # Solo datos (direcciones >= 1000)
                    # Asegúrate de que el valor esté en formato de 32 bits
                    value = self.memory[addr].zfill(32)
                    f.write(f"{hex(addr)} {value}\n")


