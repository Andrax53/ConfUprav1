# Задание 3
# Учебный конфигурационный язык

Этот проект реализует инструмент командной строки для преобразования текста из учебного конфигурационного языка в формат TOML. Инструмент обрабатывает комментарии, константы, структуры (включая вложенные структуры) и поддерживает ссылки на константы.

## Возможности
- Объявление и использование констант
- Поддержка вложенных структур произвольной глубины
- Комментарии в формате `(comment текст комментария)`
- Преобразование в формат TOML
- Проверка синтаксиса и типов данных

## Структура проекта
```
hw3/
├── config_parser.py       # Основной парсер
├── test_config_parser.py  # Модульные тесты
├── examples/             # Примеры конфигураций
│   ├── network_config.txt
│   ├── game_config.txt
│   └── nested_config.txt
└── output.toml           # Выходной TOML файл
```

## Установка

1. Убедитесь, что у вас установлен Python 3.x
2. Создайте виртуальное окружение и активируйте его:

```sh
python -m venv .venv
.venv\Scripts\activate  # Для Windows
# или
source .venv/bin/activate  # Для macOS/Linux
```

3. Установите необходимые зависимости:
```sh
pip install toml
```

## Использование

### Парсинг конфигурационного файла
```sh
python hw3/config_parser.py <input_file> <output_file>
```

Например:
```sh
python hw3/config_parser.py hw3/examples/nested_config.txt hw3/output.toml
```

### Запуск тестов
```sh
python -m unittest hw3/test_config_parser.py
```

## Примеры конфигураций

### Базовая конфигурация с константами
```
port <- 8080;
timeout <- 30;
max_connections <- 100;

backup_port <- |port|;  # Использование значения другой константы
```

### Простая структура
```
struct {
    ip = 192.168.1.1,
    mask = 255.255.255.0,
    gateway = 192.168.1.254,
}
```

### Вложенные структуры
```
struct {
    server = struct {
        host = localhost,
        port = 8080,
        ssl = struct {
            enabled = true,
            cert_path = /etc/ssl/cert.pem,
            key_path = /etc/ssl/key.pem,
        },
    },
    database = struct {
        host = localhost,
        port = 5432,
        credentials = struct {
            username = admin,
            password = secure123,
        },
    },
}
```

## Синтаксис

### Константы
- Объявление: `name <- value;`
- Ссылка на константу: `name <- |other_constant|;`

### Структуры
- Начало структуры: `struct {`
- Поля структуры: `key = value,`
- Вложенная структура: 
  ```
  field = struct {
      nested_field = value,
  },
  ```
- Конец структуры: `}`

### Комментарии
- Однострочные: `(comment текст комментария)`
