# Matrix Spiral

Библиотека для тестового задания: асинхронно скачивает квадратную матрицу по протоколу HTTP(S) и возвращает её элементы в виде списка, обходя матрицу по спирали против часовой стрелки, начиная с левого верхнего угла.

## Задание

Тестовое задание Avito: python-trainee-assignment

## Что сделано

- `async def get_matrix(url: str) -> List[int]` — интерфейс по ТЗ.
- Загрузка реализована асинхронно через **aiohttp**: сессия с таймаутом 30 секунд, ответ читается без блокировки цикла событий.
- Спиральный обход против часовой стрелки от левого верхнего угла.
- Работает на квадратных матрицах любой размерности (проверено на 1×1–4×4).
- Проверка квадратности матрицы: несовпадение длин строк → `MatrixError`.
- Нечисловые ячейки перехватываются: `ValueError` сводится к `MatrixError` с текстом строки.
- Обработка ошибок сети и сервера — всё сводится к `MatrixError`; код ответа 400 и выше тоже превращается в `MatrixError`.
- 8 юнит-тестов: кейс из задания, размерности, Connection Refused, пустой URL.
- Подсказки по типам и докстринги для всех функций.

## Уточнения

- Тест `test_from_source` загружает матрицу по URL из задания и требует доступа в интернет. Остальные тесты работают офлайн.

## Что не сделано

- Повторные попытки при сбоях в сети — при единичной загрузке матрицы избыточны.
- Тесты на ошибки сервера (HTTP-коды) и таймаут — обработка в коде есть (`response.status`, `ClientTimeout`), тестов нет.

## Как запустить

### Установка

Нужен Python 3.10 или новее.

1. Клонируйте репозиторий и перейдите в папку проекта:

   ```powershell
   git clone <ссылка-на-репозиторий>
   cd <папка-проекта>
   ```

2. Создайте и активируйте виртуальное окружение:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate          # Windows, PowerShell
   source .venv/bin/activate        # Linux/macOS
   ```

3. Установите зависимости:

   ```powershell
   uv pip install aiohttp           # если окружение создано через uv
   ```

   или, для обычного окружения:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Проверка установки:

   ```powershell
   python -c "import aiohttp; print('ok', aiohttp.__version__)"
   ```

### Запуск тестов

Все команды выполняются из папки проекта:

```powershell
python -m unittest test_matrix -v
```

Ожидаемый результат:

```
Ran 8 tests in ...s

OK
```

### Использование

```python
import asyncio
from matrix import get_matrix

SOURCE_URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"

result = asyncio.run(get_matrix(SOURCE_URL))
print(result)
```
