# Library Api
## Python-Django Library API
With this software, hundreds of thousands of books can be added to a library with a single request, and all books can be reserved to users randomly. Again, you can cancel the reservations of all the books with a single request. By registering as a normal user, you can reserve a book and return your book.

## Running sample
http://44.212.3.24/

## Requisites
* Python => python:3.8-slim
* MongoDB => mongo:latest
* PostgreSQL => postgres:12 
* Redis => redis:6
* Celery
* Nginx

## Can be executed with Docker
* Docker
* Docker-compose

# Running the app
Firstly create the .env file to project folder(Libray/.env
```
# Django App
DEBUG=False
SECRET_KEY=somesecretkey
DJANGO_ALLOWED_HOSTS=*

# Mongo DB
MONGO_DB_HOST=mongo
MONGO_DB_PORT=27017
MONGO_DB_NAME=mongo_db
MONGO_DB_USERNAME=root
MONGO_DB_PASSWORD=root
MONGO_DB_URI=mongodb://root:root@mongo:27017

# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_DB=app_db
POSTGRES_USER=app_db_user
POSTGRES_PASSWORD=supersecretpassword
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=supersecretpassword
BROKER_URL=redis://:supersecretpassword@redis:6379/0
REDIS_CHANNEL_URL=redis://:supersecretpassword@redis:6379/1
CELERY_URL=redis://:supersecretpassword@redis:6379/0
```

After .env file created run this command
```
docker-compose up
```

## API USAGE
#### There are two user created at first:
* Admin User (Superuser) admin@example.com
  * admin: admin123 
  * We can login to django admin panel with this user
  * Endpoints that require high privileges in API usage can be used by this user.
* Library User (Standart user) library.user@example.com
  * librayuser: user123
  * This user is a normal library user, he/she can only perform operations related to himself.

# Usage

* To check that the system is working, you can check the database by connecting to the django panel via the /admin endpoint with the 'admin' user.
* To start the system, you can create as many books as you want via the api/create_more_book endpoint with the 'admin' user.
* If you want to check _/api/forgot_password_ endpoint you need to change EMAIL_HOST_USER and EMAIL_HOST_PASSWORD with yours in settings.py file
## ENDPOINTS:


##### Login
```POST api/login```

- username (required) // unique
- password (required) // str

Response: ```{"token": "4ced91d45bd77cd0ce67e6b54f97dc1f0b64b248"}```


##### Register
```POST api/register_user```

- username (required) // unique
- email (required) // 
- password (required) // str
- name (required) //  str
- surname (required) //  str

Response: ```{"success": true, "message": "User registered."}```

##### Forget Password
```POST api/forget_password```

- email (required) // 

Response: ```{"success": true, "message": "We send you an email that contains a password reset code. Please check your email!"}```

##### Reset Password
```POST api/reset_password```

- code (required) // an 8 letter code
- email (required) // 
- password (required) // 

Response: ```{"success": true, "message": "Password reset completed."}```


##### Reserve Book
Required Headers: SessionAuthentication, BasicAuthentication, TokenAuthentication

```POST api/reserve_book```

- barcode (required) // must be 7 digits number as string("0000120")

Response: ```{"success": true, "message": "Book is reserved to date 12.07.2022"}```

##### Return Book
Required Headers: Authorization

```POST api/return_book```

- barcode (required) // must be 7 digits number as string("0000120")

Response: ```{"success": true, "message": "Book is returned."}```

##### Create Book
Required Headers: Authorization
* _Must be superuser_

```POST api/create_book```

- name (required) // book name as str

Response: ```{"success": true, "message": "Book is created."}```

##### Delete Book
Required Headers: Authorization
* _Must be superuser_
* Save book as deleted but not remove completely.

```POST api/delete_book```

- name (required) // book name as str

Response: ```{"success": true, "message": "Book is deleted."}```

##### Create More Book
Required Headers: Authorization
* _Must be superuser_
* Tt works with celery and creates book with random name with Faker

```POST api/create_more_book```

- book_count (required) // int ex(100000)

Response: ```{"success": true, "message": "100000 Books is creating..."}```

##### Remove All Book
Required Headers: Authorization
* _Must be superuser_
* Removes all books completely

```POST api/remove_all_books```

Response: ```{"success": true, "message": "Removing all books..."}```

##### Reserve All Book
Required Headers: Authorization
* _Must be superuser_
* Reserving all books for all users randomly

```POST api/reserve_all_books```

Response: ```{"success": true, "message": "Reserving all books..."}```

##### Return All Book
Required Headers: Authorization
* _Must be superuser_
* Returning all books

```POST api/return_all_books```

Response: ```{"success": true, "message": "Returning all books..."}```