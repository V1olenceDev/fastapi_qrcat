# QRKot Google Sheets
 
![workflows](https://github.com/ThatCoderMan/QRkot_spreadsheets/actions/workflows/workflow.yml/badge.svg)

<details>
<summary>Project stack</summary>

- Python 3.9
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Aiogoogle
- GitHub Actions

</details>


Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Запуск проекта
### Установка
Клонируйте репозиторий:
~~~commandline
git clone git@github.com:V1olenceDev/QRkot_spreadsheets.git
~~~
Перейдите в папку QRkot_spreadsheets/:
~~~commandline
cd QRkot_spreadsheets
~~~
Активируйте виртуальное окружение:
~~~commandline
pip install -r requirements.txt
~~~
~~~
Миграции базы данных:
~~~commandline
alembic revision --autogenerate 
alembic upgrade head
~~~
### Запуск программы
~~~commandline
uvicorn app.main:app
~~~
---

Документация доступна после запуска программы по адресу `/docs`

---
## Автор
[Гаспарян Валерий Гургенович](https://github.com/V1olenceDev)
