from tkinter import *
import mysql.connector as my
from tkinter import simpledialog
from tkinter import messagebox
import tkinter as tk

def login_window():
    login_window = Tk()
    login_window.title('Login')
    login_window.geometry('300x150')
    login_window.minsize(300, 150)
    login_window.configure(bg='#f1f1f1')

    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        # Perform your login authentication here
        # Replace the condition with your actual login check
        if username == 'yassinehafsa' and password == 'zakaria':
            login_window.destroy()
            access_database()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    username_label = Label(login_window, text="Username:", font=("Arial", 12), bg='#f1f1f1')
    username_label.pack()

    username_entry = Entry(login_window, font=("Arial", 12))
    username_entry.pack()

    password_label = Label(login_window, text="Password:", font=("Arial", 12), bg='#f1f1f1')
    password_label.pack()

    password_entry = Entry(login_window, show="*", font=("Arial", 12))
    password_entry.pack()

    login_button = Button(login_window, text="Login", command=check_login, font=("Arial", 12))
    login_button.pack(pady=10)

    login_window.mainloop()

def access_database():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('600x600')
            select_window.minsize(400, 400)
            select_window.configure(bg='silver')

             # Table selection variable
            selected_table = StringVar()
            
            def update_table_dropdown():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall() #permet d'affiher tous les tables 
                    table_list = [table[0] for table in tables]
                    select_dropdown['menu'].delete(0, 'end')
                    for table in table_list:
                        select_dropdown['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Erreur lors de la récupération de la liste des tables : {e}")
                finally:
                    cursor.close()

            def display_table_contents(): #permet d'afficher tous qu'il est dans table
                table_name = selected_table.get()
                if table_name:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        table_data = ""
                        for row in rows:
                            table_data += str(row) + "\n"
                            table_text.delete("1.0", END)
                            table_text.insert(END, table_data)
                    except my.errors.ProgrammingError as e:
                        print(f"Erreur lors de la récupération des données de la table {table_name} : {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                select_window.destroy()
            
            def add_new_table():
                table_name = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_name:
                    column_data = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_data:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_name} ({column_data})")
                            con.commit()
                            print(f"New table '{table_name}' created successfully.")
                            update_table_dropdown()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")
                        finally:
                            cursor.close()

            def add_new_column():
                    table_name = selected_table.get()
                    if table_name:
                        column_name = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                        if column_name:
                            cursor = con.cursor()
                            try:
                                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(255)")
                                con.commit()
                                print(f"New column '{column_name}' added to table '{table_name}' successfully.")
                            except my.errors.ProgrammingError as e:
                                print(f"Error adding new column: {e}")
                            finally:
                                cursor.close()

            def delete_column():
                table_name = selected_table.get()
                if table_name:
                    column_name = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_name:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
                            con.commit()
                            print(f"Column '{column_name}' deleted from table '{table_name}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_name():
                table_name = selected_table.get()
                if table_name:
                    old_column_name = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_name = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_name and new_column_name:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_name}' changed to '{new_column_name}' successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")

            def delete_table():
                   table_name = selected_table.get()
                   if table_name:
                       confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_name}'?")
                       if confirm:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_name}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_name}' deleted successfully.")
                               update_table_dropdown()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()


            def insertion_valeur():
                # Récupérer les valeurs saisies dans les Entry
                valeurs = [entry.get() for entry in entries]

                try:
                    # Connexion à la base de données
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestionstock'
                    )
                    cursor = con.cursor()

                    # Exécution de la requête d'insertion
                    nom_table = entry_table.get()  # Récupérer le nom de la table depuis le widget Entry
                    colonne1 = "nom_colonne1"  # Remplacer par le nom réel de la première colonne
                    colonne2 = "nom_colonne2"  # Remplacer par le nom réel de la deuxième colonne
                    requete = f"INSERT INTO {nom_table} ({colonne1}, {colonne2}) VALUES (%s, %s)"
                    cursor.execute(requete, tuple(valeurs))
                    con.commit()

                    print("L'enregistrement a été ajouté avec succès.")

                except my.Error as e:
                    print("Erreur lors de l'ajout de l'enregistrement :", e)

                finally:
                    # Fermeture de la connexion à la base de données
                    if con.is_connected():
                        cursor.close()
                        con.close()

            # Créer une fenêtre Tkinter
            fenetre = tk.Tk()

            # Demander à l'utilisateur de saisir le nom de la table
            label_table = tk.Label(fenetre, text="Nom de la table :")
            label_table.pack()
            entry_table = tk.Entry(fenetre)
            entry_table.pack()

            # Créer des Entry pour saisir les valeurs
            entries = []
            for i in range(2):  # Remplacer par le compte approprié
                label = tk.Label(fenetre, text=f"Valeur {i+1} :")
                label.pack()
                entry = tk.Entry(fenetre)
                entry.pack()
                entries.append(entry)

   
            # Table selection label
            select_label = Label(select_window, text="Select Table:", font=("Arial", 12), bg='#f1f1f1')
            select_label.pack()

            # Table selection dropdown
            select_dropdown = OptionMenu(select_window, selected_table, "Articles", "categ_article", "transaction", "commande", "transporteur","eliot","Details_com", "emplacement", "fournisseur", "expeditions", "livraison", "details_liv", "client", "historique", "roles", "utilisateur", "Alerte Stock", "parametres_Stck")
            select_dropdown.pack()
            select_dropdown.configure(background='DarkTurquoise')

            # Display Table button
            display_button = Button(select_window, text="Display Table", command=display_table_contents, font=("Arial", 12))
            display_button.pack(pady=4)
            display_button.configure(background='DarkTurquoise')

            # Bouton pour mettre à jour la liste des tables
            update_button = tk.Button(select_window, text="Mettre à jour", command=update_table_dropdown, font=("Arial", 12))
            update_button.pack(pady=4)
            update_button.configure(background='CornflowerBlue')

            # Bouton pour afficher le contenu de la table sélectionnée
            display_button = tk.Button(select_window, text="Afficher le contenu", command=display_table_contents, font=("Arial", 12))
            display_button.pack(pady=4)
            display_button.configure(background='CornflowerBlue')

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_button = Button(select_window, text="Return to Menu", command=return_to_menu, font=("Arial", 12))
            return_button.pack(pady=4)
            return_button.configure(background='CornflowerBlue')

            #ajouter une nouvelle table
            add_table_button = tk.Button(select_window, text="Add New Table", command=add_new_table, font=("Arial", 12))
            add_table_button.pack(pady=4)
            add_table_button.configure(background='DarkTurquoise')

            #ajouter une nouvelle colonne
            add_column_button = tk.Button(select_window, text="Add New Column", command=add_new_column, font=("Arial", 12))
            add_column_button.pack(pady=4)
            add_column_button.configure(background='DarkTurquoise')
            
            #supprimer une colonne
            delete_column_button = tk.Button(select_window, text="Delete Column", command=delete_column, font=("Arial", 12))
            delete_column_button.pack(pady=4)
            delete_column_button.configure(background='DarkTurquoise')

            #changer le nom d'une colonne
            change_name_button = tk.Button(select_window, text="Change Column Name", command=change_column_name, font=("Arial", 12))
            change_name_button.pack(pady=4)
            change_name_button.configure(background='DarkTurquoise')

            #supprimer une table
            delete_table_button = Button(select_window, text="Delete Table", command=delete_table, font=("Arial", 12))
            delete_table_button.pack(pady=4)
            delete_table_button.configure(background='DarkTurquoise')

            bouton_ajouter = tk.Button(fenetre, text="Insérer", command=insertion_valeur)
            bouton_ajouter.pack()


        def change_table_name():
            current_table_name = table_label.cget("text")  # Get the current table name from the label
            new_table_name = new_table_entry.get()  # Get the new table name from an Entry widget or any other source
            
            # Update the table name in the Tkinter interface
            table_label.config(text=new_table_name)
            
            try:
                # Connect to the database
                con = my.connect(
                    user='root',
                    passwd='',
                    host='localhost',
                    port=3306,
                    database='gestionstock'
                )
                cursor = con.cursor()
                
                # Execute the SQL query to rename the table
                rename_query = f"ALTER TABLE `{current_table_name}` RENAME TO `{new_table_name}`"
                cursor.execute(rename_query)
                con.commit()
                
                print("Table name changed successfully.")
            
            except my.Error as e:
                print("Error while changing table name:", e)
            
            finally:
                # Close the database connection
                if con.is_connected():
                    cursor.close()
                    con.close()

        # Create a Tkinter window
        select_window = tk.Tk()

        # Create a label for the current table name
        table_label = tk.Label(select_window, text="Nom de la table :")
        table_label.pack()

        # Create an Entry widget to input the new table name
        new_table_entry = tk.Entry(select_window)
        new_table_entry.pack()

        # Create a button to trigger the table name change
        change_button = tk.Button(select_window, text="Changer le nom", command=change_table_name)
        change_button.pack()
        
        # Start the Tkinter event loop
        select_window.mainloop()

    except my.errors as e:
        print(e)


