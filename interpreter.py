'''
интерпретатор, который выполняет команды виртуальной машины,
загруженные из бинарного файла, и сохраняет состояние памяти в файл YAML
'''
import struct # интерпретировать бинарные данные
import yaml # для записи результатов в формате YAML
import math # для выполнения математических операций

# Словарь для команд и их бинарных представлений
command_dict = {
    'load_constant': 0xBA,  # Код команды для load_constant
    'read_memory': 0x6D,  # Код команды для read_memory
    'write_memory': 0xDF,  # Код команды для write_memory
    'sqrt': 0x38  # Код команды для sqrt
}


def execute_program(input_file, output_file):
    # Массив памяти УВМ (например, 128 ячеек памяти)
    memory = [0] * 128  # Инициализируем память (128 ячеек)

    # Открывает бинарный файл (input_file) в режиме чтения (rb) и загружает содержимое в переменную program
    with open(input_file, 'rb') as f:
        program = f.read()

    pc = 0  # Программный счётчик (указатель на текущую команду)

    while pc < len(program):
        opcode = program[pc] # Читает код операции (opcode) — первый байт текущей инструкции

        if opcode == command_dict['load_constant']: # Распознает load_constant по коду 0xBA
            # Команда load_constant
            B = struct.unpack('>H', program[pc + 1:pc + 3])[0]  # Читаем 2 байта (B)
            C = program[pc + 3]  # Читаем 1 байт (C)
            memory[C] = B  # Загружаем значение B в память по адресу C
            pc += 4  # Переходим к следующей команде

        elif opcode == command_dict['sqrt']:
            # Команда sqrt
            B = program[pc + 1]  # Читаем адрес B (1 байт)
            C = program[pc + 2]  # Читаем адрес C (1 байт)
            if memory[B] >= 0:  # Проверка, что значение для sqrt не отрицательное
                memory[C] = int(math.sqrt(memory[B]))  # Вычисляем квадратный корень и записываем в память
            pc += 3  # Переходим к следующей команде

        elif opcode == command_dict['read_memory']:
            # Команда read_memory
            B = program[pc + 1]  # Читаем адрес B (1 байт)
            C = program[pc + 2]  # Читаем адрес C (1 байт)
            memory[C] = memory[B]  # Читаем значение из памяти по адресу B и записываем в память по адресу C
            pc += 3  # Переходим к следующей команде

        elif opcode == command_dict['write_memory']:
            # Команда write_memory
            B = struct.unpack('>H', program[pc + 1:pc + 3])[0]  # Читаем 2 байта (B)
            C = program[pc + 3]  # Читаем 1 байт (C)
            memory[B] = memory[C]  # Записываем значение из памяти по адресу C в память по адресу B
            pc += 4  # Переходим к следующей команде

        else: # Обработка неизвестной команды
            raise ValueError(f"Неизвестный код операции: {opcode}")

    # Запись результата в YAML файл
    write_memory_to_yaml(memory, output_file)


def write_memory_to_yaml(memory, filename):
    # Фильтруем только те ячейки памяти, которые были изменены (не равны нулю)
    filtered_memory = [value for value in memory if value != 0]

    with open(filename, 'w') as yaml_file: # Сохраняет отфильтрованную память в формате YAML
        yaml.dump({'memory': filtered_memory}, yaml_file)

    #print(f"Результат выполнения программы записан в {filename}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_file> <output_file>")
        sys.exit(1)  # Завершаем программу, если аргументы не переданы правильно

    input_file = sys.argv[1]  # Первый аргумент: путь к входному бинарному файлу
    output_file = sys.argv[2]  # Второй аргумент: путь к выходному YAML файлу

    execute_program(input_file, output_file)

