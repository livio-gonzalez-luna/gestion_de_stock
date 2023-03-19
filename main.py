import mysql.connector
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import Toplevel
import tkinter.simpledialog as sd
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from productEntryField import ProductEntryField


class MainWindow:
    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.root = tk.Tk()

        # Set the theme #
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Set the window size and title #
        self.root.geometry("1330x1200") 
        self.root.resizable(0, 0)
        self.root.title("Stock Management") 
        # self.createWidgets()

        # Connect to the database #
        self.connectToDatabase()

        # Create the menu bar #
        self.notebook = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Dashboard")
        self.notebook.add(self.tab2, text="Manage Products")
        self.notebook.pack(expand=1, fill="both")

        # Tab 1 #
        self.showCategoryPieChart()
        self.showAllProductsPieChart()

        # Tab 2 #
        self.productFrame = ttk.Frame(self.tab2)
        self.productFrame.pack(side = "right", fill = "both", expand = True)

        self.createProductTable()
        self.loadProducts()

        container = ttk.Frame(self.productFrame)
        container.pack(side = "left", fill = "y", padx = 10, pady = 10)

        addProductLabel = ttk.Label(container, text = "Add/Update a product")
        addProductLabel.pack(pady=2)

        idField = ProductEntryField(container, "ID", 40)
        idField.pack(pady=5, side="top", anchor="center")

        nameField = ProductEntryField(container, "Name", 40)
        nameField.pack(pady=5, side="top", anchor="center")

        descriptionField = ProductEntryField(container, "Description", 40)
        descriptionField.pack(pady=5, side="top", anchor="center")

        priceField = ProductEntryField(container, "Price", 40)
        priceField.pack(pady=5, side="top", anchor="center")

        quantityField = ProductEntryField(container, "Quantity", 40)
        quantityField.pack(pady=5, side="top", anchor="center")

        idCategoryField = ProductEntryField(container, "ID Category", 40)
        idCategoryField.pack(pady=5, side="top", anchor="center")

        addButton = ttk.Button(container, text = "Add", command = lambda: self.addProduct(idField.get(), nameField.get(), descriptionField.get(), priceField.get(), idCategoryField.get()))
        addButton.config(width = 20)
        addButton.pack(pady = 15, side="top", anchor="center")

        updateButton = ttk.Button(container, text = "Update", command = lambda: self.updateProduct(idField.get(), nameField.get(), descriptionField.get(), priceField.get(), idCategoryField.get()))
        updateButton.config(width = 20)
        updateButton.pack(pady = 15, side="top", anchor="center")

        deleteLabel = ttk.Label(container, text = "Delete a product")
        deleteLabel.pack(pady=2, side="top", anchor="center")

        deleteButton = ttk.Button(container, text = "Delete", command = self.deleteProduct)
        deleteButton.config(width = 20)
        deleteButton.pack(pady = 15, side="top", anchor="center")

        searchLabel = ttk.Label(container, text = "Search products by category")
        searchLabel.pack(pady=2, side="top", anchor="center")
        
        searchEntry = ttk.Entry(container)
        searchEntry.pack(pady=5, side="top", anchor="center")

        searchButton = ttk.Button(container, text = "Search", command = lambda: self.searchProducts(searchEntry.get()))
        searchButton.config(width = 20)
        searchButton.pack(pady = 15, side="top", anchor="center")

        refreshButton = ttk.Button(container, text = "Refresh", command = self.refreshProducts)
        refreshButton.config(width = 20)
        refreshButton.pack(pady = 15, side="top", anchor="center")

        importCSVButton = ttk.Button(container, text = "Import CSV", command = self.importCSV)
        importCSVButton.config(width = 20)
        importCSVButton.pack(pady = 15, side="top", anchor="center")

    def run(self):
        self.root.mainloop()

    # def createWidgets(self):


    def connectToDatabase(self):
        host = sd.askstring("Host", "Enter the host")
        user = sd.askstring("User", "Enter the user")
        password = sd.askstring("Password", "Enter the password")
        database = sd.askstring("Database", "Enter the database")

        try:
            self.cnx = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.cnx.cursor()
            messagebox.showinfo("Success", "Connected to database")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", "Failed to connect to database")

    def createProductTable(self):
        columns = ("ID", "Name", "Description", "Price", "Quantity", "Category")
        self.tree = ttk.Treeview(self.tab2, columns=columns, show="headings", selectmode="browse")

        self.tree.column("ID", width=150, anchor="center")
        self.tree.column("Name", width=200, anchor="center")
        self.tree.column("Description", width=200, anchor="center")
        self.tree.column("Price", width=150, anchor="center")
        self.tree.column("Quantity", width=200, anchor="center")
        self.tree.column("Category", width=150, anchor="center")

        self.tree.configure(height = 30)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.tag_configure('myTag', font = ('Arial', 30, 'bold'))

        self.tree.pack(side = "left", fill="both", expand=True)

    def loadProducts(self):
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def addProduct(self, idProduct, name, description, price, idCategory):
        if not idProduct or not name or not description or not price or not idCategory:
            messagebox.showerror("Error", "Please fill all the fields")
            return
        sql = "INSERT INTO products (id, name, description, price, idCategory) VALUES (%s, %s, %s, %s, %s)"
        val = (idProduct, name, description, price, idCategory)
        self.cursor.execute(sql, val)
        self.cnx.commit()
        self.tree.delete(*self.tree.get_children())
        self.loadProducts()
        messagebox.showinfo("Success", "Product added successfully")

    def deleteProduct(self):
        if not self.tree.selection():
            messagebox.showerror("Error", "Click on a product to select it")
            return
        sql = "DELETE FROM products WHERE id = %s"
        val = (self.tree.item(self.tree.selection())['values'][0],)
        self.cursor.execute(sql, val)
        self.cnx.commit()
        self.tree.delete(*self.tree.get_children())
        self.loadProducts()
        messagebox.showinfo("Success", "Product deleted successfully")

    def updateProduct(self, idProduct, name, description, price, idCategory):
        if not idProduct or not name or not description or not price or not idCategory:
            messagebox.showerror("Error", "Please fill all the fields")
            return
        sql = "UPDATE products SET name = %s, description = %s, price = %s, idCategory = %s WHERE id = %s"
        val = (name, description, price, idCategory, idProduct)
        self.cursor.execute(sql, val)
        self.cnx.commit()
        self.tree.delete(*self.tree.get_children())
        self.loadProducts()
        messagebox.showinfo("Success", "Product updated successfully")

    def searchProducts(self, idCategory):
        if not idCategory:
            messagebox.showerror("Error", "Please fill the field")
            return
        sql = "SELECT * FROM products WHERE idCategory = %s"
        val = (idCategory,)
        self.cursor.execute(sql, val)
        rows = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def refreshProducts(self):
        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)

    def importCSV(self):
        with open('products.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Description", "Price", "Quantity", "Category"])
            self.cursor.execute("SELECT * FROM products")
            rows = self.cursor.fetchall()
            for row in rows:
                writer.writerow(row)
        messagebox.showinfo("Success", "Products exported successfully")


    def showCategoryPieChart(self):
        self.cursor.execute("SELECT categories.name, SUM(products.quantity) FROM products INNER JOIN categories ON products.idCategory = categories.id WHERE quantity > 0 GROUP BY categories.id")
        rows = self.cursor.fetchall()
        labels = [row[0] for row in rows]
        sizes = [row[1] for row in rows]
        
        fig1, ax1 = plt.subplots(figsize=(6.75, 6.75))
        
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        canvas = FigureCanvasTkAgg(fig1, master=self.tab1)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True)

    def showAllProductsPieChart(self):
        self.cursor.execute("SELECT name, quantity FROM products WHERE quantity > 0")
        rows = self.cursor.fetchall()
        labels = [row[0] for row in rows]
        sizes = [row[1] for row in rows]

        fig2, ax2 = plt.subplots(figsize=(6.75, 6.75))

        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax2.axis('equal')
        canvas = FigureCanvasTkAgg(fig2, master=self.tab1)
        canvas.draw()
        canvas.get_tk_widget().pack(side="right", fill="both", expand=True)
        

if __name__ == '__main__':
    window = MainWindow()
    window.run()