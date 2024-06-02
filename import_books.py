import os
import django
import psycopg2

# Step 1: Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryManagementSys.settings')

# Step 2: Initialize Django
django.setup()

# Import Django models after setting up Django
from Library.models import Books

# Connection parameters for the source PostgresSQL database
source_conn_params = {
    'dbname': 'postgres',  # Change this to your source database name
    'user': 'postgres',  # Change this to your source database user
    'password': 'animesh',  # Change this to your source database password
    'host': 'localhost',  # Change this to your source database host
    'port': '5432'  # Change this to your source database port
}


def fetch_books_from_source():
    try:
        # Connect to the source PostgresSQL database
        conn = psycopg2.connect(**source_conn_params)
        cursor = conn.cursor()

        # Fetch data from the source books table
        cursor.execute("SELECT * FROM books")  # Adjust the query based on your source table schema
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Convert the data into a list of dictionaries
        books_data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return books_data

    except Exception as e:
        print(f"Error fetching data from source: {e}")
        return []


def import_books_to_django(books_data):
    for book_data in books_data:
        try:
            Books.objects.update_or_create(
                isbn=book_data['isbn'],
                defaults={
                    'title': book_data['title'],
                    'author': book_data['author'],
                    'publisher': book_data['publisher'],
                    'publication_date': book_data['publication_date'],
                    'genre': book_data['genre'],
                    'language': book_data['language'],
                    'pages': book_data['pages'],
                    'cover_image_url': book_data['cover_image_url'],
                    'description': book_data['description'],
                    'price': book_data['price'],
                    'quantity_in_stock': book_data['quantity_in_stock'],
                }
            )
            print(f"Imported/Updated book: {book_data['title']}")

        except Exception as e:
            print(f"Error importing book {book_data['title']}: {e}")


if __name__ == '__main__':
    books_data = fetch_books_from_source()
    if books_data:
        import_books_to_django(books_data)
    else:
        print("No books data fetched from the source database.")
