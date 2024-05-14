import os
import django
from django.conf import settings

# This is a plain python script that loads and sets up django before mucking about
# with the database using the ORM. You can also use this approach to use the templating
# system or whatever part of django you want. You would use this by running:
# python standalone_script.py
# just like any normal python script.

### NOTE!
# This is only for standalone scripts

# Setup django BEFORE you start importing your models
# Two options, either set DJANGO_SETTINGS_MODULE:
os.environ["DJANGO_SETTINGS_MODULE"] = "django_library.settings"
# or call configure:
# settings.configure(DEBUG=True)
# if you're calling configure to use the ORM, you'd need to give it the DB configuration

# Next call django.setup()
django.setup()

from random import choice, sample
from datetime import date

# Now you have django, so you can import models and do stuff as normal
from library.models import Author, Book, Reader

def make_names():
    first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Evelyn', 'Farrah', 'Gina', 'Rooster', 'Sam', 'Telly', 'Umberto', 'Vera', 'William', 'Xavier', 'Zed']
    last_names = ['Harmon', 'Ivanov', 'Jones', 'Kirkland', 'Lavrov', 'Marples', 'Namath', 'Oppenheimer', 'Petrov', 'Quail', 'Rooster', 'Snake']

    return f"{choice(first_names)} {choice(last_names)}"

def make_title():
    noun = ['Anne', 'Night', 'Dogs', 'Sister', 'Brother', 'House', 'Story', ]
    preposition = ['on', 'of', 'in']
    adjective = ['Green', 'Blue', 'Bald', 'Dark', 'High', 'Wet', 'Muddy', 'Grey', 'Flat',]
    location = ['Gables', 'Mountain', 'Hill', 'River', 'Park', 'Walk', 'Haven', 'Statue', 'Stadium', 'Valley']

    return f"{choice(noun)} {choice(preposition)} {choice(adjective)} {choice(location)}"

def make_book_info():
    return {
        'title': make_title(),
        'pub_date': date(year=choice(range(1900,2024)), month=choice(range(1,13)), day=choice(range(1,29)))
    }

def create_data():
    
    author_list = [Author.objects.create(name=make_names()) for i in range(10)]

    book_list = [Book.objects.create(**make_book_info(), author=choice(author_list)) for b in range(50)]

    reader_list = [Reader.objects.create(name=make_names(), state="KY") for i in range(50)]

    for reader in reader_list:
        # Have to create both sides of the manytomany then add one to the other
        # use splat operator to expand array into arguments
        reader.books.add(*sample(book_list, choice(range(3,8))))


def clean_all_data():
    print("Cleaning up...")
    Author.objects.all().delete()
    Book.objects.all().delete()
    Reader.objects.all().delete()
    print("Done")

def print_label_queryset(label, queryset):
    print(f"**** {label} ****")
    for i in queryset:
        print(i)
    print("\n")

def main():
    print("Start")
    book_count = Book.objects.count()
    if book_count == 0:
        create_data()
    else:
        print("Not making new data")


    
    queryset = Book.objects.all()
    print_label_queryset("Books", queryset)


    
    queryset = Author.objects.all()
    print_label_queryset("Author", queryset)

    queryset = Reader.objects.all()
    print_label_queryset("Reader", queryset)

    # For at least 3 authors, connect them to multiple books
    # I already did this, but:
    
    author = Author(name=make_names())
    author.save()
    # could also create the books one at a time
    # Book.object.create() or Book(...).save()
    book = Book.objects.bulk_create([
        Book(title="Boring Book", pub_date=date(year=2001, month=1, day=1), author=author),
        Book(title="Boringer Book", pub_date=date(year=2005, month=7, day=15), author=author),
        Book(title="Boringest Book", pub_date=date(year=2009, month=9, day=12), author=author),
    ])
    print("**** Author with multiple books ****")
    print("Author: ", author)
    for b in author.book_set.all():
        print(f"  {b}")

    # List all authors with a name containing an “S”
    authors = Author.objects.filter(name__contains="S")
    print_label_queryset("Authors with 'S' in their name", authors)

    # List all books published before 1984
    books = Book.objects.filter(pub_date__year__lt=1984)
    print_label_queryset("Books before 1984", books)

    # Several of these can be done with annotations
    # List all authors who have written multiple books
    for a in Author.objects.all():
        if a.book_set.count() > 1:
            print(f"Author: {a} wrote {a.book_set.count()} books")

    # List the author who has written the most books.  If a tie, list them all.
    # List the author who has written the least books.  If a tie, list them all.
    most = 0
    least = 100
    authors_with_most = []
    authors_with_least = []
    for a in Author.objects.all():
        count = a.book_set.count()
        if count > most:
            most = count
            authors_with_most = [a]
        elif count == most:
            authors_with_most.append(a)
        if count < least:
            least = count
            authors_with_least = [a]
        elif count == least:
            authors_with_least.append(a)

    print(f"The most books pub'd by an author is: {most} and these authors did it:")
    for i in authors_with_most:
        print(i)
    
    print(f"The least books pub'd by an author is: {least} and these authors did it:")
    for i in authors_with_least:
        print(i)


    
    # List all books a reader has read
    reader = Reader.objects.first()
    print_label_queryset(f"Reader: {reader}'s books", reader.books.all())

    print("\n")
    # List the reader who has read the most books.  If a tie, list them all.
    most_reader = None # This time I'm saving the reader
    for r in Reader.objects.all():
        if not most_reader:
            most_reader = [r]
        elif r.books.count() > most_reader[0].books.count():
            most_reader = [r]
        elif r.books.count() == most_reader[0].books.count():
            most_reader.append(r)

    print(f"Readers {most_reader} has read the most books at {most_reader[0].books.count()}")
    print("\n")

    # List the author whose books have been read the most
    # List the top three most popular books
    # for book in Book.objects.filter(reader_set__count__gt=1):
    #     print(book)


    # Find a reader’s favorite author (The one that occurs most frequently in the books they have read)  If a tie, list them all.
    # for b in reader.books.all():
    #     print(b.author)


    # clean_all_data()

if __name__=="__main__":
    main()