#pour produit
def accessDATABASE1():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('600x600')
            select_window.minsize(400, 400)
            select_window.configure(bg='silver')
            # Table selection variable
            selected_table = StringVar()
            
            def update_table_dropdownpro():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    table_list = [table[0] for table in tables]
                    select_dropdownpro['menu'].delete(0, 'end')
                    for table in table_list:
                        select_dropdownpro['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Erreur lors de la récupération de la liste des tables : {e}")
                finally:
                    cursor.close()

            def display_table_contentspro():
                table_name = selected_table.get()
                if table_name:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        table_data = ""
                        for row in rows:
                            table_data += str(row) + "\n"
                            table_text.delete("1.0", END)
                            table_text.insert(END, table_data)
                    except my.errors.ProgrammingError as e:
                        print(f"Error retrieving data from table {table_name}: {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                select_window.destroy()

            
            def add_new_tablepro():
                table_namepro = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_namepro:
                    column_data1 = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_data1:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_namepro} ({column_data1})")
                            con.commit()
                            print(f"New table '{table_namepro}' created successfully.")
                            update_table_dropdownpro()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")
                        finally:
                            cursor.close()

            def add_new_columnpro():
                table_namepro = selected_table.get()
                if table_namepro:
                    column_namepro = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                    if column_namepro:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namepro} ADD COLUMN {column_namepro} VARCHAR(255)")
                            con.commit()
                            print(f"New column '{column_namepro}' added to table '{table_namepro}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error adding new column: {e}")
                        finally:
                            cursor.close()

            def delete_columnpro():
                table_namepro = selected_table.get()
                if table_namepro:
                    column_namepro = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_namepro:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namepro} DROP COLUMN {column_namepro}")
                            con.commit()
                            print(f"Column '{column_namepro}' deleted from table '{table_namepro}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_namepro():
                table_namepro = selected_table.get()
                if table_namepro:
                    old_column_namepro = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_namepro = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_namepro and new_column_namepro:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namepro} RENAME COLUMN {old_column_namepro} TO {new_column_namepro}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_namepro}' changed to '{new_column_namepro}' successfully.")
                        except my.errors.ProgrammingError as e:
                             messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")

            def delete_tablepro():
                   table_namepro = selected_table.get()
                   if table_namepro:
                       confirmpro = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_namepro}'?")
                       if confirmpro:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_namepro}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_namepro}' deleted successfully.")
                               update_table_dropdownpro()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()

            def insert_valuespro():
                table_namepro = selected_table.get()
                if table_namepro:
                    valuespro = simpledialog.askstring("Insert Values", "Enter comma-separated values:")
                    if valuespro:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"INSERT INTO {table_namepro} VALUES ({valuespro})")
                            con.commit()
                            messagebox.showinfo("Insert Values", "Values inserted successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error inserting values: {e}")
                        finally:
                            cursor.close()

                 # Table selection label
            select_labelpro = Label(select_window, text="Select Table produit:", font=("Arial", 12), bg='#f1f1f1')
            select_labelpro.pack()

             # Table selection dropdown
            select_dropdownpro = OptionMenu(select_window, selected_table, "produit")
            select_dropdownpro.pack()
            select_dropdownpro.configure(background='DarkTurquoise')

            display_button1 = Button(select_window, text="Display Tablepro", command=display_table_contentspro, font=("Arial", 12))
            display_button1.pack(pady=10)

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_button1 = Button(select_window, text="Return to Menupro", command=return_to_menu, font=("Arial", 12))
            return_button1.pack(pady=10)
            
            update_button = tk.Button(select_window, text="Mettre à jourpro", command=update_table_dropdownpro, font=("Arial", 12))
            update_button.pack(pady=4)

            add_table_buttonpro = Button(select_window, text="Add New Tablepro", command=add_new_tablepro, font=("Arial", 12))
            add_table_buttonpro.pack(pady=5)

            add_column_buttonpro = Button(select_window, text="Add New Columnpro", command=add_new_columnpro, font=("Arial", 12))
            add_column_buttonpro.pack(pady=5)

            delete_column_buttonpro = Button(select_window, text="Delete Columnpro", command=delete_columnpro, font=("Arial", 12))
            delete_column_buttonpro.pack(pady=5)

            change_name_buttonpro = Button(select_window, text="Change Column Namepro", command=change_column_namepro, font=("Arial", 12))
            change_name_buttonpro.pack(pady=5)

            delete_table_buttonpro = Button(select_window, text="Delete Table", command=delete_tablepro, font=("Arial", 12))
            delete_table_buttonpro.pack(pady=5)

            insert_values_buttonpro = Button(select_window, text="Insert Values", command=insert_valuespro, font=("Arial", 12))
            insert_values_buttonpro.pack(pady=5)
        
            def change_table_namepro():
                current_table_namepro = table_labelpro.cget("text")  # Get the current table name from the label
                new_table_namepro = new_table_entrypro.get()  # Get the new table name from an Entry widget or any other source
                
                # Update the table name in the Tkinter interface
                table_labelpro.config(text=new_table_namepro)
                
                try:
                    # Connect to the database
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestionstock'
                    )
                    cursor = con.cursor()
                    
                    # Execute the SQL query to rename the table
                    rename_query = f"ALTER TABLE `{current_table_namepro}` RENAME TO `{new_table_namepro}`"
                    cursor.execute(rename_query)
                    con.commit()
                    
                    print("Table name changed successfully.")
                
                except my.Error as e:
                    print("Error while changing table name:", e)
                
                finally:
                    # Close the database connection
                    if con.is_connected():
                        cursor.close()
                        con.close()
            
        select_window = tk.Tk()

        # Create a label for the current table name
        table_labelpro = tk.Label(select_window, text="Nom de la table :")
        table_labelpro.pack()

        # Create an Entry widget to input the new table name
        new_table_entrypro = tk.Entry(select_window)
        new_table_entrypro.pack()

        # Create a button to trigger the table name change
        change_buttonpro = tk.Button(select_window, text="Changer le nompro", command=change_table_namepro)
        change_buttonpro.pack()

        

        select_window.mainloop()

    except my.errors as e:
        print(e)

