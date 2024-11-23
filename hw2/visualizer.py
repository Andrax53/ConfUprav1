import os
import sys
import requests
from collections import defaultdict
import argparse

def download_nupkg_dependencies(base_url, package_name):
    """
    Загружает зависимости пакета .NET.
    """
    url = f"{base_url}/{package_name}.nupkg"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        sys.exit(1)

def parse_nupkg_dependencies(dependencies_data):
    """
    Парсит зависимости пакета .NET.
    """
    dependencies = defaultdict(list)
    for package in dependencies_data:
        package_name = package['name']
        for dependency in package.get('dependencies', []):
            dependencies[package_name].append(dependency['id'])
    return dependencies

def build_dependency_graph(package_name, dependencies, max_depth):
    """
    Построение графа зависимостей до указанной глубины.
    """
    graph = defaultdict(list)
    visited = set()

    def fetch_deps(pkg, depth):
        if depth > max_depth or pkg in visited:
            return
        visited.add(pkg)
        for dep in dependencies.get(pkg, []):
            graph[pkg].append(dep)
            fetch_deps(dep, depth + 1)

    fetch_deps(package_name, 0)
    return graph

def generate_mermaid_graph(graph):
    """
    Генерирует граф в формате Mermaid.
    """
    mermaid = ["graph TD"]
    for pkg, deps in graph.items():
        for dep in deps:
            mermaid.append(f"    {pkg} --> {dep}")
    return "\n".join(mermaid)

def main():
    parser = argparse.ArgumentParser(description="Визуализатор графа зависимостей пакетов .NET")
    parser.add_argument("visualizer_path", help="Путь к программе для визуализации графов")
    parser.add_argument("package_name", help="Имя анализируемого пакета")
    parser.add_argument("output_file", help="Путь к файлу-результату в виде кода")
    parser.add_argument("max_depth", type=int, help="Максимальная глубина анализа зависимостей")
    parser.add_argument("base_url", help="URL-адрес репозитория")

    args = parser.parse_args()

    # Загрузка и парсинг зависимостей пакета .NET
    print("Загрузка зависимостей пакета .NET...")
    dependencies_data = download_nupkg_dependencies(args.base_url, args.package_name)
    print("Парсинг зависимостей пакета .NET...")
    dependencies = parse_nupkg_dependencies(dependencies_data)

    # Построение графа зависимостей
    print("Построение графа зависимостей...")
    graph = build_dependency_graph(args.package_name, dependencies, args.max_depth)

    # Генерация Mermaid-графа
    print("Генерация Mermaid-графа...")
    mermaid_graph = generate_mermaid_graph(graph)

    # Запись в файл
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as file:
            file.write(mermaid_graph)
        print(f"Граф зависимостей записан в файл {args.output_file}.")
    else:
        print("Граф зависимостей:")
        print(mermaid_graph)

if __name__ == "__main__":
    main()
