from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Book, BorrowedBook
from books.forms import LoginForm
import csv
from natsort import natsorted # type: ignore
from django.db.models import Q



# Book List View
def book_list(request):
    query = request.GET.get('q', '')  # Get search query
    books = Book.objects.all()  # Start with all books

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))  
        # Ensure filtering happens on QuerySet before conversion

    books = natsorted(books, key=lambda b: b.title.lower())  # Natural sorting on filtered results

    borrowed_book_ids = {}
    if request.user.is_authenticated:
        borrowed_books = BorrowedBook.objects.filter(user=request.user, returned=False)
        borrowed_book_ids = {borrowed.book.id: borrowed for borrowed in borrowed_books}

    return render(request, 'book_list.html', {'books': books, 'borrowed_book_ids': borrowed_book_ids, 'query': query})


# Borrow Request
@login_required
def request_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.quantity <= 0:
        messages.error(request, "Book is out of stock.")
        return redirect('book_list')

    if BorrowedBook.objects.filter(user=request.user, book=book, approved=False, returned=False).exists():
        messages.warning(request, "You already have a pending request for this book.")
        return redirect('book_list')

    BorrowedBook.objects.create(user=request.user, book=book, approved=False, returned=False)
    messages.success(request, "Borrow request sent to admin.")
    return redirect('book_list')


# Return Book
@login_required
def return_book(request, book_id):
    borrowed_book = BorrowedBook.objects.filter(user=request.user, book_id=book_id, returned=False, approved=True).first()

    if borrowed_book:
        borrowed_book.returned = True
        borrowed_book.save()

        book = borrowed_book.book
        book.quantity += 1
        book.save()

        messages.success(request, "Book returned successfully!")
    else:
        messages.error(request, "You cannot return this book.")

    return redirect('book_list')

# Admin Dashboard
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    borrow_requests = BorrowedBook.objects.filter(approved=False, returned=False)  # Pending requests
    borrow_history = BorrowedBook.objects.all().order_by('-borrowed_at')  # History sorted by latest

    return render(request, 'admin_dashboard.html', {
        'borrow_requests': borrow_requests,
        'borrow_history': borrow_history
    })


# Approve Borrow Request
@user_passes_test(lambda u: u.is_staff)
def approve_request(request, request_id):
    borrow_request = get_object_or_404(BorrowedBook, id=request_id)

    if borrow_request.book.quantity > 0:
        borrow_request.approved = True
        borrow_request.book.quantity -= 1
        borrow_request.book.save()
        borrow_request.save()
        messages.success(request, f"Request approved for {borrow_request.user.username}.")
    else:
        messages.error(request, "Book is out of stock.")

    return redirect('admin_dashboard')

# Admin login
def admin_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_staff:  
                    login(request, user)
                    return redirect('admin_dashboard')  
                else:
                    messages.error(request, "You do not have admin permissions.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'admin_login.html', {'form': form})

# Admin Logout
def admin_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('book_list')

# User Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Choose a different one.")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Signup successful! Please log in.")
        return redirect("login")

    return render(request, "signup.html")

# User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("book_list")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")


# User Logout
def custom_logout(request):
    logout(request)
    return redirect('book_list')

# Add a Single Book
@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        isbn = request.POST['isbn']
        quantity = int(request.POST['quantity'])

        Book.objects.create(title=title, author=author, isbn=isbn, quantity=quantity)
        messages.success(request, 'Book added successfully!')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_staff)
def upload_books(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        books_added = 0

        for row in reader:
            # Normalize column names to lowercase and strip spaces
            row = {key.lower().strip(): value.strip() for key, value in row.items()}

            isbn = row.get('isbn')  # Use .get() to avoid KeyError

            if not isbn:
                messages.error(request, "Missing 'ISBN' column in the CSV file.")
                return redirect('admin_dashboard')

            if Book.objects.filter(isbn=isbn).exists():
                continue  # Skip if the book exists
            
            try:
                Book.objects.create(
                    title=row.get('title', ''),  
                    author=row.get('author', ''),  
                    isbn=isbn,
                    quantity=int(row.get('quantity', 0)),  
                )
                books_added += 1
            except ValueError:
                messages.error(request, "Invalid quantity value in the CSV file.")
                return redirect('admin_dashboard')

        if books_added == 0:
            messages.info(request, "All books already exist. No new books added.")
        else:
            messages.success(request, f"{books_added} new books added.")

        return redirect('admin_dashboard')

    return render(request, 'upload_books.html')
