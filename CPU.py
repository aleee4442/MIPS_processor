from RAM import RAM
from regs import Regs

class CPU:

    def __init__(self):
        """ Inicializa algo, si hiciera falta """
        # TODO: Rellenad el método
        memory = RAM()
        regs = Regs()
        # Líneas de control
        self.lineas_control = {
            "reg_dst": None,
            "reg_write": None,
            "alu_src": None,
            "alu_op": None,
            "mem_read": None,
            "mem_write": None,
            "mem_to_reg": None,
            "branch": None,
        }
    
    def unidad_control(self, opcode: str, func: str):
        """ Dado el opcode y funct de una función, activar las lineas 
        de control para el correcto desarrollo de la instrucción
        """
        # TODO: Rellenad el método
        pass
        
    def ALU(self, value1: str, value2: str):
        """ Dado dos valores de entrada y la operación de la ALU se calcula y 
        devuelve el resultado.
        (RECUERDA: La operación de la ALU viene dada por self.lineas_control["alu_op"])
        """
        # TODO: Rellenad el método
        pass

    def load_program(self, instructions: str):
        """ Resetea toda la información propia de la ejecución anterior para 
            preparar la ejecución del nuevo programa (por ejemplo, resetea las
            líneas de control a None) y guarda las instrucciones del nuevo programa 
            en las primeras direcciones de la memoria 
        """
        # TODO: Rellenad el método
        pass

    def run_instrucion(self):
        """ Ejecuta la instrucción que indica el PC en cada momento.
            Esta función ha de ser capaz de:
             - Acceder a memoria y obtener la instrucción que toca (recibirá una cadena de bits)
             - Identificar el tipo de instrucción
             - Decodificar la instrucción usando el formato adecuado
             - Ejecutar correctamenente la instrucción, leyendo o escribiendo en memoria o registros
               si hiciera falta """
        # TODO: Rellenad el método
        pass

    def run(self):
        """ Ejecuta el programa cargado desde el punto de ejecución actual, 
            indicado por el PC, hasta el final """
        # TODO: Rellenad el método
        pass
    
    def dump(self, reg_filename, mem_filename):
        """ Llama a los dumps de registros y memoria con los nombres pertinentes"""
        # TODO: Rellenad el método
        pass


    