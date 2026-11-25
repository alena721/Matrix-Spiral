"""Библиотека: получает квадратную матрицу с сервера и обходит её по спирали"""
import asyncio
import urllib.request
import urllib.error
from typing import List


class MatrixError(Exception):
    """Ошибка загрузки или разбора матрицы."""


def parse_matrix(text: str) -> List[List[int]]:
    """Разбирает текстовую таблицу: берёт только строки с числами"""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):         
            continue
        try:
            rows.append([int(cell) for cell in line.strip("|").split("|")])
        except ValueError:
                raise MatrixError(f"в таблице не число: {line}")
    if not rows:
        raise MatrixError("в ответе нет строк матрицы")
    if any(len(row) != len(rows) for row in rows):
        raise MatrixError("матрица не квадратная")
    return rows


def spiral_traversal(matrix: List[List[int]]) -> List[int]:
    """Обход по спирали против часовой стрелки, с левого верхнего угла.

    Снимаем левый столбец, а остаток поворачиваем по часовой стрелке -
    тогда следующий нужный столбец снова оказывается слева.
    """
    result = []
    while matrix and matrix[0]:
        result += [row[0] for row in matrix]             # вниз по левому столбцу
        matrix = [row[1:] for row in matrix]

        if matrix and matrix[0]:
            result += matrix[-1]                         # вправо по нижней строке
            matrix = matrix[:-1]

            result += [row[-1] for row in matrix][::-1]  # вверх по правому столбцу
            matrix = [row[:-1] for row in matrix]

            if matrix and matrix[0]:
                result += matrix[0][::-1]                # влево по верхней строке
                matrix = matrix[1:]
    return result


def _download(url: str) -> str:
    """Скачивает текст по URL через стандартную библиотеку"""
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            if response.status >= 400:
                raise MatrixError(f"сервер вернул код {response.status}: {url}")
            return response.read().decode("utf-8")
    except MatrixError:
        raise
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        raise MatrixError(f"ошибка сети или сервера: {exc}")


async def get_matrix(url: str) -> List[int]:
    """Скачивает матрицу по URL и возвращает её обход по спирали"""
    if not url:
        raise MatrixError("не указан URL")
    loop = asyncio.get_running_loop()
    text = await loop.run_in_executor(None, _download, url)
    return spiral_traversal(parse_matrix(text))
