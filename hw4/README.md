# Задание 4

# Учебная Виртуальная Машина (УВМ)

## Описание
Данный проект представляет собой реализацию учебной виртуальной машины (УВМ), включающую в себя ассемблер и интерпретатор. УВМ поддерживает набор базовых команд для работы с памятью и регистрами, а также специальные операции, такие как byte swap.

## Структура проекта
- `uvm.py` - основной файл с реализацией ассемблера и интерпретатора
- `test_vm.py` - модульные тесты
- `test_program.asm` - пример программы на ассемблере
- `program.log` - лог-файл с информацией о скомпилированных инструкциях
- `result.yaml` - файл с результатами работы программы

## Система команд
1. `load_const` - загрузка константы в регистр
   - Формат: `load_const адрес константа`
   - Размер: 4 байта
   - Тест: A=82, B=352, C=346
   - Бинарный код: 0x52, 0xB0, 0xD0, 0x0A

2. `read_memory` - чтение из памяти
   - Формат: `read_memory цель адрес смещение`
   - Размер: 6 байт
   - Тест: A=19, B=511, C=112, D=71
   - Бинарный код: 0x93, 0xFF, 0x80, 0x83, 0x23, 0x00

3. `write_memory` - запись в память
   - Формат: `write_memory адрес смещение источник`
   - Размер: 6 байт
   - Тест: A=31, B=27, C=148, D=883
   - Бинарный код: 0x9F, 0x0D, 0xA0, 0x64, 0x6E, 0x00

4. `bswap` - операция byte swap
   - Формат: `bswap источник цель`
   - Размер: 4 байта
   - Тест: A=22, B=810, C=188
   - Бинарный код: 0x16, 0x95, 0xE1, 0x05

## Использование

### Установка зависимостей
```bash
pip install pytest pyyaml
```

### Запуск ассемблера и интерпретатора
```bash
python uvm.py <входной_файл.asm> <выходной_файл.bin> <лог_файл.log> <результат.yaml> <диапазон_памяти>
```

Например:
```bash
python uvm.py test_program.asm output.bin program.log result.yaml 100,5
```

Где:
- `test_program.asm` - исходный файл с программой
- `output.bin` - скомпилированный бинарный файл
- `program.log` - лог-файл с информацией об инструкциях
- `result.yaml` - файл с результатами работы программы
- `100,5` - диапазон памяти (начальный адрес и длина)

### Запуск тестов
```bash
python -m pytest test_vm.py -v
```

## Формат файлов

### program.log
Содержит информацию о скомпилированных инструкциях в формате YAML:
```yaml
instructions:
  - command: имя_команды
    bytes: [байты_инструкции]
```

### result.yaml
Содержит значения из указанного диапазона памяти в формате YAML:
```yaml
memory_values:
  100: '0x12345678'
  101: '0x12345678'
  102: '0x12345678'
  103: '0x12345678'
  104: '0x12345678'
```


## Формат лог-файла
Лог-файл создается в формате YAML и содержит информацию о каждой инструкции:
- Название инструкции
- Аргументы
- Бинарное представление

## Особенности реализации
- Поддержка меток для организации циклов и переходов
- Различные размеры инструкций (4 или 6 байт)
- Битовая адресация полей инструкций
- Порядок байтов: little-endian

## Ограничения
- Максимальное количество регистров: 16
- Размер памяти определяется при создании интерпретатора
- Не поддерживаются комментарии внутри инструкций
