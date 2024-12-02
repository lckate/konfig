import argparse
import toml
import math
import re


# Исключения для ошибок синтаксики
class SyntaxError(Exception):
    pass


# Проверка корректности имени
def validate_name(name):
    if not re.match(r"^[_a-zA-Z][_a-zA-Z0-9]*$", name):
        raise SyntaxError(f"Некорректное имя: {name}")


# Постфиксное вычисление
def evaluate_postfix(expression, constants):
    stack = []
    for token in expression:
        if token.lstrip('-').isdigit():  # Проверка на отрицательные числа
            stack.append(float(token))  # Используем float для поддержки дробных чисел
        elif token in constants:  # Константы
            stack.append(constants[token])
        elif token == "+":
            stack.append(stack.pop() + stack.pop())
        elif token == "-":
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
        elif token == "*":
            stack.append(stack.pop() * stack.pop())
        elif token == "sqrt":
            stack.append(math.sqrt(stack.pop()))
        elif token == "abs":
            stack.append(abs(stack.pop()))
        else:
            raise SyntaxError(f"Некорректный токен: {token}")
    return stack[-1]


# Преобразование TOML в учебный язык
def convert_toml_to_custom(data):
    constants = {}
    result = []

    def process_dict(d):
        items = []
        for k, v in d.items():
            validate_name(k)
            if isinstance(v, dict):
                v_str = process_dict(v)
                items.append(f"{k} => {v_str}")
            elif isinstance(v, str):
                items.append(f"{k} => '{v}'")
            elif isinstance(v, (int, float)):
                items.append(f"{k} => {v}")
            else:
                raise SyntaxError(f"Некорректное значение для ключа {k}: {v}")
        return "[\n  " + ",\n  ".join(items) + "\n]"

    for key, value in data.items():
        validate_name(key)
        if isinstance(value, dict):
            result.append(f"{key} := {process_dict(value)}")
        elif isinstance(value, (int, float, str)):
            constants[key] = value
            result.append(f"{key} := {value}")
        elif isinstance(value, list):  # Постфиксное вычисление
            # Проверка, является ли список постфиксным выражением
            if all(isinstance(item, str) for item in value):
                evaluated = evaluate_postfix(value, constants)
                result.append(f"{key} := ^({' '.join(value)}) # {evaluated}")
            else:
                raise SyntaxError(f"Некорректное значение для ключа {key}: {value}")
        else:
            raise SyntaxError(f"Некорректное значение: {value}")

    return "\n".join(result)




# Основная функция
def main():
    parser = argparse.ArgumentParser(description="Конвертер TOML в учебный конфигурационный язык.")
    parser.add_argument("-i", "--input", required=True, help="Входной файл TOML")
    parser.add_argument("-o", "--output", required=True, help="Выходной файл")
    args = parser.parse_args()

    try:
        # Чтение TOML
        with open(args.input, "r") as infile:
            toml_data = toml.load(infile)

        # Преобразование
        output = convert_toml_to_custom(toml_data)

        # Запись результата
        with open(args.output, "w") as outfile:
            outfile.write(output)
        print(f"Конвертация завершена. Результат записан в {args.output}")

    except SyntaxError as e:
        print(f"Ошибка синтаксиса: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