def accessDATABASE2():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('600x600')
            select_window.minsize(400, 400)
            select_window.configure(bg='silver')
            # Table selection variable
            selected_table = StringVar()
            
            def update_table_dropdowncom():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    table_list = [table[0] for table in tables]
                    select_dropdowncom['menu'].delete(0, 'end')
                    for table in table_list:
                        select_dropdowncom['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Erreur lors de la récupération de la liste des tables : {e}")
                finally:
                    cursor.close()

            def display_table_contentscom():
                table_namecom = selected_table.get()
                if table_namecom:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_namecom}")
                        rows = cursor.fetchall()
                        table_data = ""
                        for row in rows:
                            table_data += str(row) + "\n"
                            table_text.delete("1.0", END)
                            table_text.insert(END, table_data)
                    except my.errors.ProgrammingError as e:
                        print(f"Error retrieving data from table {table_namecom}: {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                select_window.destroy()

            def add_new_tablecom():
                table_namecom = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_namecom:
                    column_data2 = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_data2:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_namecom} ({column_data2})")
                            con.commit()
                            print(f"New table '{table_namecom}' created successfully.")
                            update_table_dropdowncom()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")

            def add_new_columncom():
                table_namecom = selected_table.get()
                if table_namecom:
                    column_namecom = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                    if column_namecom:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecom} ADD COLUMN {column_namecom} VARCHAR(255)")
                            con.commit()
                            print(f"New column '{column_namecom}' added to table '{table_namecom}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error adding new column: {e}")
                        finally:
                            cursor.close()

            def delete_columncom():
                table_namecom = selected_table.get()
                if table_namecom:
                    column_namecom = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_namecom:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecom} DROP COLUMN {column_namecom}")
                            con.commit()
                            print(f"Column '{column_namecom}' deleted from table '{table_namecom}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_namecom():
                table_namecom = selected_table.get()
                if table_namecom:
                    old_column_namecom = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_namecom = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_namecom and new_column_namecom:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecom} RENAME COLUMN {old_column_namecom} TO {new_column_namecom}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_namecom}' changed to '{new_column_namecom}' successfully.")
                        except my.errors.ProgrammingError as e:
                             messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")

            def delete_tablecom():
                   table_namecom = selected_table.get()
                   if table_namecom:
                       confirmcom = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_namecom}'?")
                       if confirmcom:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_namecom}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_namecom}' deleted successfully.")
                               update_table_dropdowncom()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()

            def insert_valuescom():
                table_namecom = selected_table.get()
                if table_namecom:
                    valuescom = simpledialog.askstring("Insert Values", "Enter comma-separated values:")
                    if valuescom:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"INSERT INTO {table_namecom} VALUES ({valuescom})")
                            con.commit()
                            messagebox.showinfo("Insert Values", "Values inserted successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error inserting values: {e}")
                        finally:
                            cursor.close()

                # Table selection label
            select_labelcom = Label(select_window, text="Select Table commande:", font=("Arial", 12), bg='#f1f1f1')
            select_labelcom.pack()

            select_dropdowncom = OptionMenu(select_window, selected_table, "commande")
            select_dropdowncom.pack()
            select_dropdowncom.configure(background='DarkTurquoise')

            display_button2 = Button(select_window, text="Display Tablecom", command=display_table_contentscom, font=("Arial", 12))
            display_button2.pack(pady=10)

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_button2 = Button(select_window, text="Return to Menucom", command=return_to_menu, font=("Arial", 12))
            return_button2.pack(pady=10)

            update_button = tk.Button(select_window, text="Mettre à jourcom", command=update_table_dropdowncom, font=("Arial", 12))
            update_button.pack(pady=4)

            add_table_buttoncom = Button(select_window, text="Add New Tablecom", command=add_new_tablecom, font=("Arial", 12))
            add_table_buttoncom.pack(pady=5)

            add_column_buttoncom = Button(select_window, text="Add New Columncom", command=add_new_columncom, font=("Arial", 12))
            add_column_buttoncom.pack(pady=5)

            delete_column_buttoncom = Button(select_window, text="Delete Columncom", command=delete_columncom, font=("Arial", 12))
            delete_column_buttoncom.pack(pady=5)

            change_name_buttoncom = Button(select_window, text="Change Column Namecom", command=change_column_namecom, font=("Arial", 12))
            change_name_buttoncom.pack(pady=5)

            delete_table_buttoncom = Button(select_window, text="Delete Tablecom", command=delete_tablecom, font=("Arial", 12))
            delete_table_buttoncom.pack(pady=5)

            insert_values_buttoncom = Button(select_window, text="Insert Values", command=insert_valuescom, font=("Arial", 12))
            insert_values_buttoncom.pack(pady=5)
           
            def change_table_namecom():
                current_table_namecom = table_labelcom.cget("text")  # Get the current table name from the label
                new_table_namecom = new_table_entrycom.get()  # Get the new table name from an Entry widget or any other source
                
                # Update the table name in the Tkinter interface
                table_labelcom.config(text=new_table_namecom)
                
                try:
                    # Connect to the database
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestionstock'
                    )
                    cursor = con.cursor()
                    
                    # Execute the SQL query to rename the table
                    rename_query = f"ALTER TABLE `{current_table_namecom}` RENAME TO `{new_table_namecom}`"
                    cursor.execute(rename_query)
                    con.commit()
                    
                    print("Table name changed successfully.")
                
                except my.Error as e:
                    print("Error while changing table name:", e)
                
                finally:
                    # Close the database connection
                    if con.is_connected():
                        cursor.close()
                        con.close()
            
        select_window = tk.Tk()
        
        # Create a label for the current table name
        table_labelcom = tk.Label(select_window, text="Nom de la table :")
        table_labelcom.pack()

        # Create an Entry widget to input the new table name
        new_table_entrycom = tk.Entry(select_window)
        new_table_entrycom.pack()

        # Create a button to trigger the table name change
        change_buttoncom = tk.Button(select_window, text="Changer le nompro", command=change_table_namecom)
        change_buttoncom.pack()

        select_window.mainloop()
   
    except my.errors as e:
        print(e)

