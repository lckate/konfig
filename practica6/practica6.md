# 1 Задание
Написать Программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше. Для мало знакомых с Питоном используется упрощенный вариант civgraph: [civgraph.json](civgraph.json).
Реализация (упрощенный вариант):
```
import json
def parse_civgraph_to_makefile(input_file, output_file):

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            civgraph = json.load(f)

        # Собираем все зависимости
        all_technologies = set(civgraph.keys())
        all_dependencies = {dep for deps in civgraph.values() for dep in deps}
        standalone_technologies = all_dependencies - all_technologies

        with open(output_file, 'w', encoding='utf-8') as makefile:
            # Записываем правила в civgraph
            for tech, dependencies in civgraph.items():
                dependencies_str = ' '.join(dependencies)
                makefile.write(f"{tech}: {dependencies_str}\n")
                makefile.write(f"\t@echo {tech}\n\n")

            # Добавляем пустые правила для зависимостей без определений
            for tech in standalone_technologies:
                makefile.write(f"{tech}:\n")
                makefile.write(f"\t@echo {tech}\n\n")

        print(f"Makefile успешно создан: {output_file}")

    except FileNotFoundError:
        print(f"Файл {input_file} не найден.")
    except json.JSONDecodeError:
        print(f"Ошибка при чтении JSON из файла {input_file}.")

input_file = "civgraph.json"
output_file = "Makefile"
parse_civgraph_to_makefile(input_file, output_file)
```
Результат работы программы:
![image](https://github.com/lckate/konfig_menegment/blob/main/practica6/task1.png)
# 2 Задание
Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".
Реализация: 
```

```
Результат работы программы:
![image]()
