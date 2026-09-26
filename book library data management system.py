from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, timedelta
import sys

Base = declarative_base()
engine = create_engine('sqlite:///library.db', echo=False)
Session = sessionmaker(bind=engine)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    year_published = Column(Integer)
    available = Column(Boolean, default=True)

    borrowed_books = relationship('BorrowedBook', back_populates='book', cascade="all, delete")

    def __repr__(self):
        return f"[{'✔' if self.available else '✖'}] {self.title} by {self.author} ({self.year_published})"


class Reader(Base):
    __tablename__ = 'readers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    borrowed_books = relationship('BorrowedBook', back_populates='reader', cascade="all, delete")

    def __repr__(self):
        return f"{self.name} ({self.email})"


class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    reader_id = Column(Integer, ForeignKey('readers.id'))
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    return_due_date = Column(DateTime)

    book = relationship('Book', back_populates='borrowed_books')
    reader = relationship('Reader', back_populates='borrowed_books')


Base.metadata.create_all(engine)


def add_book():
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year = input("Year Published: ").strip()
    session = Session()
    try:
        book = Book(title=title, author=author, year_published=int(year))
        session.add(book)
        session.commit()
        print("Book added.")
    except Exception as e:
        session.rollback()
        print("Failed to add book:", e)
    finally:
        session.close()


def add_reader():
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    session = Session()
    try:
        reader = Reader(name=name, email=email)
        session.add(reader)
        session.commit()
        print("Reader added.")
    except Exception as e:
        session.rollback()
        print("Failed to add reader:", e)
    finally:
        session.close()


def loan_book():
    session = Session()
    try:
        book_id = int(input("Book ID: "))
        reader_id = int(input("Reader ID: "))
        book = session.query(Book).get(book_id)
        reader = session.query(Reader).get(reader_id)

        if not book or not reader:
            print("Invalid book or reader ID.")
            return
        if not book.available:
            print("Book not available.")
            return

        due_date = datetime.utcnow() + timedelta(days=14)
        loan = BorrowedBook(book=book, reader=reader, return_due_date=due_date)
        book.available = False
        session.add(loan)
        session.commit()
        print(f"Book '{book.title}' loaned to {reader.name}. Due {due_date.date()}.")
    except Exception as e:
        session.rollback()
        print("Failed to loan book:", e)
    finally:
        session.close()


def update_book():
    session = Session()
    try:
        book_id = int(input("Book ID to update: "))
        book = session.query(Book).get(book_id)
        if not book:
            print("Book not found.")
            return

        print(f"Current title: {book.title}")
        new_title = input("New title (leave blank to keep): ").strip()
        if new_title:
            book.title = new_title

        new_author = input("New author (leave blank to keep): ").strip()
        if new_author:
            book.author = new_author

        new_year = input("New year (leave blank to keep): ").strip()
        if new_year:
            book.year_published = int(new_year)

        session.commit()
        print("Book updated.")
    except Exception as e:
        session.rollback()
        print("Update failed:", e)
    finally:
        session.close()


def delete_book():
    session = Session()
    try:
        book_id = int(input("Book ID to delete: "))
        book = session.query(Book).get(book_id)
        if not book:
            print("Book not found.")
            return
        session.delete(book)
        session.commit()
        print("Book deleted.")
    except Exception as e:
        session.rollback()
        print("Failed to delete:", e)
    finally:
        session.close()


def delete_reader():
    session = Session()
    try:
        reader_id = int(input("Reader ID to delete: "))
        reader = session.query(Reader).get(reader_id)
        if not reader:
            print("Reader not found.")
            return
        session.delete(reader)
        session.commit()
        print("Reader deleted.")
    except Exception as e:
        session.rollback()
        print("Failed to delete reader:", e)
    finally:
        session.close()


def list_books():
    session = Session()
    books = session.query(Book).all()
    for b in books:
        print(f"{b.id}: {b}")
    session.close()


def list_loans():
    session = Session()
    loans = session.query(BorrowedBook).all()
    for loan in loans:
        print(f"{loan.book.title} -> {loan.reader.name} (Due: {loan.return_due_date.date()})")
    session.close()


def show_loan_duration():
    session = Session()
    loans = session.query(BorrowedBook).all()
    for loan in loans:
        days = (datetime.utcnow() - loan.borrowed_at).days
        print(f"{loan.book.title} loaned to {loan.reader.name} for {days} day(s).")
    session.close()


def reader_history():
    session = Session()
    reader_id = int(input("Reader ID: "))
    loans = session.query(BorrowedBook).filter_by(reader_id=reader_id).all()
    if not loans:
        print("No history found.")
    for loan in loans:
        print(f"{loan.book.title} borrowed on {loan.borrowed_at.date()}, due {loan.return_due_date.date()}")
    session.close()


def main():
    actions = {
        '1': add_book,
        '2': add_reader,
        '3': loan_book,
        '4': update_book,
        '5': delete_book,
        '6': delete_reader,
        '7': list_books,
        '8': list_loans,
        '9': show_loan_duration,
        '10': reader_history,
        '0': lambda: sys.exit("👋 Exiting..."),
    }

    while True:
        print("\n📚 Library Menu:")
        print("1. Add Book")
        print("2. Add Reader")
        print("3. Loan Book")
        print("4. Update Book")
        print("5. Delete Book")
        print("6. Delete Reader")
        print("7. List All Books")
        print("8. List Borrowed Books")
        print("9. Show Loan Durations")
        print("10. Reader Loan History")
        print("0. Exit")

        choice = input("Choose action: ").strip()
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()
















