# Library Management System

A web-based Library Management System built using **Django** for backend and **HTML, CSS, JavaScript** for frontend. The system allows users to browse, borrow, and return books, while the admin can manage books and track borrowing history.

## Features

- User authentication (Login/Logout)
- Browse available books
- Search books by title, author, or ISBN
- Request to borrow books (with admin approval)
- Return borrowed books
- Admin dashboard for managing books (CSV upload support)
- Borrowing history tracking
- Responsive design

## Technologies Used

- **Backend:** Django, SQLite
- **Frontend:** HTML, CSS, JavaScript (Vanilla JS)
- **Authentication:** Django built-in user authentication

## Installation

### Prerequisites
- Python 3.10+
- Django 5+
- Virtual environment (recommended)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/library-management.git
   cd library-management
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser for admin access:
   ```sh
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```sh
   python manage.py runserver
   ```
7. Access the application in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

### User
- Register/Login
- Browse and search for books
- Request to borrow books
- Return borrowed books

### Admin
- Approve or reject borrow requests
- Upload books via CSV or add manually
- View borrowing history

## CSV Upload Format

The CSV file for book uploads must have the following columns:

```csv
Title,Author,ISBN,Quantity
"Book Title","Author Name",1234567890123,5
```

## Contributing
Pull requests are welcome. Please follow these steps:
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## License
This project is licensed under the MIT License.

---
**Author:** Muslim  
**GitHub:** [Muslim-WD](https://github.com/Muslim-WD)

