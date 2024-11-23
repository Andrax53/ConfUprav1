 # Задание 4
 # Учебная Виртуальная Машина (УВМ)

Этот проект реализует ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Программа принимает текстовые команды, ассемблирует их в бинарный формат, выполняет команды и логирует результаты.

## Установка

1. Убедитесь, что у вас установлен Python 3.x.
2. Скачайте или клонируйте репозиторий:

```sh
git clone https://github.com/yourusername/uvm.git
cd uvm
```
Установите необходимые зависимости:
```sh
pip install -r requirements.txt
```
## Использование
Формат команд
Команды для УВМ записываются в текстовом файле. Пример команд:

```sh
move 352 346
read 511 112 71
write 27 148 883
bswap 810 188
```
## Запуск программы
Для запуска программы используйте следующую команду:
```sh
python uvm.py <input_file> <assembler_log> <interpreter_result>
```
<input_file>: Путь к текстовому файлу с командами.
<assembler_log>: Путь к файлу лога ассемблера (YAML формат).
<interpreter_result>: Путь к файлу результатов интерпретатора (YAML формат).
## Пример
```sh
python run_uvm.py test_program.txt assembler_log.yaml interpreter_result.yaml
```
## Пример содержимого файлов логов
assembler_log.yaml:
```sh
- op: move
  args: [352, 346]
- op: read
  args: [511, 112, 71]
- op: write
  args: [27, 148, 883]
- op: bswap
  args: [810, 188]
interpreter_result.yaml:


- op: move
  A: '0x52'
  B: '0x160'
  C: '0x15A'
- op: read
  A: '0x13'
  B: '0x1FF'
  C: '0x70'
  D: '0x47'
- op: write
  A: '0x1F'
  B: '0x1B'
  C: '0x94'
  D: '0x373'
- op: bswap
  A: '0x16'
  B: '0x32A'
  C: '0xBC'
```
## Тестирование
Для запуска модульных тестов используйте следующую команду:

```sh
python -m unittest test_uvm.py
```
