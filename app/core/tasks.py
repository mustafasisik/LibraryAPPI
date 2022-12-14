import logging
from datetime import datetime, timedelta

from faker import Faker
from .models import Book
from celery import shared_task

from django.contrib.auth.models import User

from .utils.log_handlers import LoggingHandler

logger = logging.getLogger(__name__)
logger.addHandler(LoggingHandler())


@shared_task
def create_more_book(book_count):
    fake = Faker()
    books_count = Book.objects.all().count()
    logger.debug("Book Count", str(books_count))

    for i in range(book_count):
        try:
            name = fake.sentence()
            if len(name) > 100:
                name = name[0:99]
            book = Book()
            book.name = name

            i_string = str(i + books_count)
            barcode = "0" * (7 - len(i_string)) + i_string # create a barcode for book

            book.barcode = barcode
            book.save()
        except Exception as exc:
            logger.error("The book number %s failed due to the %s", i, exc)
    logger.debug("RESULT FOR BOOKS CREATE:", "Successfully Completed")


@shared_task
def remove_all_books():

    for book in Book.objects.all():
        book.delete()
    logger.debug("RESULT FOR BOOKS REMOVE:", "Successfully Completed")


@shared_task
def reserve_all_books():
    user_ids = User.objects.all().values_list('id', flat=True)
    return_date = datetime.now()+timedelta(days=14)
    for book in Book.objects.all():
        try:
            if book.is_deleted or book.is_reserved:
                pass
            else:
                book.is_reserved = True
                book.user_id = user_ids.order_by('?').first()
                book.return_date = return_date
                book.save()
        except Exception as exc:
            logger.error("The book barcode number %s failed due to the %s", book.barcode, exc)
    logger.debug("RESULT FOR ALL BOOKS RESERVATION: ", "Successfully Completed")


@shared_task
def return_all_books():
    for book in Book.objects.all():
        try:
            if book.is_reserved:
                book.is_reserved = False
                book.user_id = -1
                book.return_date = None
                book.save()
        except Exception as exc:
            logger.error("The book barcode number %s failed due to the %s", book.barcode, exc)
    logger.debug("RESULT FOR ALL BOOKS RETURN: ", "Successfully Completed")