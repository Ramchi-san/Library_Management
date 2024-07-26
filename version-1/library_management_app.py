import tkinter as tk
from tkinter import ttk, messagebox

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
        self.notebook.add(self.search_books_frame, text="Search books")
        self.notebook.add(self.checkout_return_frame, text="Checkout/Return")

        self.create_add_book_widgets()
        self.create_add_member_widgets()
        self.create_search_books_widgets()
        self.create_checkout_return_widgets()

    def create_add_book_widgets(self):
        ttk.Label(self.add_book_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(self.add_book_frame)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_book_frame, text="Author: ").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(self.add_book_frame)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_book_frame, text="ISBN:").grid(row=2, column=0, padx=5, pady=5)
        self.isbn_entry = ttk.Entry(self.add_book_frame)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_book_frame, text="Quantity:").grid(row=3, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(self.add_book_frame)
        self.quantity_entry.grid(row=3, column=1, padx=5, pady=5)

        #Missing command
        ttk.Button(self.add_book_frame, text="Add Book").grid(row=4, column=0, columnspan=2, pady=10)

    def create_add_member_widgets(self):
        ttk.Label(self.add_member_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.member_name_entry = ttk.Entry(self.add_member_frame)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_member_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.member_email_entry = ttk.Entry(self.add_member_frame)
        self.member_email_entry.grid(row=1, column=1, padx=5, pady=5)

        #Missing command
        ttk.Button(self.add_member_frame, text="Add Member").grid(row=2, column=0, columnspan=2, pady=10)

    def create_search_books_widgets(self):
        ttk.Label(self.search_books_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(self.search_books_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        #Missing command
        ttk.Button(self.search_books_frame, text="Search").grid(row=1, column=0, columnspan=2, pady=10)

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

        #Missing commands        
        ttk.Button(self.checkout_return_frame, text="Checkout").grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(self.checkout_return_frame, text="Return").grid(row=3, column=0, columnspan=2, pady=10)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        quantity = self.quantity_entry.get()

        if title and author and isbn and quantity:
            #add_book(title, author, isbn, int(quantity))
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
            self.clear_add_book_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def add_member(self):
        member_name = self.member_name_entry.get()
        member_email = self.member_email_entry.get()
        
        if member_name and member_email:
            #add_member(member_name, member_email)
            messagebox.showinfo("Success", f"Member '{member_name}' added successfully.")
            self.clear_add_member_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    
    def search_books(self):
        keyword = self.search_entry.get()
        #results = search_books(keyword)
        self.search_results.delete(*self.search_results.get_children())
        for book in results:
            self.search_results.insert("", "end", values=book[1:])
    
    def checkout_book(self):
        book_id = self.book_id_entry.get()
        member_id = self.member_id_entry.get()
        if book_id and member_id:
            #check_out_book(int(book_id), int(member_id))
            messagebox.showinfo("Success", "Book checked out successfully.")
            self.clear_checkout_return_entries()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def return_book(self):
        book_id = self.book_id_entry.get()
        member_id = self.member_id_entry.get()
        if book_id and member_id:
            #return_book(int(book_id), int(member_id))
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

    
        