def accessDATABASE3():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('600x600')
            select_window.minsize(400, 400)
            select_window.configure(bg='silver')

             # Table selection variable
            selected_table = StringVar()
            
            def update_table_dropdowncl():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall() #permet d'affiher tous les tables 
                    table_list = [table[0] for table in tables]
                    select_dropdowncl['menu'].delete(0, 'end')
                    for table in table_list:
                        select_dropdowncl['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Erreur lors de la récupération de la liste des tables : {e}")
                finally:
                    cursor.close()
                 
            # Function to display table contents
            def display_table_contentscl():
                table_namecl = selected_table.get()
                if table_namecl:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_namecl}")
                        rows = cursor.fetchall()
                        table_data = ""
                        for row in rows:
                            table_data += str(row) + "\n"
                            table_text.delete("1.0", END)
                            table_text.insert(END, table_data)
                    except my.errors.ProgrammingError as e:
                        print(f"Error retrieving data from table {table_namecl}: {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                select_window.destroy()

            def add_new_tablecl():
                table_namecl = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_namecl:
                    column_data3 = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_data3:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_namecl} ({column_data3})")
                            con.commit()
                            print(f"New table '{table_namecl}' created successfully.")
                            update_table_dropdowncl()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")
                        finally:
                            cursor.close()

            def add_new_columncl():
                table_namecl = selected_table.get() #récypérer la valeur d'un widget
                if table_namecl:
                    #simpledialog.askstring:permet de créerune boite pour saisir une chaine de caractére
                    column_namecl = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                    if column_namecl:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecl} ADD COLUMN {column_namecl} VARCHAR(255)")
                            con.commit()
                            print(f"New column '{column_namecl}' added to table '{table_namecl}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error adding new column: {e}")
                        finally:
                            cursor.close()

            def delete_columncl():
                table_namecl = selected_table.get()
                if table_namecl:
                    column_namecl = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_namecl:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecl} DROP COLUMN {column_namecl}")
                            con.commit()
                            print(f"Column '{column_namecl}' deleted from table '{table_namecl}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_namecl():
                table_namecl = selected_table.get()
                if table_namecl:
                    old_column_namecl = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_namecl = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_namecl and new_column_namecl:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecl} RENAME COLUMN {old_column_namecl} TO {new_column_namecl}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_namecl}' changed to '{new_column_namecl}' successfully.")
                        except my.errors.ProgrammingError as e:
                             messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")


            def delete_tablecl():
                   table_namecl = selected_table.get()
                   if table_namecl:
                        #permet de creer une boite pour confirmer si oui ou non
                       confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_namecl}'?")
                       if confirm:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_namecl}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_namecl}' deleted successfully.")
                               update_table_dropdowncl()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()

            def insert_valuescl():
                table_namecl = selected_table.get()
                if table_namecl:
                    values = simpledialog.askstring("Insert Values", "Enter comma-separated values:")
                    if values:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"INSERT INTO {table_namecl} VALUES ({values})")
                            con.commit()
                            messagebox.showinfo("Insert Values", "Values inserted successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error inserting values: {e}")
                        finally:
                            cursor.close()

            # Table selection label
            select_label = Label(select_window, text="Select Table client:", font=("Arial", 12), bg='#f1f1f1')
            select_label.pack()

            # Table selection dropdown
            select_dropdowncl = OptionMenu(select_window, selected_table, "client")
            select_dropdowncl.pack()
            select_dropdowncl.configure(background='DarkTurquoise')
            
            display_button1 = Button(select_window, text="Display Table", command=display_table_contentscl, font=("Arial", 12))
            display_button1.pack(pady=4)
            display_button1.configure(background='DarkTurquoise')

            # Bouton pour mettre à jour la liste des tables
            update_button1 = tk.Button(select_window, text="Mettre à jour", command=update_table_dropdowncl, font=("Arial", 12))
            update_button1.pack(pady=4)
            update_button1.configure(background='CornflowerBlue')

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_button = Button(select_window, text="Return to Menu", command=return_to_menu, font=("Arial", 12))
            return_button.pack(pady=5)

            add_table_button1 = Button(select_window, text="Add New Tablecl", command=add_new_tablecl, font=("Arial", 12))
            add_table_button1.pack(pady=5)

            add_column_buttoncl = Button(select_window, text="Add New Columncl", command=add_new_columncl, font=("Arial", 12))
            add_column_buttoncl.pack(pady=5)

            delete_column_buttoncl = Button(select_window, text="Delete Columncl", command=delete_columncl, font=("Arial", 12))
            delete_column_buttoncl.pack(pady=5)

            change_name_buttoncl = Button(select_window, text="Change Column Namecl", command=change_column_namecl, font=("Arial", 12))
            change_name_buttoncl.pack(pady=5)

            delete_table_buttoncl = Button(select_window, text="Delete Tablecl", command=delete_tablecl, font=("Arial", 12))
            delete_table_buttoncl.pack(pady=5)

            insert_values_buttoncl = Button(select_window, text="Insert Valuescl", command=insert_valuescl, font=("Arial", 12))
            insert_values_buttoncl.pack(pady=5)

            def change_table_namecl():
                current_table_namecl = table_labelcl.cget("text")  # Get the current table name from the label
                new_table_namecl = new_table_entrycl.get()  # Get the new table name from an Entry widget or any other source
            
                # Update the table name in the Tkinter interface
                table_labelcl.config(text=new_table_namecl)
                
                try:
                    # Connect to the database
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestionstock'
                    )
                    cursor = con.cursor()
                    
                    # Execute the SQL query to rename the table
                    rename_query = f"ALTER TABLE `{current_table_namecl}` RENAME TO `{new_table_namecl}`"
                    cursor.execute(rename_query)
                    con.commit()
                    
                    print("Table name changed successfully.")
                
                except my.Error as e:
                    print("Error while changing table name:", e)
                
                finally:
                    # Close the database connection
                    if con.is_connected():
                        cursor.close()
                        con.close()

            # Create a Tkinter window
        select_window = tk.Tk()

        # Create a label for the current table name
        table_labelcl = tk.Label(select_window, text="Nom de la table :")
        table_labelcl.pack()

        # Create an Entry widget to input the new table name
        new_table_entrycl = tk.Entry(select_window)
        new_table_entrycl.pack()

        # Create a button to trigger the table name change
        change_buttoncl = tk.Button(select_window, text="Changer le nom", command=change_table_namecl)
        change_buttoncl.pack()

        select_window.mainloop()

    
    except my.errors as e:
        print(e)


