# Домашние задания в ветке master

**Олейников Артемий ИКБО-30-23**
# Домашнее задание №1
[Эмулятор + Тест]([(https://github.com/Andrax53/ConfUprav1/)])

 # Учебная Виртуальная Машина (УВМ) Задание 4

Этот проект включает в себя ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Ассемблер преобразует текстовую программу в бинарный файл, а интерпретатор выполняет команды из этого бинарного файла.

## Структура проекта
hw2/

├── assembler.py

├── interpreter.py

├── test_program.asm

├── README.md


## Установка

1. Убедитесь, что у вас установлен Python 3.x.
2. Создайте виртуальное окружение (опционально):
   ```sh
   python -m venv venv
   source venv/bin/activate  # Для Unix/MacOS
   .\venv\Scripts\activate  # Для Windows
## Использование
Ассемблирование программы
Ассемблер принимает на вход файл с текстом исходной программы и генерирует бинарный файл.


python hw4/assembler.py hw4/test_program.asm hw4/binary_output.bin hw4/log.yaml

hw4/test_program.asm: Входной файл с текстом исходной программы.

hw4/binary_output.bin: Выходной бинарный файл.

hw4/log.yaml: Файл-лог в формате YAML.

## Интерпретация программы

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет значения из диапазона памяти УВМ в файл-результат.


python hw4/interpreter.py hw4/binary_output.bin hw4/result.yaml 0 4

hw4/binary_output.bin: Входной бинарный файл.

hw4/result.yaml: Выходной файл-результат в формате YAML.

0 4: Диапазон памяти для сохранения (от 0 до 4).

## Пример тестовой программы

Пример тестовой программы, которая выполняет поэлементно операцию bswap() над вектором длины 5 и записывает результат в исходный вектор:



LOAD_CONST 0 0x12345678

LOAD_CONST 1 0x9ABCDEF0

LOAD_CONST 2 0x12345678

LOAD_CONST 3 0x9ABCDEF0

LOAD_CONST 4 0x12345678

BSWAP 0 0

BSWAP 1 1

BSWAP 2 2

BSWAP 3 3
BSWAP 4 4

## Пример выходного файла result.yaml

memory:

  0: 78563412
  
  1: 3735928536
  
  2: 78563412
  
  3: 3735928536
  
  4: 78563412
