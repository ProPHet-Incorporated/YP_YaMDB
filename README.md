# Проект YaMDb.
## Яндекс.Практикум
## Python-backend

 **О проекте:**
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

**Технологии**
Python
Django
Django Rest Framework
Simple JWT
SQLite3

***

### Как запустить проект:

С помощью командной строки клонировать репозиторий и перейти в корневой каталог:

```bash
git clone https://github.com/philippbovin/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```bash
# Windows
py -3.9 -m venv venv
source venv/Scripts/activate

# Linux и macOS
python3 -m venv venv
source venv/bin/activate
```

Обновить pip и установить зависимости из requirements.txt:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python manage.py migrate
```

Наполнить БД из csv-файла:

```bash
python manage.py upload_csv_to_database static/data/category.csv
```

Запустить проект:

```bash
python manage.py runserver
```

### Пара примеров обращений к endpoint'ам проекта:

#### TITLES
#### Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

#### Получение списка всех произведений
Права доступа: Доступно без токена

#### GET
```url
/api/v1/titles/
```

#### Cтруктура JSON в отклике:
```JSON
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 0,
                "text": "string",
                "author": "string",
                "score": 1,
                "pub_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
]
```

#### REVIEWS
#### Отзывы

#### Получение списка всех отзывов
Права доступа: Доступно без токена

#### GET
```url
/api/v1/titles/{title_id}/reviews/
```

#### Cтруктура JSON в отклике:
```JSON
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
            "id": 0,
            "text": "string",
            "author": "string",
            "score": 1,
            "pub_date": "2019-08-24T14:15:22Z"
            }
        ]
    }
]
```

Все остальные эндпоинты можно посмотреть в REDOC:
http://127.0.0.1:8000/redoc/

***Авторы:***
* Филипп Бовин | Github: https://github.com/philippbovin | Тимлид. 
Работал над управлением пользователями:
Системы регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail.
* Никита Тарасов | Github: https://github.com/ProPHet-Incorporated | Разработчик #2.
Работал над моделями, view и эндпойнтами для произведений, категорий, жанров; Реализовал импорт данных из csv файлов.
* Андрей Башилов | Github: https://github.com/chemicalsp | Разработчик #3.
Работал над отзывами, комментариями, рейтингом произведений.
