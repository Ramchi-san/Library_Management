import mysql.connector
from datetime import date, timedelta
import tkinter as tk
from tkinter import ttk, messagebox

class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="12345",
            database="library_management"
        )
        self.cursor = self.connection.cursor()

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

# Create a global instance of the DatabaseConnection
db = DatabaseConnection()

# Make sure to call this function at the end of your script
def cleanup():
    db.close()

class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
    
    def add_to_db(self):
        query = "INSERT INTO books (title, author, isbn, quantity) VALUES (%s, %s, %s, %s)"
        values = (self.title, self.author, self.isbn, self.quantity)
        db.cursor.execute(query, values)
        db.connection.commit()

class Member:
    def __init__(self, member_name, email):
        self.member_name = member_name
        self.email = email
        self.join_date = date.today()
    
    def add_to_db(self):
        query = "INSERT INTO members (member_name, email, join_date) VALUES(%s, %s, %s)"
        values = (self.member_name, self.email, self.join_date)
        db.cursor.execute(query, values)
        db.connection.commit()

class Loan:
    def __init__(self, book_id, member_id):
        self.book_id = book_id
        self.member_id = member_id
        self.loan_date = date.today()
        self.due_date = self.loan_date + timedelta(days=14)
        self.return_date = None

    def add_to_db(self):
        query = "INSERT INTO loans (book_id, member_id, loan_date, due_date) VALUES (%s, %s, %s, %s)"
        values = (self.book_id, self.member_id, self.loan_date, self.due_date)
        db.cursor.execute(query, values)
        db.connection.commit()
    
    def return_book(self):
        self.return_date = date.today()
        query = "UPDATE loans SET return_date = % WHERE book_id = % AND member_id = %s AND return_date IS NULL"
        values = (self.return_date, self.book_id, self.member_id)
        db.cursor.execute(query, values)
        db.connection.commit()
    
def add_book(title, author, isbn, quantity):
    book = Book(title, author, isbn, quantity)
    book.add_to_db()
    print(f"Book '{title}' added successfully.")
    
def add_member(name, email):
    member = Member(name, email)
    member.add_to_db()
    print(f"Member '{name}' added successfully.")

def search_books(keyword):
    query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s"
    values = (f"%{keyword}", f"%{keyword}", f"%{keyword}")
    db.cursor.execute(query, values)
    return db.cursor.fetchall()

def check_out_book(book_id, member_id):
    #Check if book is available
    query = "SELECT quantity FROM books WHERE book_id = %s"
    db.cursor.execute(query, (book_id,))
    result = db.cursor.fetchone()
    if result and result[0] > 0:
        #Create loan
        loan = Loan(book_id, member_id)
        loan.add_to_db()
        #Update book quantity
        query = "UPDATE books SET quantity = quantity -1 WHERE book_id = %s"
        db.cursor.execute(query, (book_id,))
        db.connection.commit()
        print("Book checked out successfully.")
    else:
        print("Book not available for checkout.")

def return_book(book_id, member_id):
    loan = Loan(book_id, member_id)
    loan.return_book()

    #Update book quantity
    query = "UPDATE books SET quantity = quantity + 1 WHERE book_id = %s"
    db.cursor.execute(query, (book_id,))
    db.connection.commit()
    print("Book returned successfully.")

def get_overdue_loans():
    today = date.today()
    query = """
    SELECT m.member_name, b.title, l.due_date
    FROM loans l
    JOIN members m ON l.member_id = m.member_id
    JOIN books b ON l.book_id = b.book_id
    WHERE l.due_date < %s AND l.return_date IS NULL
    """
    db.cursor.execute(query, (today,))
    return db.cursor.fetchall()

