#Homework No_1 : Book inventory system
#AUTHOR: Aleksandra Dmitruka, ad22069
#Created: 29.10.23
#Last update: 03.11.23

#TASK DESCRIPTION

# Data Structure:

# Inventory list is stored as a Python dictionary.
# To avoid re-entering data each time, the program can "encode" the initial list of books.
# For each book, at least the following information is stored: title, author, ISBN, price, and quantity in stock.
# Information for each book is stored in a separate dictionary.
# The keys of the inventory list dictionary are ISBN codes, and their values are dictionaries with book information.

# Functionality:

# Add a Book:
# Allow the user to add a new book to the list.
# When adding a book, ensure that its ISBN number is unique. If the ISBN is already in the list, display an error message.

# Search by ISBN:
# Allow users to search for a book by its ISBN number.
# If the book is found, display information about it.
# If the book is not found, display an error message.

# Search by Title or Author:
# Allow users to search for a book by entering a word in its title or author field.
# Display a list of books that match the search criteria.

# List of Books:
# Display a list of all books, showing the following information for each book: title, author, ISBN, quantity in stock.

# Delete a Book:
# Remove a book from the list using its ISBN number.
# Inform the user that the book was successfully deleted or that the ISBN was not found.



import customtkinter as ctk
from CTkTable import *
import sys


inventory = {
    "0123456789": {
        "title": "First Book",
        "author": "First Author",
        "ISBN": "0123456789",
        "price": 20.00,
        "quantity in stock": 10
    },
    "1234567890": {
        "title": "Second Book",
        "author": "Second Author",
        "ISBN": "1234567890",
        "price": 15.00,
        "quantity in stock": 5
    },
    "2345678901": {
        "title": "Third Book",
        "author": "Third Author",
        "ISBN": "2345678901",
        "price": 15.00,
        "quantity in stock": 5
    }
}



def is_valid_isbn(isbn):

    """
    def is_valid_isbn(isbn) - Checks if an ISBN (International Standard Book Number) is valid (both 10 and 13 digit one).

    Arguments:
        isbn (str): The ISBN string to be checked, may contain dashes.

    Returns:
        bool: True if the ISBN is valid, False otherwise.
    """

   
    cleaned_isbn = isbn.replace('-', '')
    #print(cleaned_isbn)


    if not cleaned_isbn.isdigit():
        return False
    
    if  cleaned_isbn=="":
        return False

    
    if len(cleaned_isbn) not in (10, 13):
        return False

    return True










def is_valid_data(title, author, price, quantity):

    """
    def is_valid_data(title,author,price,qunatity) - Checks if the input data for a book is valid and fits desired data type.

    Arguments:
        title (str): The title of the book.
        author (str): The author of the book.
        price (str): The price of the book. (Must be float and above 0)
        quantity (str): The quantity of the books in library. (Must be int and above or equal 0)

    Returns:
        bool: True if the input data is valid, False otherwise.
    """

    try:
        price_convert = float(price)
        quantity_convert = int(quantity)

      
        if title and author and price_convert != '' and quantity_convert!= '' and price_convert >0 and quantity_convert >= 0:
            return True
        else:
            return False
    except (ValueError, TypeError):
        return False

    





def show_error_messages(error_messages):

    """
    def show_error_messages(error_messages)- Displays a window with error messages and an 'OK' button to close it.

    Arguments:
        error_messages (list): A list of error messages to be displayed.

    Returns: -
    """

    error_window = ctk.CTk()
    error_window.geometry("800x200")
    error_window.title("Error")
    error_window.iconbitmap("error.ico")

    #Allows to show multiple errors in error window
    for message in error_messages:
        label = ctk.CTkLabel(error_window, text=message)
        label.pack()

    def soft_delete_error():

        """
        def soft_delete_error() - Special nested function for error window. Closes the error window, without calling any animation error in terminal. 
        It hides the error window and quits the event loop.

        """

        error_window.withdraw()
        error_window.quit()
    
    ok_button =ctk.CTkButton(error_window, text="OK", command=soft_delete_error)
    ok_button.pack(pady=20)
    error_window.mainloop()







def clean():
    """
    def clean () - Cleans up widgets in the 'show_window' by destroying unnecessary widgets. Used for table destruction before table regeneration. 
    The global variable widgets_to_preserve is defined at the end of the code

    """
    for widget in show_window.winfo_children():
     if widget not in widgets_to_preserve:
         widget.destroy()







