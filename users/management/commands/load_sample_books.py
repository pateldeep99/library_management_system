from django.core.management.base import BaseCommand
from users.models import Book

class Command(BaseCommand):
    help = 'Load sample book data'

    def handle(self, *args, **options):
        sample_books = [
            {
                'book_title': 'To Kill a Mockingbird',
                'book_author': 'Harper Lee',
                'category': 'Fiction',
                'book_copies': 5,
                'publication_year': 1960,
                'publication_name': 'J.B. Lippincott & Co.',
                'book_isbn': '9780061120084'
            },
            {
                'book_title': '1984',
                'book_author': 'George Orwell',
                'category': 'Dystopian Fiction',
                'book_copies': 8,
                'publication_year': 1949,
                'publication_name': 'Secker & Warburg',
                'book_isbn': '9780451524935'
            },
            {
                'book_title': 'Pride and Prejudice',
                'book_author': 'Jane Austen',
                'category': 'Romance',
                'book_copies': 6,
                'publication_year': 1813,
                'publication_name': 'T. Egerton',
                'book_isbn': '9780141439518'
            },
            {
                'book_title': 'The Great Gatsby',
                'book_author': 'F. Scott Fitzgerald',
                'category': 'Classic Literature',
                'book_copies': 4,
                'publication_year': 1925,
                'publication_name': 'Charles Scribner\'s Sons',
                'book_isbn': '9780743273565'
            },
            {
                'book_title': 'The Catcher in the Rye',
                'book_author': 'J.D. Salinger',
                'category': 'Coming-of-age Fiction',
                'book_copies': 3,
                'publication_year': 1951,
                'publication_name': 'Little, Brown and Company',
                'book_isbn': '9780316769174'
            },
            {
                'book_title': 'Harry Potter and the Philosopher\'s Stone',
                'book_author': 'J.K. Rowling',
                'category': 'Fantasy',
                'book_copies': 10,
                'publication_year': 1997,
                'publication_name': 'Bloomsbury',
                'book_isbn': '9780747532699'
            },
            {
                'book_title': 'The Lord of the Rings',
                'book_author': 'J.R.R. Tolkien',
                'category': 'Fantasy',
                'book_copies': 7,
                'publication_year': 1954,
                'publication_name': 'Allen & Unwin',
                'book_isbn': '9780544003415'
            },
            {
                'book_title': 'The Alchemist',
                'book_author': 'Paulo Coelho',
                'category': 'Philosophical Fiction',
                'book_copies': 5,
                'publication_year': 1988,
                'publication_name': 'HarperCollins',
                'book_isbn': '9780062315007'
            },
            {
                'book_title': 'Dune',
                'book_author': 'Frank Herbert',
                'category': 'Science Fiction',
                'book_copies': 4,
                'publication_year': 1965,
                'publication_name': 'Chilton Books',
                'book_isbn': '9780441172719'
            },
            {
                'book_title': 'The Hitchhiker\'s Guide to the Galaxy',
                'book_author': 'Douglas Adams',
                'category': 'Science Fiction Comedy',
                'book_copies': 6,
                'publication_year': 1979,
                'publication_name': 'Pan Books',
                'book_isbn': '9780345391803'
            },
            {
                'book_title': 'Brave New World',
                'book_author': 'Aldous Huxley',
                'category': 'Dystopian Fiction',
                'book_copies': 5,
                'publication_year': 1932,
                'publication_name': 'Chatto & Windus',
                'book_isbn': '9780060850524'
            },
            {
                'book_title': 'The Da Vinci Code',
                'book_author': 'Dan Brown',
                'category': 'Mystery Thriller',
                'book_copies': 8,
                'publication_year': 2003,
                'publication_name': 'Doubleday',
                'book_isbn': '9780307474278'
            },
            {
                'book_title': 'Gone Girl',
                'book_author': 'Gillian Flynn',
                'category': 'Psychological Thriller',
                'book_copies': 4,
                'publication_year': 2012,
                'publication_name': 'Crown Publishing Group',
                'book_isbn': '9780307588364'
            },
            {
                'book_title': 'The Girl with the Dragon Tattoo',
                'book_author': 'Stieg Larsson',
                'category': 'Crime Fiction',
                'book_copies': 3,
                'publication_year': 2005,
                'publication_name': 'Norstedts Förlag',
                'book_isbn': '9780307269751'
            },
            {
                'book_title': 'Educated',
                'book_author': 'Tara Westover',
                'category': 'Memoir',
                'book_copies': 6,
                'publication_year': 2018,
                'publication_name': 'Random House',
                'book_isbn': '9780399590504'
            },
            {
                'book_title': 'Sapiens',
                'book_author': 'Yuval Noah Harari',
                'category': 'History',
                'book_copies': 5,
                'publication_year': 2011,
                'publication_name': 'Dvir Publishing',
                'book_isbn': '9780062316097'
            },
            {
                'book_title': 'The Silent Patient',
                'book_author': 'Alex Michaelides',
                'category': 'Psychological Thriller',
                'book_copies': 7,
                'publication_year': 2019,
                'publication_name': 'Celadon Books',
                'book_isbn': '9781250301697'
            },
            {
                'book_title': 'Where the Crawdads Sing',
                'book_author': 'Delia Owens',
                'category': 'Mystery Fiction',
                'book_copies': 5,
                'publication_year': 2018,
                'publication_name': 'G.P. Putnam\'s Sons',
                'book_isbn': '9780735219090'
            },
            {
                'book_title': 'Atomic Habits',
                'book_author': 'James Clear',
                'category': 'Self-Help',
                'book_copies': 8,
                'publication_year': 2018,
                'publication_name': 'Avery',
                'book_isbn': '9780735211292'
            },
            {
                'book_title': 'The Power of Now',
                'book_author': 'Eckhart Tolle',
                'category': 'Spirituality',
                'book_copies': 4,
                'publication_year': 1997,
                'publication_name': 'Namaste Publishing',
                'book_isbn': '9781577314806'
            }
        ]

        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                book_isbn=book_data['book_isbn'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'Created: {book.book_title}')
            else:
                self.stdout.write(f'Already exists: {book.book_title}')

        self.stdout.write(self.style.SUCCESS('Sample books loaded successfully!'))