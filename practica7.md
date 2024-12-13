# 1 задание
Код на  LaTeX:
`\documentclass{article}
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

\end{document}`
Картинка:
![image]()
