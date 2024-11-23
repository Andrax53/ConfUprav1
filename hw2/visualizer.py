import os
import sys
import requests
from collections import defaultdict
import argparse
import tempfile
import zipfile
import xml.etree.ElementTree as ET

def download_nupkg(base_url, package_name):
    """
    Загружает последнюю версию пакета .NET и возвращает путь к загруженному файлу.
    """
    index_url = f"{base_url}/{package_name.lower()}/index.json"
    try:
        # Получаем список версий пакета
        response = requests.get(index_url)
        response.raise_for_status()
        data = response.json()
        versions = data['versions']
        latest_version = versions[-1]
        nupkg_url = f"{base_url}/{package_name.lower()}/{latest_version}/{package_name.lower()}.{latest_version}.nupkg"

        # Скачиваем файл .nupkg
        response = requests.get(nupkg_url)
        response.raise_for_status()
        temp_dir = tempfile.gettempdir()
        nupkg_path = os.path.join(temp_dir, f"{package_name}.{latest_version}.nupkg")
        with open(nupkg_path, 'wb') as f:
            f.write(response.content)
        return nupkg_path
    except Exception as e:
        print(f"Ошибка при загрузке пакета {package_name}: {e}")
        sys.exit(1)

def parse_nupkg_dependencies(nupkg_path):
    """
    Парсит зависимости пакета .NET из nupkg файла.
    """
    dependencies = []
    try:
        with zipfile.ZipFile(nupkg_path, 'r') as zip_ref:
            # Ищем файл .nuspec в архиве
            nuspec_filename = None
            for filename in zip_ref.namelist():
                if filename.endswith('.nuspec'):
                    nuspec_filename = filename
                    break
            if not nuspec_filename:
                print(f"Файл .nuspec не найден в пакете {nupkg_path}")
                return dependencies

            # Извлекаем и парсим файл .nuspec
            with zip_ref.open(nuspec_filename) as nuspec_file:
                tree = ET.parse(nuspec_file)
                root = tree.getroot()
                ns = {'ns': root.tag.split('}')[0].strip('{')}

                for dep_group in root.findall('.//ns:dependencies/ns:group', ns):
                    for dep in dep_group.findall('ns:dependency', ns):
                        dep_id = dep.attrib.get('id')
                        if dep_id:
                            dependencies.append(dep_id)
                # Для пакетов без групп
                for dep in root.findall('.//ns:dependencies/ns:dependency', ns):
                    dep_id = dep.attrib.get('id')
                    if dep_id:
                        dependencies.append(dep_id)
        return dependencies
    except Exception as e:
        print(f"Ошибка при парсинге зависимостей из {nupkg_path}: {e}")
        return dependencies

def build_dependency_graph(base_url, package_name, max_depth):
    """
    Построение графа зависимостей до указанной глубины.
    """
    graph = defaultdict(list)
    visited = set()

    def fetch_deps(pkg, depth):
        if depth > max_depth or pkg.lower() in visited:
            return
        visited.add(pkg.lower())
        print(f"Загрузка пакета {pkg} (глубина {depth})...")
        nupkg_path = download_nupkg(base_url, pkg)
        deps = parse_nupkg_dependencies(nupkg_path)
        graph[pkg].extend(deps)
        for dep in deps:
            fetch_deps(dep, depth + 1)

    fetch_deps(package_name, 0)
    return graph

def generate_mermaid_graph(graph):
    """
    Генерирует граф в формате Mermaid.
    """
    mermaid = ["graph TD"]
    for pkg, deps in graph.items():
        if deps:
            for dep in deps:
                mermaid.append(f"    {pkg} --> {dep}")
        else:
            mermaid.append(f"    {pkg}")
    return "\n".join(mermaid)



def main():
    parser = argparse.ArgumentParser(description="Визуализатор графа зависимостей пакетов .NET")
    parser.add_argument("visualizer_path", help="Путь к программе для визуализации графов")
    parser.add_argument("package_name", help="Имя анализируемого пакета")
    parser.add_argument("output_file", help="Путь к файлу-результату в виде кода")
    parser.add_argument("max_depth", type=int, help="Максимальная глубина анализа зависимостей")
    parser.add_argument("base_url", help="URL-адрес репозитория")

    args = parser.parse_args()

    # Построение графа зависимостей
    print("Построение графа зависимостей...")
    graph = build_dependency_graph(args.base_url, args.package_name, args.max_depth)

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