def search():
    """
    def search() - Performs a search (by ISBN, author or title) operation by substring on the data and displays the results in the 'show_window' table. 
    If there is no results or if user enters the empty string, it displays an error message in show_window. 

    """
    selected_option=search_dropdown.get()
    search_string=entry_string.get()  
   
   
    #Recieves current table data as well as default(full) table itself
    new_table_data=regenrate_table()

    
    
    #Cleans the table, if we need to show specific result
    if selected_option != "Default":
        clean()
        updated_table_data = []
        updated_table_data.append(column_headings) 
       

        if search_string!='':  
            for row in new_table_data[1:]:
                if selected_option == "ISBN" and search_string in row[0]:
                    updated_table_data.append(row)
                elif selected_option == "Title" and search_string in str(row[1]).lower():
                    updated_table_data.append(row)
                elif selected_option == "Author" and search_string in str(row[2]).lower():
                     updated_table_data.append(row)

        if not updated_table_data[1:]:
            if search_string=='':
                 error_label = ctk.CTkLabel(show_window, text="The search string cannot be empty!")
                 
            elif selected_option == "ISBN":
                 error_label = ctk.CTkLabel(show_window, text="No books with the following ISBN or part of ISBN found! Also note that ISBN is a number!")
                 
            elif selected_option == "Title":
                 error_label = ctk.CTkLabel(show_window, text="No books with the following title or part of title found!")
                
            elif selected_option == "Author":
                 error_label = ctk.CTkLabel(show_window, text="No books with the following author or part of authors name found!")

            error_label.configure(font=("Arial", 20), pady=20)

            error_label.pack()
                 

           


        table = CTkTable(master=show_window, row=len(updated_table_data), column=4, values=updated_table_data)
        table.pack(expand=True, fill="both", padx=20, pady=20)








def regenrate_table():

    """
    def regenrate_table() - Regenerate the default table data and display it in the 'show_window'. 
    Used for updating table in case of add, delete or search operation.

    Returns: 
       list: list containing the regenerated table data. Used for searching up-to-date data


    """


    new_table_data=[]
   

    clean()


    column_headings = ["ISBN", "Title", "Author", "Quantity in Stock"]
    new_table_data.append(column_headings)
    
    for isbn, book_info in inventory.items():
        row = [isbn, book_info["title"], book_info["author"],  book_info["quantity in stock"]]
        new_table_data.append(row)
    

  
    table = CTkTable(master=show_window, row=len(new_table_data), column=4, values=new_table_data)

    table.pack(expand=True, fill="both", padx=20, pady=20)

    return new_table_data









def add():

    """
    def add() - Displays a window for adding a new book to the inventory.
    Provides input fields for the user to enter book information, performs data validation, and adds the book to the inventory if
    the input is valid and not in inventory already.
    """



 
    add_window=ctk.CTk()
    add_window.geometry("800x500")
    add_window.title("Add window")
    add_window.iconbitmap("book.ico")

    

  


    label = ctk.CTkLabel(add_window, text="Enter Book Information:")
    label.pack(pady=10)

    isbn_label = ctk.CTkLabel(add_window, text="ISBN:")
    isbn_label.pack()
    isbn_entry = ctk.CTkEntry(add_window)
    isbn_entry.pack()

    title_label = ctk.CTkLabel(add_window, text="Title:")
    title_label.pack()
    title_entry = ctk.CTkEntry(add_window)
    title_entry.pack()

    author_label = ctk.CTkLabel(add_window, text="Author:")
    author_label.pack()
    author_entry = ctk.CTkEntry(add_window)
    author_entry.pack()

    price_label = ctk.CTkLabel(add_window, text="Price:")
    price_label.pack()
    price_entry = ctk.CTkEntry(add_window)
    price_entry.pack()

    quantity_label = ctk.CTkLabel(add_window, text="Quantity in Stock:")
    quantity_label.pack()
    quantity_entry = ctk.CTkEntry(add_window)
    quantity_entry.pack()



    def soft_exit_add():

        """
        def soft_exit_add() - Close the add window without causing any errors or warnings in terminal, special nested function for add() function.
        It is called when the 'Close' button in the add window is clicked. It hides the add window
        and quits the event loop.
        """
              
        add_window.withdraw()
        add_window.quit()





    def add_button_clicked():
        """
        add_button_clicked() - Handles the 'Add Book' button click event, nested function for add() function.
        It collects user input, performs data validation, and adds the book to the inventory if the input is valid. If there are validation
        errors, it displays error messages by calling the 'show_error_messages' function.

        """
        isbn = isbn_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()
    
        error_messages = []  

        if isbn in inventory:
            error_messages.append("ISBN already exists in inventory!")
        if not is_valid_isbn(isbn):
            error_messages.append("ISBN should be valid and not empty!")
        if not is_valid_data(title, author, price, quantity):
            error_messages.append("You have entered wrong data! Please check that all fields aren't empty and that the price and quantity are numeric!")
    

                

        if error_messages:
           show_error_messages(error_messages)

        else:
            inventory[isbn] = {
            "title": title,
            "author": author,
            "ISBN": isbn,
            "price": float(price),
            "quantity in stock": int(quantity)
        }

            regenrate_table()
            soft_exit_add()
           



    add_button = ctk.CTkButton(add_window, text="Add Book", command=add_button_clicked)
    add_button.pack(pady=20)

    exit_button_add = ctk.CTkButton(add_window, text="Close", command=soft_exit_add, fg_color="dark red")
    exit_button_add.pack(pady=10)


   
    add_window.mainloop()