#pour fournisseur
def accessDATABASE4():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('400x400')
            select_window.minsize(400, 400)
            select_window.configure(bg='#f1f1f1')

            # Table selection variable
            selected_table = StringVar()

            def update_table_dropdownfr():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    table_list = [table[0] for table in tables]
                    select_dropdownfr['menu'].delete(0, END)
                    for table in table_list:
                        select_dropdownfr['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Error retrieving table list: {e}")
                finally:
                    cursor.close()

            def display_table_contentsfr():
                table_namefr = selected_table.get()
                if table_namefr:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_namefr}")
                        rows = cursor.fetchall()
                        table_data = ""
                        for row in rows:
                            table_data += str(row) + "\n"
                            table_text.delete("1.0", END)
                            table_text.insert(END, table_data)
                    except my.errors.ProgrammingError as e:
                        print(f"Error retrieving data from table {table_namefr}: {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                select_window.destroy()

            def add_new_tablefr():
                table_namefr = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_namefr:
                    column_datafr = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_datafr:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_namefr} ({column_datafr})")
                            con.commit()
                            print(f"New table '{table_namefr}' created successfully.")
                            update_table_dropdownfr()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")
                        finally:
                            cursor.close()
            
            def add_new_columnfr():
                table_name = selected_table.get()
                if table_name:
                    column_name = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                    if column_name:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(255)")
                            con.commit()
                            print(f"New column '{column_name}' added to table '{table_name}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error adding new column: {e}")
                        finally:
                            cursor.close()

            def delete_columnfr():
                table_namefr = selected_table.get()
                if table_namefr:
                    column_namefr = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_namefr:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namefr} DROP COLUMN {column_namefr}")
                            con.commit()
                            print(f"Column '{column_namefr}' deleted from table '{table_namefr}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_namefr():
                table_namefr = selected_table.get()
                if table_namefr:
                    old_column_namefr = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_namefr = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_namefr and new_column_namefr:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namefr} RENAME COLUMN {old_column_namefr} TO {new_column_namefr}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_namefr}' changed to '{new_column_namefr}' successfully.")
                        except my.errors.ProgrammingError as e:
                             messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")

            def delete_tablefr():
                   table_namefr = selected_table.get()
                   if table_namefr:
                       confirmfr = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_namefr}'?")
                       if confirmfr:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_namefr}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_namefr}' deleted successfully.")
                               update_table_dropdownfr()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()

            def insert_valuesfr():
                table_namefr = selected_table.get()
                if table_namefr:
                    values = simpledialog.askstring("Insert Values", "Enter comma-separated values:")
                    if values:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"INSERT INTO {table_namefr} VALUES ({values})")
                            con.commit()
                            messagebox.showinfo("Insert Values", "Values inserted successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error inserting values: {e}")
                        finally:
                            cursor.close()

             # Table selection label
            select_label = Label(select_window, text="Select Table fournisseur:", font=("Arial", 12), bg='#f1f1f1')
            select_label.pack()

            # Table selection dropdownArticl
            select_dropdownfr = OptionMenu(select_window, selected_table, "fournisseur")
            select_dropdownfr.pack()

            display_button4 = Button(select_window, text="Display Tablefr ", command=display_table_contentsfr, font=("Arial", 12))
            display_button4.pack(pady=5)

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_button = Button(select_window, text="Return to Menu", command=return_to_menu, font=("Arial", 12))
            return_button.pack(pady=5)

            add_table_button = Button(select_window, text="Add New Tablefr", command=add_new_tablefr, font=("Arial", 12))
            add_table_button.pack(pady=5)

            add_column_buttonfr = Button(select_window, text="Add New Columnfr", command=add_new_columnfr, font=("Arial", 12))
            add_column_buttonfr.pack(pady=5)

            delete_column_buttonfr = Button(select_window, text="Delete Columnfr", command=delete_columnfr, font=("Arial", 12))
            delete_column_buttonfr.pack(pady=5)

            change_name_button = Button(select_window, text="Change Column Namefr", command=change_column_namefr, font=("Arial", 12))
            change_name_button.pack(pady=5)

            delete_table_buttonfr = Button(select_window, text="Delete Tablefr", command=delete_tablefr, font=("Arial", 12))
            delete_table_buttonfr.pack(pady=10)

            insert_values_buttonfr = Button(select_window, text="Insert Valuesfr", command=insert_valuesfr, font=("Arial", 12))
            insert_values_buttonfr.pack(pady=10)

            def change_table_namefr():
                current_table_namefr = table_labelfr.cget("text")  # Get the current table name from the label
                new_table_namefr = new_table_entryfr.get()  # Get the new table name from an Entry widget or any other source
                
                # Update the table name in the Tkinter interface
                table_labelfr.config(text=new_table_namefr)
                
                try:
                    # Connect to the database
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestionstock'
                    )
                    cursor = con.cursor()
                    
                    # Execute the SQL query to rename the table
                    rename_query = f"ALTER TABLE `{current_table_namefr}` RENAME TO `{new_table_namefr}`"
                    cursor.execute(rename_query)
                    con.commit()
                    
                    print("Table name changed successfully.")
                
                except my.Error as e:
                    print("Error while changing table name:", e)
                
                finally:
                    # Close the database connection
                    if con.is_connected():
                        cursor.close()
                        con.close()

             # Create a Tkinter window
        select_window = tk.Tk()

        # Create a label for the current table name
        table_labelfr = tk.Label(select_window, text="Nom de la table :")
        table_labelfr.pack()

        # Create an Entry widget to input the new table name
        new_table_entryfr = tk.Entry(select_window)
        new_table_entryfr.pack()

        # Create a button to trigger the table name change
        change_buttonfr = tk.Button(select_window, text="Changer le nom", command=change_table_namefr)
        change_buttonfr.pack()
            
        select_window.mainloop()

    
    except my.errors as e:
        print(e)


