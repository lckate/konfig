import git
from datetime import datetime
import json
import subprocess
import os


# Чтение конфигурационного файла
def read_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)


# Получение коммитов до указанной даты
def get_commits_before_date(repo_path, date_str):
    repo = git.Repo(repo_path)
    cutoff_date = datetime.strptime(date_str, "%Y-%m-%d")

    commits = []
    for commit in repo.iter_commits('main', since=cutoff_date):
        commits.append(commit.hexsha)

    return commits


def get_commits_before_date(repo_path, date_str):
    repo = git.Repo(repo_path)
    cutoff_date = datetime.strptime(date_str, "%Y-%m-%d")

    commits = []
    for commit in repo.iter_commits('main'):
        # Приведение commit.committed_datetime к offset-naive
        # Метод replace(tzinfo=None) удаляет информацию о временной зоне из объекта datetime,
        # делая его offset-naive
        commit_date = commit.committed_datetime.replace(tzinfo=None)
        if commit_date < cutoff_date:
            commits.append(commit.hexsha)
    return commits


def build_dependency_graph(repo_path, commits):
    graph = {}

    # Инициализируем граф с пустыми зависимостями
    for commit in commits:
        graph[commit] = []

    # Строим зависимости, предполагая, что порядок коммитов имеет значение
    for i in range(len(commits) - 1):
        graph[commits[i]].append(commits[i + 1])

    return graph


# Генерация кода для визуализации графа в формате PlantUML
def generate_plantuml_code(graph):
    plantuml_code = "@startuml\n"

    for commit, parents in graph.items():
        for parent in parents:
            plantuml_code += f'"{parent}" --> "{commit}"\n'

    plantuml_code += "@enduml"
    return plantuml_code


# Сохранение результата в файл
def save_result(plantuml_code, result_file_path):
    with open(result_file_path, 'w') as f:
        f.write(plantuml_code)


# Вывод результата на экран
def print_result(plantuml_code):
    print(plantuml_code)


def generate_plantuml_image(input_file, output_file):
    plantuml_path = "D://_Downloads//plantuml-jar-gplv2-1.2023.7//plantuml.jar"
    if not os.path.exists(plantuml_path):
        raise FileNotFoundError(f"PlantUML jar not found at {plantuml_path}")

    # Запуск команды для генерации изображения
    subprocess.run(['java', '-jar', plantuml_path, input_file])

    print(f"Image saved as {output_file}")


# Основная функция
def main(config_path):
    config = read_config(config_path)

    # Удаляем устаревшие результаты
    if os.path.exists(config['result_file_path']):
        os.remove(config['result_file_path'])
    if os.path.exists(config['image_output_path']):
        os.remove(config['image_output_path'])

    repo_path = config['repository_path']
    date_str = config['date']
    result_file_path = config['result_file_path']
    image_output_path = config['image_output_path']

    # Получаем список коммитов до указанной даты
    commits = get_commits_before_date(repo_path, date_str)

    # Строим граф зависимостей
    graph = build_dependency_graph(repo_path, commits)

    # Генерируем код для визуализации в PlantUML
    plantuml_code = generate_plantuml_code(graph)

    # Сохраняем результат в файл и выводим на экран
    save_result(plantuml_code, result_file_path)
    generate_plantuml_image(result_file_path, image_output_path)
    print_result(plantuml_code)


if __name__ == "__main__":
    main("config.json")