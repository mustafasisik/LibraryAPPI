from rest_framework.views import APIView, Response
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Book, PasswordResetCode
from .tasks import create_more_book, remove_all_books, reserve_all_books, return_all_books
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta, datetime
import random, string, logging
from django.db.models import Q


# myList = myApp.objects.filter(is_new__in=[False])


from .utils.log_handlers import LoggingHandler

logger = logging.getLogger(__name__)
logger.addHandler(LoggingHandler())


def home(request):
    user_ids = User.objects.all().values_list('id', flat=True)

    return JsonResponse({"test": user_ids.order_by('?').first()})


class TestAPI(APIView):
    context = {}

    def get(self, request):
        user_ids = User.objects.all().values_list('id', flat=True)
        self.context["test"] = user_ids.order_by('?').first()
        return Response(self.context)


class RegisterUserAPI(APIView):
    context = {}

    def post(self, request):

        email = self.request.POST.get("email")
        username = self.request.POST.get("username")

        if User.objects.filter(email=email).exists():
            self.context["success"] = False
            self.context["message"] = "User with this email is exists!"
        elif User.objects.filter(username=username).exists():
            self.context["success"] = False
            self.context["message"] = "User with this phone is exists!"
        else:
            name = self.request.POST.get("name")
            surname = self.request.POST.get("surname")
            password = self.request.POST.get("password")

            user = User()
            user.username = username
            user.email = email
            user.first_name = name
            user.last_name = surname
            user.set_password(password)
            user.save()
            self.context["success"] = True
            self.context["message"] = "User registered."
        return Response(self.context)


class ForgetPasswordAPI(APIView):
    context = {}

    def post(self, request):
        email = self.request.POST.get("email")
        users = User.objects.filter(email=email)

        if len(users) == 0:
            self.context["success"] = -1
            return Response(self.context)

        user = users.first()

        PasswordResetCode.objects.filter(user=user).update(is_active=False)

        code = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        passwordResetCode = PasswordResetCode()
        passwordResetCode.user = user
        passwordResetCode.code = code
        passwordResetCode.save()
        message = "Your password reset code is: " + code
        send_mail("Forget Password!", message, "mstfssk@gmail.com", [email], fail_silently=False)
        self.context["success"] = True
        self.context["message"] = "We send you an email that contains a password reset code. Please check your email!"
        return Response(self.context)


class ResetPasswordAPI(APIView):
    context = {}

    def post(self, request):
        code = self.request.POST.get("code")
        email = self.request.POST.get("email")
        password = self.request.POST.get("password")

        try:
            password_reset_code = PasswordResetCode.objects.get(user__email=email, code=code)

            if password_reset_code.is_active:
                if password_reset_code.create_date + timedelta(days=1) < timezone.now():
                    self.context["success"] = False
                    self.context["message"] = "The password reset code has expired."
                else:
                    password_reset_code.user.set_password(password)
                    password_reset_code.user.save()
                    self.context["success"] = True
                    self.context["message"] = "Password reset completed."
            else:
                self.context["success"] = False
                self.context["message"] = "Password reset code is not active"

        except:
            self.context["success"] = False
            self.context["message"] = "The code is not found. Please check again!"
        finally:
            pass
        return Response(self.context)


class ReserveBookAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):

        barcode = request.POST.get("barcode")

        try:
            book = Book.objects.get(barcode=barcode)
            if book.is_deleted:
                self.context["success"] = False
                self.context["message"] = "Book is deleted!"
            elif book.is_reserved:
                self.context["success"] = False
                if book.user_id == self.request.user.pk:
                    self.context["message"] = "Book is already reserved by you!"
                else:
                    self.context["message"] = "Book is reserved by other user!"
            else:
                book.is_reserved = True
                book.user_id = self.request.user.pk
                book.return_date = datetime.now()+timedelta(days=14)
                book.save()
                self.context["success"] = True
                self.context["message"] = "Book is reserved to date " + str(book.return_date.date())

        except Exception as exc:
            self.context["success"] = False
            self.context["message"] = "Book is not exists!"
            self.context["Exception"] = "Exception: " + str(exc)
        finally:
            pass
        return Response(self.context)


class ReturnBookAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):
        barcode = request.POST.get("barcode")
        try:
            book = Book.objects.get(barcode=barcode)
            if book.is_deleted:
                self.context["success"] = False
                self.context["message"] = "Book is deleted!"
            elif not book.is_reserved:
                self.context["success"] = False
                self.context["message"] = "Book is not reserved!"
            elif book.user_id == self.request.user.pk:
                book.is_reserved = False
                book.return_date = None
                book.user_id = -1
                book.save()
                self.context["success"] = True
                self.context["message"] = "Book is returned."
            else:
                self.context["success"] = False
                self.context["message"] = "Book is not reserved by other user!"
        except Exception as exc:
            self.context["success"] = False
            self.context["message"] = "Book is not exists!"
            self.context["Exception"] = "Exception: " + str(exc)
        finally:
            pass
        return Response(self.context)


# Superuser Actions
class CreateBookAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):
        if self.request.user.is_superuser:
            name = request.POST.get("name")
            if not name:
                self.context["success"] = False
                self.context["message"] = "Name Error!"
            if not Book.objects.filter(name=name).exists():
                i_string = str(Book.objects.all().count())
                barcode = "0" * (7 - len(i_string)) + i_string # create a barcode for book
                book = Book()
                book.name = name
                book.barcode = barcode
                book.save()
                self.context["success"] = True
                self.context["message"] = "Book is created."
                return Response(self.context)
            else:
                self.context["success"] = False
                self.context["message"] = "Book is exists in database!"
        else:
            self.context["success"] = False
            self.context["message"] = "You are not authorized to perform this action!"
        return Response(self.context)


class DeleteBookAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):
        if self.request.user.is_superuser:
            barcode = request.POST.get("barcode")
            try:
                book = Book.objects.get(barcode=barcode)
                if book.is_deleted:
                    self.context["success"] = False
                    self.context["message"] = "Book is deleted before!"
                elif book.is_reserved:
                    self.context["success"] = False
                    self.context["message"] = "Book is reserved!"
                else:
                    book.is_deleted = True
                    book.save()
                    self.context["success"] = True
                    self.context["message"] = "Book is deleted."
            except:
                self.context["success"] = False
                self.context["message"] = "Book is not exists!"
            finally:
                pass
        else:
            self.context["success"] = False
            self.context["message"] = "You are not authorized to perform this action!"
        return Response(self.context)


class CreateMoreBooksAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):
        if self.request.user.is_superuser:
            book_count = int(request.POST.get("book_count"))
            create_more_book.delay(book_count=book_count)
            self.context["success"] = True
            self.context["message"] = "{} Books is creating...".format(book_count)
        else:
            self.context["success"] = False
            self.context["message"] = "You are not authorized to perform this action!"
        return Response(self.context)


class RemoveAllBooksAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):
        if self.request.user.is_superuser:
            remove_all_books.delay()
            self.context["success"] = True
            self.context["message"] = "Removing all books..."
        else:
            self.context["success"] = False
            self.context["message"] = "You are not authorized to perform this action!"
        return Response(self.context)


class ReserveAllBooksAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):
        if self.request.user.is_superuser:
            reserve_all_books.delay()
            self.context["success"] = True
            self.context["message"] = "Reserving all books..."
        else:
            self.context["success"] = False
            self.context["message"] = "You are not authorized to perform this action!"
        return Response(self.context)


class ReturnAllBooksAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    context = {}

    def post(self, request):
        if self.request.user.is_superuser:
            return_all_books.delay()
            self.context["success"] = True
            self.context["message"] = "Returning all books..."
        else:
            self.context["success"] = False
            self.context["message"] = "You are not authorized to perform this action!"
        return Response(self.context)
