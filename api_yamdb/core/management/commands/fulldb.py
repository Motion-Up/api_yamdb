import csv
import datetime
import sqlite3
import pathlib
from pathlib import Path

from django.core.management.base import BaseCommand

dir_path = pathlib.Path.cwd()
path_db = Path(dir_path, 'db.sqlite3')

all_csv_files = {
    'users.csv': {
        'command': 'INSERT INTO users_customuser (id, username, email, password, is_superuser, first_name, last_name, is_staff, is_active, date_joined, is_moderator, bio) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        'insert': f"[(row['id'], row['username'], row['email'], 'qqq', False, row['username'], row['username'], False, False, datetime.datetime.now(), False, 'Hello!')]"
    },
    'category.csv': {
        'command': 'INSERT INTO reviews_category (name, slug) VALUES(?, ?)',
        'insert': "[(row['name'], row['slug'])]"
    },
    'genre.csv': {
        'command': 'INSERT INTO reviews_genre (name, slug) VALUES(?, ?)',
        'insert': "[(row['name'], row['slug'])]"
    },
    'genre_title.csv': {
        'command': 'INSERT INTO reviews_title_genre (title_id, genre_id) VALUES(?, ?)',
        'insert': "[(row['title_id'], row['genre_id'])]"
    },
    'titles.csv': {
        'command': 'INSERT INTO reviews_title (name, year, category_id) VALUES(?, ?, ?)',
        'insert': "[(row['name'], row['year'], row['category'])]"
    },
    'review.csv': {
        'command': 'INSERT INTO reviews_review (title_id, text, author_id, score, pub_date) VALUES(?, ?, ?, ?, ?)',
        'insert': "[(row['title_id'], row['text'], row['author'], row['score'], row['pub_date'])]"
    },
    'comments.csv': {
        'command': 'INSERT INTO reviews_comment (review_id, text, author_id, pub_date) VALUES(?, ?, ?, ?)',
        'insert': "[(row['review_id'], row['text'], row['author'], row['pub_date'])]"
    },
    
}


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        connection = sqlite3.connect(path_db)
        cursor = connection.cursor()
        for key, item in all_csv_files.items():
            insert_records = item['command']
            path_csv = Path(dir_path, 'static', 'data', key)
            with open(path_csv, newline='') as csvfile:
                spamreader = csv.DictReader(csvfile)
                for row in spamreader:
                    cursor.executemany(
                        insert_records,
                        eval(item['insert'])
                    )
                    connection.commit()
        connection.close()

        self.stdout.write('Записи добавленны в бд!')

#def handle(self, *args, **options):
#        connection = sqlite3.connect(path_db)
#        cursor = connection.cursor()
#        for key, item in all_csv_files.items():
#        insert_records = "INSERT INTO reviews_category (name, slug) VALUES(?, ?)"
#        with open(path_csv, newline='') as csvfile:
#            spamreader = csv.DictReader(csvfile)
#            for row in spamreader:
#                cursor.executemany(
#                    insert_records,
#                    [(row['name'], row['slug'])]
#                )
#                connection.commit()
#        connection.close()
#
#        self.stdout.write('Записи добавленны в бд!')