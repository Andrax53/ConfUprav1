# Учебный конфигурационный язык

Этот проект реализует инструмент командной строки для преобразования текста из учебного конфигурационного языка в формат TOML. Инструмент обрабатывает однострочные комментарии, массивы, словари, объявление констант и вычисление константных выражений на этапе трансляции.

## Структура проекта
ConfUprav1/

├── hw3/

│   ├── config_parser.py

│   ├── test_config_parser.py

│   ├── example_config.txt

│   └── output.toml


# Установка

1. Убедитесь, что у вас установлен Python 3.x.
2. Создайте виртуальное окружение и активируйте его:

```sh
python -m venv .venv
.venv\Scripts\activate  # Для Windows
# или
source .venv/bin/activate  # Для macOS/Linux
```
Установите необходимые зависимости:
```sh
pip install toml
```

# Использование
## Парсинг конфигурационного файла и запись в TOML
Перейдите в корневой каталог проекта ConfUprav1 и выполните следующую команду:
```sh
python hw3/config_parser.py hw3/example_config.txt hw3/output.toml
```

## Запуск тестов
Перейдите в корневой каталог проекта ConfUprav1 и выполните следующую команду:

```sh
python -m unittest hw3/test_config_parser.py
```

## Пример конфигурационного файла
Файл example_config.txt содержит пример конфигурации:
```sh
' Это конфигурация для сетевых настроек
var port 8080;
var timeout 30;
var max_connections 100;
var server_name "example.com";

' Это однострочный комментарий

#( "192.168.1.1", "192.168.1.2", "192.168.1.3" )

table([
    ip = "192.168.1.1",
    mask = "255.255.255.0",
    gateway = "192.168.1.254"
])

var new_port @{+ port 1};
var new_timeout @{- timeout 5};
var new_max_connections @{* max_connections 2};
var min_value @{min port timeout};
var max_value @{max port max_connections};
```