class LibraryManagementGUI:
    def __init__(self, master):
        self.master = master
        master.title("Library Management System")
        master.geometry("500x400")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill="both")

        self.add_book_frame = ttk.Frame(self.notebook)
        self.add_member_frame = ttk.Frame(self.notebook)
        self.search_books_frame = ttk.Frame(self.notebook)
        self.checkout_return_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.add_book_frame, text="Add Book")
        self.notebook.add(self.add_member_frame, text="Add Member")
        self.notebook.add(self.search_books_frame, text="Search Books")
        self.notebook.add(self.checkout_return_frame, text="Checkout/Return")

        self.create_add_book_widgets()
        self.create_add_member_widgets()
        self.create_search_books_widgets()
        self.create_checkout_return_widgets()

    def create_add_book_widgets(self):
        ttk.Label(self.add_book_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.add_book_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_book_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(self.add_book_frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_book_frame, text="ISBN:").grid(row=2, column=0, padx=5, pady=5)
        self.isbn_entry = ttk.Entry(self.add_book_frame)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_book_frame, text="Quantity:").grid(row=3, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.add_book_frame)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.add_book_frame, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

    def create_add_member_widgets(self):
        ttk.Label(self.add_member_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.member_name_entry = ttk.Entry(self.add_member_frame)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_member_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.member_email_entry = ttk.Entry(self.add_member_frame)
        self.member_email_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.add_member_frame, text="Add Member", command=self.add_member).grid(row=2, column=0, columnspan=2, pady=10)

    def create_search_books_widgets(self):
        ttk.Label(self.search_books_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.search_books_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.search_books_frame, text="Search", command=self.search_books).grid(row=0, column=2, padx=5, pady=5)

        self.search_results = ttk.Treeview(self.search_books_frame, columns=("Title", "Author", "ISBN", "Quantity"), show="headings")
        self.search_results.heading("Title", text="Title")
        self.search_results.heading("Author", text="Author")
        self.search_results.heading("ISBN", text="ISBN")
        self.search_results.heading("Quantity", text="Quantity")
        self.search_results.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def create_checkout_return_widgets(self):
        ttk.Label(self.checkout_return_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5)
        self.book_id_entry = ttk.Entry(self.checkout_return_frame)
        self.book_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.checkout_return_frame, text="Member ID:").grid(row=1, column=0, padx=5, pady=5)
        self.member_id_entry = ttk.Entry(self.checkout_return_frame)
        self.member_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.checkout_return_frame, text="Checkout", command=self.checkout_book).grid(row=2, column=0, pady=10)
        ttk.Button(self.checkout_return_frame, text="Return", command=self.return_book).grid(row=2, column=1, pady=10)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        quantity = self.quantity_entry.get()
        if title and author and isbn and quantity:
            add_book(title, author, isbn, int(quantity))
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
            self.clear_add_book_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def add_member(self):
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()
        if name and email:
            add_member(name, email)
            messagebox.showinfo("Success", f"Member '{name}' added successfully.")
            self.clear_add_member_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def search_books(self):
        keyword = self.search_entry.get()
        results = search_books(keyword)
        self.search_results.delete(*self.search_results.get_children())
        for book in results:
            self.search_results.insert("", "end", values=book[1:])

    def checkout_book(self):
        book_id = self.book_id_entry.get()
        member_id = self.member_id_entry.get()
        if book_id and member_id:
            check_out_book(int(book_id), int(member_id))
            messagebox.showinfo("Success", "Book checked out successfully.")
            self.clear_checkout_return_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def return_book(self):
        book_id = self.book_id_entry.get()
        member_id = self.member_id_entry.get()
        if book_id and member_id:
            return_book(int(book_id), int(member_id))
            messagebox.showinfo("Success", "Book returned successfully.")
            self.clear_checkout_return_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def clear_add_book_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def clear_add_member_entries(self):
        self.member_name_entry.delete(0, tk.END)
        self.member_email_entry.delete(0, tk.END)

    def clear_checkout_return_entries(self):
        self.book_id_entry.delete(0, tk.END)
        self.member_id_entry.delete(0, tk.END)

root = tk.Tk()
app = LibraryManagementGUI(root)
root.mainloop()


    


        
