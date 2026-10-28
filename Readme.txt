LITTLE LEMON - BACK-END DEVELOPER CAPSTONE PROJECT
===================================================
Django + Django REST Framework + MySQL + Djoser (token auth)

SETUP
-----
1. python -m venv venv  &&  activate it
2. pip install -r requirements.txt
3. Create MySQL database:  CREATE DATABASE littlelemon;
4. Edit DATABASES in littlelemon/settings.py (or set env vars DB_NAME, DB_USER,
   DB_PASSWORD, DB_HOST, DB_PORT) with your MySQL credentials.
   (No MySQL? run with USE_SQLITE=1 to use SQLite instead.)
5. python manage.py makemigrations restaurant
6. python manage.py migrate
7. python manage.py createsuperuser   (optional, for /admin/)
8. python manage.py runserver
9. Run unit tests:  python manage.py test

PATHS TO TEST (base URL http://127.0.0.1:8000)
----------------------------------------------
HTML pages (served by Django templates)
  GET   /                       Home page
  GET   /menu/                  Menu page (reads from database)
  GET   /admin/                 Django admin

User registration & authentication (Djoser)
  POST  /auth/users/            Register  {"username": "...", "password": "..."}
  POST  /auth/token/login/      Get token {"username": "...", "password": "..."}
  GET   /auth/users/me/         Current user (header: Authorization: Token <token>)
  POST  /auth/token/logout/     Logout (invalidate token)

Menu API (GET is public; POST/PUT/PATCH/DELETE need token)
  GET    /api/menu/             List menu items
  POST   /api/menu/             Create  {"title":"Greek Salad","price":"12.50","inventory":20}
  GET    /api/menu/1/           Single item
  PUT    /api/menu/1/           Update
  DELETE /api/menu/1/           Delete

Table booking API (token required for all)
  GET    /api/tables/           List bookings
  POST   /api/tables/           Create {"name":"Anna","no_of_guests":4,"booking_date":"2026-12-01T19:00:00Z"}
  GET    /api/tables/1/         Single booking
  PUT    /api/tables/1/         Update
  DELETE /api/tables/1/         Delete

INSOMNIA TIP
------------
After logging in at /auth/token/login/, copy "auth_token" and add header
   Authorization: Token <auth_token>
to requests to /api/menu/ and /api/tables/.
