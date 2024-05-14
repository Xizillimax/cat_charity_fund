# Проект приложение QRKot

## Описание
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Технологии

- Python
- FastAPI

### Развертывание и запуск парсера

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Xizillimax/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Выполнить миграции:

```
alembic upgrade head
```

Запустить в терминале командой:
```
uvicorn app.main:app --reload
```

Автор - [Maxim Zelenin](https://github.com/Xizillimax)