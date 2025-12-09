Курсовий проєкт — Fleet Management System (Варіант 7)
1. Загальна інформація
     
Назва: Fleet Management System
Мета проєкту: Розробити інформаційну систему для керування автопарком з адміністративною та операційною (store) частинами, REST API, генерацією звітів (експорт у Excel), контролем технічного обслуговування, обліком витрат і поїздок.
Студент: Ігор Знетиняк
Спеціальність: Комп'ютерна інженерія (ІоТ)

2. Технологічні вимоги / стек

Мова: Python 3.12+ (у проєкті використовується 3.13)

Веб-фреймворк: Flask

ORM: SQLAlchemy

Міграції: Flask-Migrate

Шаблонізація: Jinja2

Frontend: HTML / CSS (+ кастомні стилі, можна Bootstrap при бажанні)

БД: SQLite

Формат експорту звітів: Excel (openpyxl)

Тестування: pytest (опціонально)

3. Архітектура проєкту

Трирівнева архітектура:

Presentation layer (controllers) — Flask route handlers + шаблони (Store/Admin).

Service layer (services) — бізнес-логіка: робота з поїздками, витратами, ТО, звітами.

Data layer (repositories / models) — SQLAlchemy моделі та репозиторії (Repository pattern).

Файлова структура (приклад):

app/
 ├── controllers/        # store_controller.py, admin_controller.py, auth_controller.py, api controllers
 ├── services/           # vehicle_service.py, trip_service.py, expense_service.py, maintenance_service.py, report_service.py
 ├── repositories/       # vehicle_repository.py, trip_repository.py, expense_repository.py, maintenance_repository.py
 ├── models/             # vehicle.py, trip.py, expense.py, maintenance.py, user.py
 ├── reports/            # usage_report.py, expenses_report.py, maintenance_report.py
 ├── templates/          # Store/, Admin/, Auth/, base.html
 ├── static/             # css/, js/
 ├── extensions.py       # db, migrate initialization
 ├── run.py              # запуск
 └── config.py

4. Основні сутності (UML — класи)

Короткий опис сутностей і атрибутів:

Vehicle

id, brand, model, vin, year, available, odometer, other_meta

Driver

id, full_name, license_number, phone, email

Trip

id, vehicle_id, driver_id, start_time, end_time, start_km, end_km, distance, status

Expense

id, vehicle_id, expense_type, amount, date, description

Maintenance

id, vehicle_id, maintenance_type, date, next_date, notes

User

id, full_name, email, password, role — (roles: user, admin)

5. Бізнес-логіка (Service layer)

VehicleService

CRUD, пошук, відмітка доступності, оновлення пробігу

TripService

Створення поїздки (перевірка доступності авто), закриття поїздки (обчислення пробігу), підрахунок відстані

ExpenseService

Фіксація витрат, підсумки за період, групування по типах

MaintenanceService

Додавання ТО, підрахунок прийдешніх ТО, нагадування

ReportService

Генерація звітів: usage, expenses, maintenance; експорт в Excel

6. Застосовані патерни (GoF + архітектурні)

Repository — всі звернення до БД інкапсульовані в repositories/*.

Service (Facade) — services/* агрегують виклики репозиторіїв; контроллери працюють тільки з сервісами.

Singleton — ініціалізація db (через extensions.py) як єдиний екземпляр.

Strategy — (опціонально) для вибору алгоритму агрегації звітів або правил підрахунку штрафів.

Observer — (опціонально) нотифікації про майбутні ТО / прострочені поїздки.

Factory Method — (опціонально) створення різних типів звітів/експорту (CSV/Excel).

7. REST API (мінімальний набір ендпоінтів)

Базова схема (HTTP метод — маршрут)

Vehicles

GET    /api/vehicles
GET    /api/vehicles/<id>
POST   /api/vehicles
PUT    /api/vehicles/<id>
DELETE /api/vehicles/<id>


Drivers

GET    /api/drivers
GET    /api/drivers/<id>
POST   /api/drivers
PUT    /api/drivers/<id>
DELETE /api/drivers/<id>


Trips

GET    /api/trips
GET    /api/trips/<id>
POST   /api/trips         # start trip
PUT    /api/trips/<id>    # close trip
DELETE /api/trips/<id>


Expenses

GET    /api/expenses
POST   /api/expenses
GET    /api/expenses/<id>


Maintenance

GET    /api/maintenance
POST   /api/maintenance
GET    /api/maintenance/<id>

8. UI / сторінки 

Store/dashboard.html — головна (щипки: карти, швидкий доступ до звітів)

Store/vehicles.html — список авто + пошук, пагінація

Store/vehicle_detail.html — деталі авто, список поїздок, витрат

Store/trips.html, Store/trip_detail.html

Store/expenses.html

Store/reports_*.html — сторінки звітів із фільтрами та кнопками експорту

Admin/* — CRUD інтерфейси для адміна

9. Підготовка до запуску (інструкція)

Клонувати репозиторій:

git clone <твій-repo-url>
cd fleet_management_full_project


Створити віртуальне оточення і встановити залежності:

python -m venv .venv
source .venv/bin/activate      # або .venv\Scripts\activate (Windows)
pip install -r requirements.txt

Запуск:

python run.py
# або
flask run


Відкрити: http://127.0.0.1:5000/store/dashboard
