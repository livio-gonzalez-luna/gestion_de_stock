import mysql.connector
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox



class Product:
    def __init__(self, idProduct, name, description, price, idCategory):
        self.idProduct = idProduct
        self.name = name
        self.description = description
        self.price = price
        self.idCategory = idCategory

    def createProductUI(self):
        columns = ("ID", "Name", "Description", "Price", "idCategory")
        self.tree = ttk.Treeview(self.tab2, columns=columns, show="headings")
        
        for column in columns:
            self.tree.heading(column, text=column)

        for product in self.products:
            values = (product.idProduct, product.name, product.description, product.price, product.idCategory)
            self.tree.insert("", "end", values=values)

        self.tree.pack(fill = "both", expand = True)


