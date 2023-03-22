import csv
import logging
import os

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import (
    Categories, Comments, Genre, Review, Title, TitleGenre
)
from users.models import User

logging.basicConfig(level=logging.DEBUG, filename='main.log', filemode='w')
logger = logging.getLogger('django')


class Command(BaseCommand):
    help = 'Загружает информацию из файлов .csv в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('command', nargs=1, type=str)

    def handle(self, *args, **options):
        self.imported_counter = 0
        self.scipped_counter = 0

        command = options['command'][0]
        if command == 'help':
            print(
                'Данный скрипт загружает информацию из файлов .csv '
                'в базу данных.\n'
                'Доступны следующие команды: \n'
                '   auto - автоматическое добавление всех файлов по порядку\n'
                '   exit - завершение работы\n'
                'Если хотите загрузить отдельный файл, вместо команды '
                'напишите его абсолютный или относительный путь (например '
                'static/data/category.csv'
            )
            command = input('Введите команду: ')
        if command == 'exit':
            return
        if command == 'auto':
            files = [
                'users.csv',
                'genre.csv',
                'category.csv',
                'titles.csv',
                'genre_title.csv',
                'review.csv',
                'comments.csv'
            ]
            for file in files:
                self.csv_path = 'static/data/' + file
                logger.info(f'Попытка загрузки информации из файла {file}')
                self.main()
                logger.info('Успешно.')
            self.finalize()
            return

        self.csv_path = command
        self.main()
        self.finalize()

    def get_data(self, fields, data):
        result = {}
        for field in fields:
            if data.get(field):
                result[field] = data.get(field)
        return result

    def error_message(self, file_name, error):
        return f'В файле {file_name} не найдено значение {error}'

    def upload_genre(self, reader, file_name):
        fields = ('id', 'name', 'slug')
        for index, data in enumerate(reader):
            clean_data = self.get_data(fields, data)
            Genre.objects.create(
                id=clean_data['id'],
                name=clean_data['name'],
                slug=clean_data['slug']
            )
            self.imported_counter += 1

    def upload_comments(self, reader, file_name):
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')
        for index, data in enumerate(reader):
            clean_data = self.get_data(fields, data)
            review = get_object_or_404(Review, pk=clean_data['review_id'])
            author = get_object_or_404(User, pk=clean_data['author'])
            Comments.objects.create(
                id=clean_data['id'],
                review=review,
                text=clean_data['text'],
                author=author,
                pub_date=clean_data['pub_date'],
            )
            self.imported_counter += 1

    def upload_category(self, reader, file_name):
        fields = ('id', 'name', 'slug')
        for index, data in enumerate(reader):
            clean_data = self.get_data(fields, data)
            Categories.objects.create(
                id=clean_data['id'],
                name=clean_data['name'],
                slug=clean_data['slug']
            )
            self.imported_counter += 1

    def upload_genre_title(self, reader, file_name):
        fields = ('id', 'title_id', 'genre_id')
        for index, data in enumerate(reader):
            clean_data = self.get_data(fields, data)
            title = get_object_or_404(Title, pk=clean_data['title_id'])
            genre = get_object_or_404(Genre, pk=clean_data['genre_id'])
            TitleGenre.objects.create(
                id=clean_data['id'],
                title=title,
                genre=genre
            )
            self.imported_counter += 1

    def upload_review(self, reader, file_name):
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')
        for index, data in enumerate(reader):
            clean_data = self.get_data(fields, data)
            title = get_object_or_404(Title, pk=clean_data['title_id'])
            author = get_object_or_404(User, pk=clean_data['author'])
            Review.objects.create(
                id=clean_data['id'],
                text=clean_data['text'],
                author=author,
                score=clean_data['score'],
                pub_date=clean_data['pub_date'],
                title=title
            )
            self.imported_counter += 1

    def upload_titles(self, reader, file_name):
        fields = ('id', 'name', 'year', 'category')
        for index, data in enumerate(reader):
            clean_data = self.get_data(fields, data)
            category = get_object_or_404(Categories, pk=clean_data['category'])
            Title.objects.create(
                id=clean_data['id'],
                name=clean_data['name'],
                year=clean_data['year'],
                category=category
            )
            self.imported_counter += 1

    def upload_users(self, reader, file_name):
        fields = ('id', 'username', 'email', 'role')
        for index, data in enumerate(reader):
            clean_data = self.get_data(fields, data)
            User.objects.create(
                id=clean_data['id'],
                username=clean_data['username'],
                email=clean_data['email'],
                role=clean_data['role'],
            )
            self.imported_counter += 1

    FILES_AND_FUNCTIONS = {
        'category.csv': upload_category,
        'comments.csv': upload_comments,
        'genre.csv': upload_genre,
        'genre_title.csv': upload_genre_title,
        'review.csv': upload_review,
        'titles.csv': upload_titles,
        'users.csv': upload_users,
    }

    def main(self):
        with open(self.csv_path, mode='r', encoding='utf-8') as file:
            file_name = os.path.basename(file.name)
            reader = csv.DictReader(file)
            file_function = self.FILES_AND_FUNCTIONS[file_name]
            try:
                file_function(self, reader, file_name)
            except KeyError as error:
                logger.error(self.error_message(file_name, error))
                raise error

    def finalize(self):
        if self.scipped_counter == 0:
            logger.info(
                'Импорт завершён без ошибок. Загружено строк: '
                f'{self.imported_counter}'
            )
        else:
            logger.info(f'Импортировано: {self.imported_counter}')
            logger.info(f'Пропущено: {self.scipped_counter}')
