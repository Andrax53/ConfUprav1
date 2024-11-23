# Задание 2
 # Визуализатор графа зависимостей пакетов .NET

Этот проект представляет собой инструмент командной строки для визуализации графа зависимостей пакетов .NET. Инструмент использует NuGet API для получения информации о пакетах и их зависимостях, а затем генерирует граф в формате Mermaid.

## Установка

1. Убедитесь, что у вас установлен Python 3.x.
2. Установите необходимые зависимости:

```sh
pip install requests
```
## Использование
Команда запуска
Для запуска инструмента используйте следующую команду:

```sh
python3 test.py <путь_к_graphviz> <имя_пакета> <выходной_файл> <максимальная_глубина> <URL_репозитория>
```
## Пример команды
```sh
python3 test.py /usr/bin/dot Newtonsoft.Json output.mmd 2 https://api.nuget.org/v3-flatcontainer
```
Аргументы командной строки

<путь_к_graphviz>: Путь к программе для визуализации графов (например, /usr/bin/dot).

<имя_пакета>: Имя анализируемого пакета (например, Newtonsoft.Json).

<выходной_файл>: Путь к файлу-результату в виде кода (например, output.mmd).

<максимальная_глубина>: Максимальная глубина анализа зависимостей (например, 2).

<URL_репозитория>: URL-адрес репозитория (например, https://api.nuget.org/v3-flatcontainer).

## Пример использования
Создайте файл config.csv с параметрами конфигурации:
```sh
graphviz_path,package_name,output_file,max_depth,repository_url
/usr/bin/dot,Newtonsoft.Json,output.mmd,2,https://api.nuget.org/v3-flatcontainer
```
Запустите скрипт с использованием параметров из файла config.csv:
```sh
python3 run_visualizer.py
```
## ИЛИ

```sh
python3 test.py /usr/bin/dot Newtonsoft.Json output.mmd 2 https://api.nuget.org/v3-flatcontainer
```

## Тестирование
Для запуска тестов используйте следующую команду:

```
python -m unittest test_visualizer.py
```
