from RAM import RAM
from regs import Regs

class CPU:

    def __init__(self):
        """ Inicializa algo, si hiciera falta """
        # TODO: Rellenad el método
        self.PC = 0
        self.memory = RAM()  # Asigna la memoria como atributo de la clase
        self.regs = Regs()
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
        print(f"Unidad de control recibida: opcode = {opcode}, func = {func}")  # Imprime opcode y func
        print(f"Ejecutando unidad_control con opcode: {opcode}, func: {func}")
        if opcode == "000000":  # Tipo R
            # Si el func es "000000", es un NOP (No Operación)
            if func == "000000":
                print("NOP detected, no operation performed.")
                return  # No hacer nada, simplemente salimos
            
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
        # Convertir las cadenas binarias a enteros
        value1_int = int(value1, 2)
        value2_int = int(value2, 2)

        op = self.lineas_control["alu_op"]
        
        if op == "add":
            return format(value1_int + value2_int, '032b')
        elif op == "sub":
            return format(value1_int - value2_int, '032b')
        elif op == "and":
            return format(value1_int & value2_int, '032b')
        elif op == "or":
            return format(value1_int | value2_int, '032b')
        elif op == "slt":
            return format(1 if value1_int < value2_int else 0, '032b')
        else:
            raise Exception(f"Operación ALU no soportada: {op}")

    def load_program(self, instructions: str):
        """ Resetea toda la información propia de la ejecución anterior para 
            preparar la ejecución del nuevo programa (por ejemplo, resetea las
            líneas de control a None) y guarda las instrucciones del nuevo programa 
            en las primeras direcciones de la memoria 
        """
       # 1. Fetch: obtener la instrucción desde memoria usando el PC
        addr_bin = format(self.PC, '032b')
        instr = self.memory.get(addr_bin)
        
        print(f"Instr: {instr}")  # Imprime la instrucción cargada

        # 2. Decode: extraer campos comunes (para tipo R, I, etc.)
        opcode = instr[0:6]
        funct = instr[26:32]  # Obtenemos 'func'

        print(f"Func: {funct}")  # Imprime el valor de funct antes de llamar a unidad_control

        if opcode == "000000":  # Tipo R
            rs = instr[6:11]  # Esto será una cadena de 5 bits
            rt = instr[11:16]  # Esto será una cadena de 5 bits
            rd = int(instr[16:21], 2)
            shamt = int(instr[21:26], 2)  # No lo usamos aún
            funct = instr[26:32]

            # 3. Unidad de control
            self.unidad_control(opcode, funct)  # Aquí se lanza la excepción si no es válido
            print(f"rs: {rs}, rt: {rt}")  # Verifica que rs y rt sean cadenas de 5 bits
            # 4. Leer registros
            value1 = self.regs.get(rs)
            value2 = self.regs.get(rt)

            # 5. ALU
            result = self.ALU(value1, value2)

            # 6. Write-back (si reg_write está activado)
            if self.lineas_control["reg_write"]:
                dest = rd if self.lineas_control["reg_dst"] else rt
                self.regs.write(dest, result)


    def run(self):
        """ Ejecuta el programa cargado desde el punto de ejecución actual, 
            indicado por el PC, hasta el final """
        try:
            while True:
                addr_bin = format(self.PC, '032b')
                instr = self.memory.get(addr_bin)
                if instr is None or len(instr) != 32:  # Por si llegamos al final o algo raro
                    break
                self.run_instrucion()
        except Exception as e:
            print(f"Error durante la ejecución: {e}")
    
    def dump(self, reg_filename, mem_filename):
        """ Llama a los dumps de registros y memoria con los nombres pertinentes"""
        self.regs.dump(reg_filename)
        self.memory.dump(mem_filename)


    