def delete():

    """
    def delete () -Displays a window for deleting a book from the inventory.

    It allows the user to enter an ISBN for the book to be deleted, performs validation, and if valid,
    deletes the book from the inventory and displays a success message. If there are errors, it displays error messages using the
    'show_error_messages' function.

    """

    delete_window = ctk.CTk()
    delete_window.geometry("800x440")
    delete_window.title("Delete book")
    delete_window.iconbitmap("book.ico")

    label_del = ctk.CTkLabel(delete_window, text="Enter an ISBN to delete")
    label_del.pack(pady=10)

    isbn_label_del = ctk.CTkLabel(delete_window, text="ISBN:")
    isbn_label_del.pack()
    isbn_entry_del = ctk.CTkEntry(delete_window)
    isbn_entry_del.pack()



    def soft_close_delete():
         """
        def soft_close_delete() - Close the delete window without causing any errors or warnings in terminal, special nested function for delete() function.
        It is called when the 'Close' button in the add window is clicked. It hides the add window
        and quits the event loop.

        """

         delete_window.withdraw()
         delete_window.quit()




    def delete_book():

        """
         def delete_book() - Handles the 'Delete Book' button click event.

        It collects the ISBN entered by the user, validates it, and deletes the book from the inventory if it is valid.
        It also displays a success message or error messages, depending on the result of the validation.

        """


        error_messages_del = []
        isbn = isbn_entry_del.get()



        if is_valid_isbn(isbn) and isbn in inventory:

         
            del inventory[isbn]
            regenrate_table()

            

            
            soft_close_delete()


            def soft_delete_success():
                """
                Closes the success window without causing any warinigs or errors in terminal.

                This function is called when the 'OK' button in the success window is clicked. It hides the success window
                and quits the event loop, effectively closing the window.
                """

                success_window.withdraw()
                success_window.quit()


            success_window = ctk.CTk()
            success_window.title("Success")
            success_window.geometry("400x150")
            success_window.iconbitmap("done.ico")

            success_message = f"The book with ISBN {isbn} was successfully deleted!"
            message_label = ctk.CTkLabel(success_window, text=success_message)
            message_label.pack(pady=20)
            ok_button = ctk.CTkButton(success_window, text="OK", command=soft_delete_success)
            ok_button.pack()
            success_window.mainloop()

        else:
             if isbn not in inventory:
                 error_messages_del.append("Non-existing ISBN")
             if not is_valid_isbn(isbn):
                 error_messages_del.append("The ISBN cannot be invalid or empty!")
                     
             show_error_messages(error_messages_del)


    delete_button = ctk.CTkButton(delete_window, text="Delete Book", command=delete_book)
    delete_button.pack(pady=20)
    delete_exit_button = ctk.CTkButton(delete_window, text="Close", command=soft_close_delete, fg_color="dark red")
    delete_exit_button.pack(pady=10)

    delete_window.mainloop()









ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("green")  



show_window = ctk.CTk()
show_window.geometry("1000x500")
show_window.title("Book inventory system")
show_window.iconbitmap("book.ico")

#A frame for all buttons and entry places in show_window. Allows to separate button placement from table placement 
button_frame = ctk.CTkFrame(show_window)
button_frame.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)
     





entry_label = ctk.CTkLabel(button_frame, text="String:")
entry_label.pack(side=ctk.LEFT, padx=10)



#The search string entry
entry_string = ctk.CTkEntry(button_frame)
entry_string.pack(side=ctk.LEFT, padx=10)




search_dropdown = ctk.CTkOptionMenu(button_frame, values=["Default","ISBN", "Author", "Title"])
search_dropdown.set("Default")
search_dropdown.pack(side=ctk.LEFT, padx=10)



search_button = ctk.CTkButton(button_frame, text="Search", command=search)
search_button.pack(side=ctk.LEFT, padx=10)




  


exit_button=ctk.CTkButton(button_frame, text="EXIT", command= sys.exit, fg_color="dark red", hover_color="dark blue",width=50 )
exit_button.pack(side=ctk.RIGHT, padx=10)

delete_button = ctk.CTkButton(button_frame, text="Delete", command=delete, fg_color="dark red", hover_color="red")
delete_button.pack(side=ctk.RIGHT, padx=15) 

add_button = ctk.CTkButton(button_frame, text="Add", command=add)
add_button.pack(side=ctk.RIGHT, padx=20)


#The list of widgets that won't be deleted/regenerated while regeneration table
widgets_to_preserve = [entry_label, entry_string, search_dropdown, search_button,button_frame]   


#First table creation
column_headings = ["ISBN", "Title", "Author", "Quantity in Stock"]
regenrate_table()


show_window.mainloop()



