#pour catégorie
def accessDATABASE5():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('400x400')
            select_window.minsize(400, 400)
            select_window.configure(bg='#f1f1f1')

            # Table selection variable
            selected_table = StringVar()
            
            def update_table_dropdowncat():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    table_list = [table[0] for table in tables]
                    select_dropdowncat['menu'].delete(0, END)
                    for table in table_list:
                        select_dropdowncat['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Error retrieving table list: {e}")
                finally:
                    cursor.close()

            # Function to display table contents
            def display_table_contentscat():
                table_namecat = selected_table.get()
                if table_namecat:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_namecat}")
                        rows = cursor.fetchall()
                        table_data = ""
                        for row in rows:
                            table_data += str(row) + "\n"
                            table_text.delete("1.0", END)
                            table_text.insert(END, table_data)
                    except my.errors.ProgrammingError as e:
                        print(f"Error retrieving data from table {table_namecat}: {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                select_window.destroy()

            def add_new_tablecat():
                table_namecat = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_namecat:
                    column_datacat = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_datacat:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_namecat} ({column_datacat})")
                            con.commit()
                            print(f"New table '{table_namecat}' created successfully.")
                            update_table_dropdowncat()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")
                        finally:
                            cursor.close()

            def add_new_columncat():
                table_namecat = selected_table.get()
                if table_namecat:
                    column_namecat = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                    if column_namecat:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecat} ADD COLUMN {column_namecat} VARCHAR(255)")
                            con.commit()
                            print(f"New column '{column_namecat}' added to table '{table_namecat}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error adding new column: {e}")
                        finally:
                            cursor.close()

            def delete_columncat():
                table_namecat = selected_table.get()
                if table_namecat:
                    column_namecat = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_namecat:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecat} DROP COLUMN {column_namecat}")
                            con.commit()
                            print(f"Column '{column_namecat}' deleted from table '{table_namecat}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_namecat():
                table_namecat = selected_table.get()
                if table_namecat:
                    old_column_namecat = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_namecat = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_namecat and new_column_namecat:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_namecat} RENAME COLUMN {old_column_namecat} TO {new_column_namecat}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_namecat}' changed to '{new_column_namecat}' successfully.")
                        except my.errors.ProgrammingError as e:
                             messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")
            def delete_tablecat():
                   table_namecat = selected_table.get()
                   if table_namecat:
                       confirmcat = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_namecat}'?")
                       if confirmcat:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_namecat}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_namecat}' deleted successfully.")
                               update_table_dropdowncat()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()

            def insert_valuescat():
                table_namecat = selected_table.get()
                if table_namecat:
                    values = simpledialog.askstring("Insert Values", "Enter comma-separated values:")
                    if values:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"INSERT INTO {table_namecat} VALUES ({values})")
                            con.commit()
                            messagebox.showinfo("Insert Values", "Values inserted successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error inserting values: {e}")
                        finally:
                            cursor.close()

            # Table selection label
            select_label = Label(select_window, text="Select Table catégorie:", font=("Arial", 12), bg='#f1f1f1')
            select_label.pack()

            # Table selection dropdown
            select_dropdowncat = OptionMenu(select_window, selected_table, "catégorie")
            select_dropdowncat.pack()

            # Display Table button
            display_buttoncat = Button(select_window, text="Display Tablecat", command=display_table_contentscat, font=("Arial", 12))
            display_buttoncat.pack(pady=5)

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_buttoncat = Button(select_window, text="Return to Menu", command=return_to_menu, font=("Arial", 12))
            return_buttoncat.pack(pady=5)

            add_table_buttoncat = Button(select_window, text="Add New Table", command=add_new_tablecat, font=("Arial", 12))
            add_table_buttoncat.pack(pady=5)

            add_column_buttoncat = Button(select_window, text="Add New Column", command=add_new_columncat, font=("Arial", 12))
            add_column_buttoncat.pack(pady=5)

            delete_column_buttoncat = Button(select_window, text="Delete Column", command=delete_columncat, font=("Arial", 12))
            delete_column_buttoncat.pack(pady=5)

            change_name_buttoncat = Button(select_window, text="Change Column Name", command=change_column_namecat, font=("Arial", 12))
            change_name_buttoncat.pack(pady=5)

            delete_table_buttoncat = Button(select_window, text="Delete Table", command=delete_tablecat, font=("Arial", 12))
            delete_table_buttoncat.pack(pady=10)

            insert_values_button = Button(select_window, text="Insert Values", command=insert_valuescat, font=("Arial", 12))
            insert_values_button.pack(pady=10)
            
        def change_table_namecat():
            current_table_namecat = table_labelcat.cget("text")  # Get the current table name from the label
            new_table_namecat = new_table_entrycat.get()  # Get the new table name from an Entry widget or any other source
            
            # Update the table name in the Tkinter interface
            table_labelcat.config(text=new_table_namecat)
            
            try:
                # Connect to the database
                con = my.connect(
                    user='root',
                    passwd='',
                    host='localhost',
                    port=3306,
                    database='gestionstock'
                )
                cursor = con.cursor()
                
                # Execute the SQL query to rename the table
                rename_query = f"ALTER TABLE `{current_table_namecat}` RENAME TO `{new_table_namecat}`"
                cursor.execute(rename_query)
                con.commit()
                
                print("Table name changed successfully.")
            
            except my.Error as e:
                print("Error while changing table name:", e)
            
            finally:
                # Close the database connection
                if con.is_connected():
                    cursor.close()
                    con.close()

            # Create a Tkinter window
        select_window = tk.Tk()

        # Create a label for the current table name
        table_labelcat = tk.Label(select_window, text="Nom de la table :")
        table_labelcat.pack()

        # Create an Entry widget to input the new table name
        new_table_entrycat = tk.Entry(select_window)
        new_table_entrycat.pack()

        # Create a button to trigger the table name change
        change_buttoncat = tk.Button(select_window, text="Changer le nomcat", command=change_table_namecat)
        change_buttoncat.pack()

        select_window.mainloop()             

    except my.errors as e:
        print(e)

