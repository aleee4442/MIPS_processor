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

        elif opcode == "001000":  # ADDI
            self.lineas_control.update({
                "reg_dst": 0,
                "alu_src": 1,
                "mem_to_reg": 0,
                "reg_write": 1,
                "mem_write": 0,
                "mem_read": 0,
                "PCSrc": 0,
                "alu_op": "add"
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

    def load_program(self, instructions: list[str]):
        """
        Carga una lista de instrucciones binarias en la memoria de instrucciones.
        También reinicia el PC y cualquier estado necesario.
        """
        # Resetear estado anterior
        self.PC = 0
        self.lineas_control = {
            "reg_dst": None,
            "alu_op": None,
            "alu_src": None,
            "mem_to_reg": None,
            "reg_write": None,
            "mem_read": None,
            "mem_write": None,
            "branch": None,
        }

        # Cargar instrucciones en memoria
        for i, instr in enumerate(instructions):
            address = format(i, '032b')  # Dirección binaria de 32 bits
            self.memory.set(address, instr)  # Usar set() en lugar de write()

    def run_instrucion(self):
        """ Ejecuta la instrucción que indica el PC en ese momento. """
        #self.regs.initialize_regs()
        addr_bin = format(self.PC, '032b')
        instr = self.memory.get(addr_bin)

        if instr is None or len(instr) != 32:
            raise Exception("Instrucción inválida o fin del programa.")

        print(f"Instr: {instr}")

        opcode = instr[0:6]
        funct = instr[26:32]

        print(f"Func: {funct}")
        self.unidad_control(opcode, funct)

        if opcode == "000000" and funct == "000000":
            print("NOP: Avanzando PC.")
            self.PC += 1
            return

        if opcode == "000000":  # Tipo R
            rs = instr[6:11]
            rt = instr[11:16]
            rd = instr[16:21]  # <-- Mantener en binario de 5 bits

            print(f"rs: {rs}, rt: {rt}, rd: {rd}")
            
            # Verificar los valores de los registros antes de la operación
            print(f"Antes de ejecutar ALU: $t0 = {self.regs.get('01000')}, $t1 = {self.regs.get('01001')}")

            value1 = self.regs.get(rs)
            value2 = self.regs.get(rt)

            result = self.ALU(value1, value2)

            print(f"Resultado ALU: {result}")

            if self.lineas_control["reg_write"]:
                dest = rd if self.lineas_control["reg_dst"] else rt
                self.regs.set(dest, result)  # <-- Actualiza el registro de destino
                print(f"Registro {dest} actualizado a: {self.regs.get(dest)}")
        elif opcode in ["100011", "101011"]:  # LW o SW (tipo I)
            rs = instr[6:11]
            rt = instr[11:16]
            offset = int(instr[16:32], 2)

            base_addr = int(self.regs.get(rs), 2)
            mem_addr = base_addr + offset
            mem_addr_bin = format(mem_addr, '032b')

            if self.lineas_control["mem_read"]:  # LW
                value = self.memory.get(mem_addr_bin)
                if self.lineas_control["reg_write"]:
                    self.regs.set(int(rt, 2), value)

            elif self.lineas_control["mem_write"]:  # SW
                value = self.regs.get(rt)
                self.memory.set(mem_addr_bin, value)        
                print(f"Memoria en {mem_addr_bin} actualizada a: {value}")
        elif opcode == "000100":  # BEQ
            rs = instr[6:11]
            rt = instr[11:16]
            offset = int(instr[16:32], 2)

            value1 = self.regs.get(rs)
            value2 = self.regs.get(rt)
            result = self.ALU(value1, value2)

            if result == format(0, '032b'):  # son iguales
                self.PC += offset
                return
        # Avanza PC si no ha saltado
        elif opcode == '001000':  # ADDI
            rs_bin = instr[6:11]
            rt_bin = instr[11:16]
            imm_bin = instr[16:]

            rs_val = self.regs.get(rs_bin)
            imm_val = int(imm_bin, 2)
            rs_int = int(rs_val, 2)

            result = rs_int + imm_val
            result_bin = format(result, '032b')

            self.regs.set(rt_bin, result_bin)

        self.PC += 4
        self.regs.set("00001", format(self.PC, '032b'))  # Usa el índice binario para PC        print(f"PC = {self.PC}")
        #print(f"PC = {self.regs.get('PC')}")
        print(f"PC = {self.PC}")

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
        self.memory.dump_instr(mem_filename)   # si quieres volcar instrucciones
        # o
        self.memory.dump_data(mem_filename)    # si quieres volcar datos
        # o ambos:
        self.memory.dump_instr("instr_dump.txt")
        self.memory.dump_data(mem_filename)

