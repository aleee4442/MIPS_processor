# Ejemplo de uso
from CPU import CPU

print("Iniciando simulación...")

cpu = CPU()

# Lectura de instrucciones
with open('sample_program.txt', 'r') as program_file:
    instructions = program_file.read().splitlines() 
cpu.load_program(instructions)

# Ejecutamos las instrucciones una a una
for i in range(len(instructions)):
    cpu.run_instrucion()
    # Aquí, vía pdb o de otra forma, podemos verificar que las instrucciones se han ejecutado bien

# Volcado para ver el resultado al final de la ejecución
cpu.dump("memory_dump.txt", "registers_dump.txt")

