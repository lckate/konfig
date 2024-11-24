import os
import argparse
from graphviz import Digraph
import unittest


def parse_dependencies(package_name, max_depth):
    """
    Функция для генерации зависимостей пакета.
    Имитация данных для тестирования.
    """
    dependencies = {
        "PackageA": ["PackageB", "PackageC"],
        "PackageB": ["PackageD"],
        "PackageC": [],
        "PackageD": ["PackageE"],
        "PackageE": []
    }
    graph = {}

    def fetch_deps(pkg, depth):
        if depth > max_depth or pkg not in dependencies:
            return
        graph[pkg] = dependencies.get(pkg, [])
        for dep in graph[pkg]:
            fetch_deps(dep, depth + 1)

    fetch_deps(package_name, 0)
    return graph


def generate_mermaid_graph(graph):
    """
    Генерация графа в формате Mermaid.
    """
    lines = ["graph TD"]
    for pkg, deps in graph.items():
        for dep in deps:
            lines.append(f"  {pkg} --> {dep}")
    return "\n".join(lines)


def save_graph_as_png(graph, output_path, graphviz_path):
    """
    Сохранение графа в формате PNG с помощью Graphviz.
    """
    dot = Digraph(format="png", engine="dot")
    for pkg, deps in graph.items():
        for dep in deps:
            dot.edge(pkg, dep)
    dot.render(output_path, cleanup=True, directory=os.path.dirname(output_path))


def main():
    parser = argparse.ArgumentParser(description="Инструмент для визуализации графа зависимостей .NET пакетов.")
    parser.add_argument("--graphviz-path", required=True, help="Путь к программе для визуализации графов (Graphviz).")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета.")
    parser.add_argument("--output-path", required=True, help="Путь к файлу с изображением графа зависимостей.")
    parser.add_argument("--max-depth", type=int, required=True, help="Максимальная глубина анализа зависимостей.")
    args = parser.parse_args()

    # Установка пути к Graphviz
    os.environ["PATH"] += os.pathsep + args.graphviz_path

    # Генерация графа зависимостей
    graph = parse_dependencies(args.package, args.max_depth)

    if not graph:
        print(f"Нет данных о зависимостях для пакета {args.package}.")
        return

    # Сохранение графа в формате PNG
    save_graph_as_png(graph, args.output_path, args.graphviz_path)

    print("Граф зависимостей успешно сохранен!")


# Тесты
class TestDependencyVisualizer(unittest.TestCase):
    def test_parse_dependencies(self):
        graph = parse_dependencies("PackageA", 2)
        expected = {
            "PackageA": ["PackageB", "PackageC"],
            "PackageB": ["PackageD"],
            "PackageC": [],
            "PackageD": ["PackageE"]
        }
        self.assertEqual(graph, expected)

    def test_generate_mermaid_graph(self):
        graph = {
            "PackageA": ["PackageB", "PackageC"],
            "PackageB": ["PackageD"],
            "PackageC": [],
        }
        mermaid = generate_mermaid_graph(graph)
        expected = """graph TD
  PackageA --> PackageB
  PackageA --> PackageC
  PackageB --> PackageD"""
        self.assertEqual(mermaid.strip(), expected.strip())


if __name__ == "__main__":
    main()
