'''
ассемблер для преобразования текстового описания инструкций (в файле .asm)
в бинарный файл и логирование данных в формате YAML
'''
import struct # упаковывать и распаковывать данные в бинарном формате
import sys # для работы с аргументами командной строки
import yaml # для работы с YAML-файлами

# Словарь для команд и их бинарных представлений
command_dict = {
    'load_constant': 0xBA,  # Код команды для load_constant
    'read_memory': 0x6D,    # Код команды для read_memory
    'write_memory': 0xDF,   # Код команды для write_memory
    'sqrt': 0x38            # Код команды для sqrt
}


'''
Функция берет текстовый файл с инструкциями, преобразует его в бинарный файл, 
а также создает YAML-файл с логами
'''
def assemble_program(input_file, output_file, log_file):
    with open(input_file, 'r') as f: # Чтение входного файла
        lines = f.readlines()

    binary_program = bytearray() # пустой массив байтов, в который будет записан результирующий бинарный код
    log_data = {} # словарь для хранения логов в YAML

    for line in lines:
        line = line.strip() # Удаляет пробелы в начале и конце строки
        if not line or line.startswith('#'):
            continue # Пропускает пустые строки и строки с комментариями

        # Разделение команды и параметров
        parts = line.split()
        command = parts[0]
        params = parts[1:]

        if command == 'load_constant':
            # Парсит параметры: A, B, C
            A = int(params[0])
            B = int(params[1])
            C = int(params[2])
            # Запись команды load_constant: [A, B, C]
            binary_program.append(command_dict[command])  # Добавляет код команды (0xBA) в binary_program
            binary_program.extend(struct.pack('>H', B))   # Упаковывает B (число) в 2 байта в формате Big-Endian (>H) и добавляет к binary_program
            binary_program.append(C)                       # Добавляет C как 1 байт
            log_data[f'{command} {B} {C}'] = [command_dict[command], B, C] # Логирует команду в log_data

        elif command == 'read_memory':
            A = int(params[0])
            B = int(params[1])
            C = int(params[2])
            # Запись команды read_memory: [A, B, C]
            binary_program.append(command_dict[command])  # Код команды
            binary_program.append(B)                       # Адрес B (1 байт)
            binary_program.append(C)                       # Адрес C (1 байт)
            log_data[f'{command} {B} {C}'] = [command_dict[command], B, C]

        elif command == 'write_memory':
            A = int(params[0])
            B = int(params[1])
            C = int(params[2])
            # Запись команды write_memory: [A, B, C]
            binary_program.append(command_dict[command])  # Код команды
            binary_program.extend(struct.pack('>H', B))   # Адрес B (2 байта)
            binary_program.append(C)                       # Адрес C (1 байт)
            log_data[f'{command} {B} {C}'] = [command_dict[command], B, C]

        elif command == 'sqrt':
            A = int(params[0])
            B = int(params[1])
            C = int(params[2])
            # Запись команды sqrt: [A, B, C]
            binary_program.append(command_dict[command])  # Код команды
            binary_program.append(B)                       # Адрес B (1 байт)
            binary_program.append(C)                       # Адрес C (1 байт)
            log_data[f'{command} {B} {C}'] = [command_dict[command], B, C]

        # Неизвестные команды
        else:
            print(f"Unknown command: {command}")
            continue

    # Запись бинарного файла
    with open(output_file, 'wb') as f:
        f.write(binary_program) # Записывает массив байтов binary_program

    # Запись логов в YAML файл
    with open(log_file, 'w') as f:
        yaml.dump(log_data, f, default_flow_style=False) # Записывает данные log_data в формате YAML

    #print(f"The binary file is written to {output_file}")
    #print(f"The log is recorded in {log_file}")


if __name__ == '__main__':
    # Проверяет, что программа запускается с тремя аргументами
    # входной файл, выходной бинарный файл и файл логов
    if len(sys.argv) != 4:
        print("Используй: python assembler.py input.asm output.bin log.yaml")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    # Передает их в функцию assemble_program
    assemble_program(input_file, output_file, log_file)
