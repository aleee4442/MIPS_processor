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
            "mem_write": None,
            "mem_read": None,
            "mem_to_reg": None,
            "PCSrc": None,
        }
    
    def unidad_control(self, opcode: str, func: str):
        if opcode == "000000":  # Tipo R
            # Traducimos func a operación ALU
            if func == "100000":  # ADD
                alu_op = "add"
            elif func == "100010":  # SUB
                alu_op = "sub"
            elif func == "100100":  # AND
                alu_op = "and"
            elif func == "100101":  # OR
                alu_op = "or"
            elif func == "101010":  # SLT
                alu_op = "slt"
            else:
                raise Exception(f"Func no soportado: {func}")
            
            self.lineas_control.update({
                "reg_dst": 1,
                "alu_src": 0,
                "mem_to_reg": 0,
                "reg_write": 1,
                "mem_write": 0,
                "mem_read": 0,
                "PCSrc": 0,
                "alu_op": alu_op
            })
        
        elif opcode == "100011":  # LW
            self.lineas_control.update({
                "reg_dst": 0,
                "alu_src": 1,
                "mem_to_reg": 1,
                "reg_write": 1,
                "mem_write": 0,
                "mem_read": 1,
                "PCSrc": 0,
                "alu_op": "add"
            })

        elif opcode == "101011":  # SW
            self.lineas_control.update({
                "alu_src": 1,
                "reg_write": 0,
                "mem_write": 1,
                "mem_read": 0,
                "PCSrc": 0,
                "alu_op": "add"
            })

        elif opcode == "000100":  # BEQ
            self.lineas_control.update({
                "alu_src": 0,
                "reg_write": 0,
                "mem_write": 0,
                "mem_read": 0,
                "PCSrc": 1,
                "alu_op": "sub"  # Para comprobar igualdad
            })
        
        else:
            raise Exception(f"Opcode no soportado: {opcode}")
        
    def ALU(self, value1: str, value2: str):
        op = self.lineas_control["alu_op"]

        if op == "add":
            return value1 + value2
        elif op == "sub":
            return value1 - value2
        elif op == "and":
            return value1 & value2
        elif op == "or":
            return value1 | value2
        elif op == "slt":
            return 1 if value1 < value2 else 0
        else:
            raise Exception(f"Operación ALU no soportada: {op}")

    def load_program(self, instructions: str):
        """ Resetea toda la información propia de la ejecución anterior para 
            preparar la ejecución del nuevo programa (por ejemplo, resetea las
            líneas de control a None) y guarda las instrucciones del nuevo programa 
            en las primeras direcciones de la memoria 
        """
        self.memory = RAM()  # Nueva instancia para resetear memoria
        self.regs = Regs()   # Nueva instancia para resetear registros
        self.PC = 0          # Resetear el contador de programa

        # Resetear las líneas de control
        for value in self.lineas_control:
            self.lineas_control[value] = None

        # Cargar instrucciones en memoria (una por línea)
        for i, instr in enumerate(instructions):
            self.memory.store_word(i * 4, instr)  # MIPS usa direcciones múltiplos de 4

    def run_instrucion(self):
        """ Ejecuta la instrucción que indica el PC en cada momento.
            Esta función ha de ser capaz de:
             - Acceder a memoria y obtener la instrucción que toca (recibirá una cadena de bits)
             - Identificar el tipo de instrucción
             - Decodificar la instrucción usando el formato adecuado
             - Ejecutar correctamenente la instrucción, leyendo o escribiendo en memoria o registros
               si hiciera falta """
        # 1. Fetch: obtener la instrucción desde memoria usando el PC
        instr = self.memory.load_word(self.PC)
        
        # 2. Decode: extraer campos comunes (para tipo R, I, etc.)
        opcode = instr[0:6]

        if opcode == "000000":  # Tipo R
            rs = int(instr[6:11], 2)
            rt = int(instr[11:16], 2)
            rd = int(instr[16:21], 2)
            shamt = int(instr[21:26], 2)  # no lo usamos aún
            funct = instr[26:32]

            # 3. Unidad de control
            self.unidad_control(opcode, funct)

            # 4. Leer registros
            value1 = self.regs.read(rs)
            value2 = self.regs.read(rt)

            # 5. ALU
            result = self.ALU(value1, value2)

            # 6. Write-back (si reg_write está activado)
            if self.lineas_control["reg_write"]:
                dest = rd if self.lineas_control["reg_dst"] else rt
                self.regs.write(dest, result)

        else:  # Tipo I (LW, SW, BEQ)
            rs = int(instr[6:11], 2)
            rt = int(instr[11:16], 2)
            imm = int(instr[16:32], 2)
            if imm >= 2**15:  # Sign-extend
                imm -= 2**16

            self.unidad_control(opcode, "xxxxxx")  # func no se usa

            value1 = self.regs.read(rs)
            value2 = self.regs.read(rt)

            if opcode == "100011":  # LW
                addr = self.ALU(value1, imm)
                word = self.memory.load_word(addr)
                if self.lineas_control["reg_write"]:
                    self.regs.write(rt, word)

            elif opcode == "101011":  # SW
                addr = self.ALU(value1, imm)
                self.memory.store_word(addr, value2)

            elif opcode == "000100":  # BEQ
                alu_result = self.ALU(value1, value2)
                if alu_result == 0:  # Son iguales
                    self.PC += 4 + (imm << 2)  # Branch tomado
                    return  # ¡Importante! ya actualizamos PC, salimos
            
        # 7. Avanzar PC por defecto
        self.PC += 4


    def run(self):
        """ Ejecuta el programa cargado desde el punto de ejecución actual, 
            indicado por el PC, hasta el final """
        try:
            while True:
                instr = self.memory.load_word(self.PC)
                if instr is None or len(instr) != 32:  # Por si llegamos al final o algo raro
                    break
                self.run_instrucion()
        except Exception as e:
            print(f"Error durante la ejecución: {e}")
    
    def dump(self, reg_filename, mem_filename):
        """ Llama a los dumps de registros y memoria con los nombres pertinentes"""
        self.regs.dump(reg_filename)
        self.memory.dump(mem_filename)


    