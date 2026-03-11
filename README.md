# BookNook - Book E-commerce

University project for the Databases course (Academic Year 2023-2024). 

BookNook is a web platform dedicated to book lovers, designed to allow users to buy and sell books easily and securely. The application uses Flask for the back-end and PostgreSQL for the database.

---

## Struttura del Progetto

The project is organized with the following file and folder structure:

* **`app.py`**: The main back-end file containing Flask routes, SQLAlchemy models, and application logic.
* **`templates/`**: Folder containing all HTML files for the user interface (e.g., login, cart, profile).
* **`static/img/`**: Folder dedicated to static resources, such as the logo and images used on the website.
* **`db/schema_booknook_db.sql`**: Backup file containing the structural schema of the PostgreSQL database (tables, views, triggers, and roles), stripped of personal data for privacy reasons.

---

## Main Features

The application distinguishes between two types of users via a boolean field in the database, offering targeted features:

**Buyers Area**

* **Search and Filters**: Advanced search bar to find books by title, publisher, category, and price. Results automatically exclude books sold by the user themselves.
* **Cart Management**: Addition of products to the cart with dynamic, real-time checking of the actual quantity remaining in stock.
* **Orders and Notifications**: Purchase completion and receipt of automatic notifications whenever the seller updates the order status (e.g., "In Preparation", "Shipped").
* **Reviews**: Feedback system to rate purchased books, with automatic calculation of the average rating.

**Sellers Area**

* **Catalog Management**: Insertion of new books or addition of copies to existing titles (with auto-completion feature via JavaScript) specifying quantity, price, and condition.
* **Product Removal**: Logical deletion of a book from the storefront simply by setting its quantity to zero.
* **Sales Dashboard**: Dedicated screen to view orders received from buyers and update their shipping status.

**Behind the Scenes (Database and Security)**

* **Password Security**: All passwords are encrypted using the SHA-256 algorithm before saving.
* **PostgreSQL Role Management**: Registration physically creates a user in the PostgreSQL database, assigning them the formal permissions (`GRANT`) appropriate for their role.
* **Integrity Triggers**: A *Before Trigger* prevents adding unavailable quantities to the cart, while an *After Trigger* manages the automatic activation of order notifications.
* **Optimized Views**: Use of an SQL View to pre-calculate and aggregate average book reviews.

---

## How to Use the Project (Installation and Execution from Terminal)

Follow these steps to run the application locally on your computer using the command line.

### 1. Database Setup (Empty Schema)
Being a public repository, the provided database contains only the logical structure and no sensitive data. Make sure you have **PostgreSQL** installed and configured in your system's environment variables.

1. Open the terminal and create a new empty database named `progetto_basi` by running this command:
   ```bash
   createdb -U postgres progetto_basi
   ```
2. Restore the structural schema by importing the SQL file provided in the repository:
   ```bash
    psql -U postgres -d progetto_basi -f schema_booknook_db.sql
   ```
   
Note: Upon starting the app, the database will initially be empty. Register as a new user from the web interface to start populating it!

### 2. Python Environment Setup

1. Make sure you have Python installed on your system.
2. Open the terminal in the main project folder (where the `app.py` file is located).
3. Install all necessary dependencies by running:
   ```bash
    pip install Flask Flask-SQLAlchemy Flask-Login Flask-Migrate psycopg2 sqlalchemy
   ```
(Tip: it's good practice to first create a virtual environment with ```python -m venv venv``` and activate it, then run the ```pip install``` command).

### 3. Connection and Startup

1. Open the `app.py` file with your favorite text editor (e.g., VS Code, PyCharm, or Notepad).
2. On line 14, verify that the URI connection string matches the password of your local PostgreSQL server:
   ```Python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:latuapassword@localhost/progettoBasi'
   ```
3. Go back to the terminal and start the server by running:
   ```bash
   python app.py
   ```
4. Open your browser and connect to the address ```http://127.0.0.1:5000```.
