# 1 Задание
Код на  LaTeX:
```
\documentclass{article}
\usepackage[T2A]{fontenc} % Поддержка кириллицы
\usepackage[utf8]{inputenc} % Кодировка UTF-8
\usepackage[russian]{babel} % Подключение русского языка
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}

\begin{document}

\begin{center}
    \textbf{Дудик Екатерина Сергеевна}
\end{center}

\[
\int_{x}^{\infty} \frac{dt}{t(t^{2}-1)\log t} = \int_{x}^{\infty} \frac{1}{t\log t} \left( \sum_{m} t^{-2m} \right) dt = \sum_{m} \int_{x}^{\infty} \frac{t^{-2m}}{t\log t} dt \quad = -\sum_{m} \mathrm{li}(x^{-2m})
\]

\end{document}
```
Картинка:
![image](https://github.com/lckate/konfig_menegment/blob/main/practica7/task1.jpg)

# 2 Задание
Код на PlantUML
```
@startuml

' Убираем стандартный желтый цвет
skinparam backgroundColor white
skinparam sequenceArrowColor black
skinparam actorBorderColor black
skinparam participantBorderColor black
skinparam noteBackgroundColor white
skinparam noteBorderColor black

' Псевдонимы
actor "Студент Дудик Е.С." as Student
actor "Преподаватель" as Teacher
participant "Piazza" as Piazza

' Диаграмма
Student -> Piazza: Публикация задачи
Piazza -> Teacher: Задача опубликована
Teacher -> Piazza: Поиск задач
Piazza -> Teacher: Получение задачи
Teacher -> Piazza: Публикация решения
Piazza -> Student: Решение опубликовано
Student -> Piazza: Поиск решений
Piazza -> Student: Решение найдено
Student -> Piazza: Публикация оценки
Piazza -> Teacher: Оценка опубликована
Teacher -> Piazza: Проверка оценки
Piazza -> Teacher: Оценка получена

@enduml
```
Картинка:
![image](https://github.com/lckate/konfig_menegment/blob/main/practica7/task2.jpg)

# 4 Задание
Документация проекта на Java (практика №14):
[pdf-файл с документацией](https://github.com/lckate/konfig_menegment/blob/main/practica7/refman4.pdf)
# 5 Задание
Документация проекта на Python (дз №3):
[pdf-файл с документацией](https://github.com/lckate/konfig_menegment/blob/main/practica7/refman1.pdf)