#pour livraison
def access_DATABASE6():
    try:
        con = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        if con.is_connected():
            print("Connected to the database")
            # Create a new window for selecting the table
            select_window = Tk()
            select_window.title('Select Table')
            select_window.geometry('600x600')
            select_window.minsize(400, 400)
            select_window.configure(bg='silver')

             # Table selection variable
            selected_table = StringVar()

            def update_table_dropdownliv():
                cursor = con.cursor()
                try:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    table_list = [table[0] for table in tables]
                    select_dropdownliv['menu'].delete(0, END)
                    for table in table_list:
                        select_dropdownliv['menu'].add_command(label=table, command=lambda value=table: selected_table.set(value))
                except my.errors.ProgrammingError as e:
                    print(f"Error retrieving table list: {e}")
                finally:
                    cursor.close()

            # Function to display table contents
            def display_table_contentsliv():
                table_nameliv = selected_table.get()
                if table_nameliv:
                    cursor = con.cursor()
                    try:
                        cursor.execute(f"SELECT * FROM {table_nameliv}")
                        rows = cursor.fetchall()
                        table_data = ""
                        for row in rows:
                            table_data += str(row) + "\n"
                            table_text.delete("1.0", END)
                            table_text.insert(END, table_data)
                    except my.errors.ProgrammingError as e:
                        print(f"Error retrieving data from table {table_nameliv}: {e}")
                    finally:
                        cursor.close()

            def return_to_menu():
                    select_window.destroy()

            def add_new_tableliv():
                table_nameliv = simpledialog.askstring("Add New Table", "Enter the name of the new table:")
                if table_nameliv:
                    column_dataliv = simpledialog.askstring("Add New Table", "Enter column data (column1_name column1_type, column2_name column2_type, ...):")
                    if column_dataliv:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"CREATE TABLE {table_nameliv} ({column_dataliv})")
                            con.commit()
                            print(f"New table '{table_nameliv}' created successfully.")
                            update_table_dropdownliv()
                        except my.errors.ProgrammingError as e:
                            print(f"Error creating new table: {e}")
                        finally:
                            cursor.close()

            def add_new_columnliv():
                table_nameliv = selected_table.get()
                if table_nameliv:
                    column_nameliv = simpledialog.askstring("Add New Column", "Enter the name of the new column:")
                    if column_nameliv:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_nameliv} ADD COLUMN {column_nameliv} VARCHAR(255)")
                            con.commit()
                            print(f"New column '{column_nameliv}' added to table '{table_nameliv}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error adding new column: {e}")
                        finally:
                            cursor.close()

            def delete_columnliv():
                table_nameliv = selected_table.get()
                if table_nameliv:
                    column_nameliv = simpledialog.askstring("Delete Column", "Enter the name of the column to delete:")
                    if column_nameliv:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_nameliv} DROP COLUMN {column_nameliv}")
                            con.commit()
                            print(f"Column '{column_nameliv}' deleted from table '{table_nameliv}' successfully.")
                        except my.errors.ProgrammingError as e:
                            print(f"Error deleting column: {e}")
                        finally:
                            cursor.close()

            def change_column_nameliv():
                table_nameliv = selected_table.get()
                if table_nameliv:
                    old_column_nameliv = simpledialog.askstring("Change Column Name", "Enter the old name of the column:")
                    new_column_nameliv = simpledialog.askstring("Change Column Name", "Enter the new name of the column:")
                    if old_column_nameliv and new_column_nameliv:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"ALTER TABLE {table_nameliv} RENAME COLUMN {old_column_nameliv} TO {new_column_nameliv}")
                            con.commit()
                            messagebox.showinfo("Column Name Change", f"Column name '{old_column_nameliv}' changed to '{new_column_nameliv}' successfully.")
                        except my.errors.ProgrammingError as e:
                             messagebox.showerror("Error", f"Error changing column name: {e}")
                        finally:
                            cursor.close()
                    else:
                        messagebox.showwarning("Input Error", "Please enter both the old and new column names.")

            def delete_tableliv():
                   table_nameliv = selected_table.get()
                   if table_nameliv:
                       confirmliv = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the table '{table_nameliv}'?")
                       if confirmliv:
                           cursor = con.cursor()
                           try:
                               cursor.execute(f"DROP TABLE {table_nameliv}")
                               con.commit()
                               messagebox.showinfo("Table Deletion", f"Table '{table_nameliv}' deleted successfully.")
                               update_table_dropdownliv()
                           except my.errors.ProgrammingError as e:
                               messagebox.showerror("Error", f"Error deleting table: {e}")
                           finally:
                               cursor.close()

            def insert_valuesliv():
                table_nameliv = selected_table.get()
                if table_nameliv:
                    values = simpledialog.askstring("Insert Values", "Enter comma-separated values:")
                    if values:
                        cursor = con.cursor()
                        try:
                            cursor.execute(f"INSERT INTO {table_nameliv} VALUES ({values})")
                            con.commit()
                            messagebox.showinfo("Insert Values", "Values inserted successfully.")
                        except my.errors.ProgrammingError as e:
                            messagebox.showerror("Error", f"Error inserting values: {e}")
                        finally:
                            cursor.close()


            # Table selection label
            select_label = Label(select_window, text="Select Table livraison:", font=("Arial", 12), bg='#f1f1f1')
            select_label.pack()

             # Table selection dropdown
            select_dropdownliv = OptionMenu(select_window, selected_table, "livraison")
            select_dropdownliv.pack()

            display_buttonliv = Button(select_window, text="Display Table", command=display_table_contentsliv, font=("Arial", 12))
            display_buttonliv.pack(pady=5)

            table_text = Text(select_window, height=10, width=50)
            table_text.pack()

            return_buttonliv = Button(select_window, text="Return to Menu", command=return_to_menu, font=("Arial", 12))
            return_buttonliv.pack(pady=5)

            add_table_buttonliv = Button(select_window, text="Add New Tableliv", command=add_new_tableliv, font=("Arial", 12))
            add_table_buttonliv.pack(pady=5)

            add_column_buttonliv = Button(select_window, text="Add New Columnliv", command=add_new_columnliv, font=("Arial", 12))
            add_column_buttonliv.pack(pady=5)

            delete_column_buttonliv = Button(select_window, text="Delete Columnliv", command=delete_columnliv, font=("Arial", 12))
            delete_column_buttonliv.pack(pady=5)

            change_name_buttonliv = Button(select_window, text="Change Column Nameliv", command=change_column_nameliv, font=("Arial", 12))
            change_name_buttonliv.pack(pady=5)

            delete_table_buttonliv = Button(select_window, text="Delete Tableliv", command=delete_tableliv, font=("Arial", 12))
            delete_table_buttonliv.pack(pady=5)

            insert_values_buttonliv = Button(select_window, text="Insert Valuesliv", command=insert_valuesliv, font=("Arial", 12))
            insert_values_buttonliv.pack(pady=10)

            def change_table_nameliv():
                current_table_name = table_labelliv.cget("text")  # Get the current table name from the label
                new_table_name = new_table_entryliv.get()  # Get the new table name from an Entry widget or any other source
                
                # Update the table name in the Tkinter interface
                table_labelliv.config(text=new_table_name)
                
                try:
                    # Connect to the database
                    con = my.connect(
                        user='root',
                        passwd='',
                        host='localhost',
                        port=3306,
                        database='gestionstock'
                    )
                    cursor = con.cursor()
                    
                    # Execute the SQL query to rename the table
                    rename_query = f"ALTER TABLE `{current_table_name}` RENAME TO `{new_table_name}`"
                    cursor.execute(rename_query)
                    con.commit()
                    
                    print("Table name changed successfully.")
                
                except my.Error as e:
                    print("Error while changing table name:", e)
                
                finally:
                    # Close the database connection
                    if con.is_connected():
                        cursor.close()
                        con.close()

                # Create a Tkinter window
            select_window = tk.Tk()

            # Create a label for the current table name
            table_labelliv = tk.Label(select_window, text="Nom de la table :")
            table_labelliv.pack()

            # Create an Entry widget to input the new table name
            new_table_entryliv = tk.Entry(select_window)
            new_table_entryliv.pack()

            # Create a button to trigger the table name change
            change_button = tk.Button(select_window, text="Changer le nom", command=change_table_nameliv)
            change_button.pack()



            select_window.mainloop()



    except my.errors as e:
        print(e)


def calculate_sales_rate():
    try:
        # Connectez-vous à la base de données
        connection = my.connect(
            user='root',
            passwd='',
            host='localhost',
            port=3306,
            database='gestionstock'
        )
        cursor = connection.cursor()

        # Exécutez la requête SQL pour calculer le taux de vente
        query = "SELECT (SUM(quantité_en_stock) / SUM(prix_de_vente)) * 100 AS taux_vente FsROM produit"
        cursor.execute(query)
        result = cursor.fetchone()

        # Affichez le résultat dans une boîte de dialogue
        tk.messagebox.showinfo("Taux de vente", f"Le taux de vente est de {result[0]}%")

    except my.Error as e:
        tk.messagebox.showerror("Erreur", f"Erreur lors du calcul du taux de vente : {str(e)}")

    finally:
        # Fermez la connexion à la base de données
        if connection.is_connected():
            cursor.close()
            connection.close()

# Créez la fenêtre principale
window = tk.Tk()
window.title("Statistiques de gestion de stock")

# Ajoutez un bouton pour le taux de vente
sales_rate_button = tk.Button(window, text="Taux de vente", command=calculate_sales_rate)
sales_rate_button.pack()

# Ajoutez d'autres boutons pour les autres statistiques

# Lancez la boucle principale de l'interface utilisateur
window.mainloop()


fenetre = Tk()
fenetre.geometry('400x400')
fenetre.title('GESTION DE STOCK')
fenetre['bg'] = '#f1f1f1'
fenetre.resizable(height=False, width=False)
fenetre.configure(background='#00BFFF')

image_label = Label(fenetre)
image_label.pack()

# Chargement de l'image
image = PhotoImage(file="Capture d’écran 2023-06-12 101918.png")
image = image.subsample(8)
# Configuration de l'image dans le widget Label
image_label.config(image=image)

# Login Button
login_button = Button(fenetre, text="Login", command=login_window, font=("Arial", 12))
login_button.pack(pady=5)

login_button1 = Button(fenetre, text="produit", command=accessDATABASE1, font=("Arial", 12))
login_button1.pack(pady=5)

login_button2 = Button(fenetre, text="commande", command=accessDATABASE2, font=("Arial", 12))
login_button2.pack(pady=5)

login_button3 = Button(fenetre, text="client", command=accessDATABASE3, font=("Arial", 12))
login_button3.pack(pady=5)

login_button4 = Button(fenetre, text="fournissseur", command=accessDATABASE4, font=("Arial", 12))
login_button4.pack(pady=5)

login_button5 = Button(fenetre, text="catégorie", command=accessDATABASE5, font=("Arial", 12))
login_button5.pack(pady=5)

login_button5 = Button(fenetre, text="livraison", command=access_DATABASE6, font=("Arial", 12))
login_button5.pack(pady=5)

# Exit Button
exit_button = Button(fenetre, text="quitter", command=fenetre.quit, font=("Arial", 12))
exit_button.pack(pady=5)


fenetre.mainloop()

