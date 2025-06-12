import sys
from pathlib import Path
import csv, json

from ui.main_ui import Ui_EmailSlicer
import sql.manage_SQL
import qol.load_from_file

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog, QMessageBox


class EmailSlicerApp(Ui_EmailSlicer):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setupUi(widget)
        self.setup()

    def setup(self):
        try:
            self.slice_button.clicked.connect(self.get_input)
            self.save_db_button.clicked.connect(self.save_to_db)
            self.load_db_button.clicked.connect(self.get_database_info)
            self.load_file_button.clicked.connect(self.load_file_data)
            self.save_temp_file_button.clicked.connect(self.save_temp_data)
            self.save_db_file_button.clicked.connect(self.save_db_data)
            self.search_user_button.clicked.connect(self.search_db_by_user)

            self.email_input.returnPressed.connect(self.get_input)
        except Exception as e:
            self.show_error_message("Setup Error", f"Failed to setup UI connections: \n\n{str(e)}")

    def show_error_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def show_success_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def load_file_data(self):
        try:
            file_path, ok1 = QInputDialog.getText(
                self.widget,
                'File Path',
                'Enter absolute file path:'
            )
            
            if not ok1 or not file_path.strip():
                return None
            
            file_path = file_path.strip('"')
            file_path = Path(file_path.replace("\\", '/')).resolve()

            if not file_path.exists():
                self.show_error_message("File Error", f"File not found: {file_path}")
                return None            
            if not file_path.is_file():
                self.show_error_message("File Error", f"Path is not a file: {file_path}")
                return None
            
            usernames, domains, extensions = qol.load_from_file.load_data(file_path)

            if usernames is None or domains is None or extensions is None:
                self.show_error_message("File Error", "Failed to load data from file. Please check file format.")
                return None            
            if len(usernames) == 0:
                self.show_error_message("File Error", "No valid email data found in file.")
                return None

            for i in range(0, len(usernames)):
                self.insert_to_temp_table([usernames[i], domains[i], extensions[i]])  
        except Exception as e:
            self.show_error_message("File error", f"Error loading file: \n\n{e}")

    def save_temp_data(self):
        try:
            file_format = None
            while not file_format:
                file_format, ok1 = QInputDialog.getText(
                    self.widget,
                    'File Format',
                    'Enter format to save data in (json, csv): '
                )
                if not ok1:
                    return 
                if file_format.lower() not in ['json', 'csv']:
                    file_format = None
            file_format = file_format.lower()

            data = []
            table = self.email_temp_table

            if table.rowCount() == 0:
                self.show_error_message("Save Error", "No data to save. The temporary table is empty.")
                return None

            for row in range(table.rowCount()):
                try:
                    u_i = table.item(row, 0).text()
                    d_i = table.item(row, 1).text()
                    e_i = table.item(row, 2).text()
                    data.append([u_i, d_i, e_i])
                except Exception as e:
                    self.show_error_message("Data Error", f"Error reading row {row}: \n\n{str(e)}")
                    continue
            
            data.reverse()

            parent_directory, ok1 = QInputDialog.getText(
                self.widget,
                'Directory',
                'Enter directory to save output data in: '
            )

            if not ok1 or not parent_directory.strip():
                return None
            
            parent_directory = parent_directory.strip('"')
            parent_directory = Path(parent_directory.replace("\\", '/')).resolve()

            if not parent_directory.exists():
                self.show_error_message("Directory Error", f"Directory not found: \n{parent_directory}")
                return None
            if not parent_directory.is_dir():
                self.show_error_message("Directory Error", f"Path is not a directory: {parent_directory}")
                return None

            if file_format == 'csv':
                with open(f'{str(parent_directory)}/output_temp_data.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['username', 'domain', 'extension'])
                    writer.writerows(data)
            
            elif file_format == 'json':
                result = []
                for i in range(len(data)):
                    result.append({
                        'username': data[i][0],
                        'domain': data[i][1],
                        'extension': data[i][2]
                    })
                with open(f'{str(parent_directory)}/output_temp_data.json', 'w') as file:
                    json.dump(result, file, indent=4)
                    

            self.show_success_message("Save Successful", f"Temporary data saved successfully to: {f'{str(parent_directory)}/output_temp_data.{file_format}'}")

        except Exception as e:
            self.show_error_message("Save Error", f"Error saving data: \n\n{str(e)}")

    def save_db_data(self):
        try:
            file_format = None
            while not file_format:
                file_format, ok1 = QInputDialog.getText(
                    self.widget,
                    'File Format',
                    'Enter format to save data in (json, csv): '
                )
                if not ok1:
                    return 
                if file_format.lower() not in ['json', 'csv']:
                    file_format = None
            file_format = file_format.lower()

            data = []
            table = self.database_email_table

            if table.rowCount() == 0:
                self.show_error_message("Save Error", "No data to save. The database table is empty.")
                return None

            for row in range(table.rowCount()):
                try:
                    u_i = table.item(row, 0).text()
                    d_i = table.item(row, 1).text()
                    e_i = table.item(row, 2).text()
                    data.append([u_i, d_i, e_i])
                except Exception as e:
                    self.show_error_message("Data Error", f"Error reading row {row}: \n\n{str(e)}")
                    continue
            
            data.reverse()

            parent_directory, ok1 = QInputDialog.getText(
                self.widget,
                'Directory',
                'Enter directory to save output data in: '
            )

            if not ok1 or not parent_directory.strip():
                return None
            
            parent_directory = parent_directory.strip('"')
            parent_directory = Path(parent_directory.replace("\\", '/')).resolve()

            if not parent_directory.exists():
                self.show_error_message("Directory Error", f"Directory not found: \n{parent_directory}")
                return None
            if not parent_directory.is_dir():
                self.show_error_message("Directory Error", f"Path is not a directory: {parent_directory}")
                return None

            if file_format == 'csv':
                with open(f'{str(parent_directory)}/output_db_data.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['username', 'domain', 'extension'])
                    writer.writerows(data)
            
            elif file_format == 'json':
                result = []
                for i in range(len(data)):
                    result.append({
                        'username': data[i][0],
                        'domain': data[i][1],
                        'extension': data[i][2]
                    })
                with open(f'{str(parent_directory)}/output_db_data.json', 'w') as file:
                    json.dump(result, file, indent=4)

            self.show_success_message("Save Successful", f"Database data saved successfully to: {f'{str(parent_directory)}/output_db_data.{file_format}'}")

        except Exception as e:
            self.show_error_message("Save Error", f"Error saving data: \n\n{str(e)}")

    def save_to_db(self):
        try:
            table = self.email_temp_table
            if table.rowCount() == 0:
                self.show_error_message("Database Error", "No data to save to database. The temporary table is empty.")
                return None
            
            if not self.get_temp_data_and_save():
                return None
            if not self.clear_temp_table():
                return None
            self.show_success_message("Database Save", "Data successfully saved to database.")
            
        except Exception as e:
            self.show_error_message("Database Error", f"Error saving to database: \n\n{str(e)}")

    def clear_temp_table(self):
        try:
            table = self.email_temp_table
            while table.rowCount()>0:
                table.removeRow(0)
            return True
        except Exception as e:
            self.show_error_message("Table Error", f"Error clearing temporary table: {str(e)}")
            return False

    def get_database_info(self):
        try:

            host, ok1 = QInputDialog.getText(
                self.widget,
                'Database Host',
                'Enter database host:',
                text='localhost'
            )
            
            if not ok1 or not host.strip():
                return None
            
            user, ok2 = QInputDialog.getText(
                self.widget,
                'Database User',
                'Enter database username:'
            )
            
            if not ok2 or not user.strip():
                return None
                
            password, ok3 = QInputDialog.getText(
                self.widget,
                'Database Password',
                'Enter database password:'
            )

            if not ok3:
                return None
            
            status = sql.manage_SQL.taking_creds(host.strip(), user.strip(), password)

            if status == True:
                pass
            else:
                self.show_error_message("Database Connection Failed", f"Could not connect to MySQL:\n\n{status}")
                return None
        

            db_name, ok1 = QInputDialog.getText(
                self.widget,
                'Database Name',
                'Enter database name:',
                text='emailSlicing'
            )
            
            if not ok1 or not db_name.strip():
                return None
            
            table_name, ok2 = QInputDialog.getText(
                self.widget,
                'Table Name', 
                'Enter table name:',    
                text='emails'
            )
            
            if not ok2 or not table_name.strip():
                return None
            
            if not db_name.replace('_', '').isalnum():
                self.show_error_message("Database Error", "Database name contains invalid characters. Use only letters, numbers, and underscores.")
                return None            
            if not table_name.replace('_', '').isalnum():
                self.show_error_message("Database Error", "Table name contains invalid characters. Use only letters, numbers, and underscores.")
                return None
                
            sql.manage_SQL.setup(db_name, table_name)
            self.get_db_table_data()
            self.show_success_message("Database Connection", f"Successfully connected to database '{db_name}' and table '{table_name}'.")

        except Exception as e:
            self.show_error_message("Database Error", f"Error connecting to database: \n\n{str(e)}")


    def get_input(self):
        try:
            value = self.email_input.text()
            
            if not value:
                self.show_error_message("Input Error", "Please enter an email address.")
                return
            if "@" not in value:
                self.show_error_message("Email Error", "Invalid email format: Missing '@' symbol.")
                return
            if "." not in value:
                self.show_error_message("Email Error", "Invalid email format: Missing domain extension.")
                return
            if value.count("@") > 1:
                self.show_error_message("Email Error", "Invalid email format: Multiple '@' symbols found.")
                return
            
            self.email_input.setText("")
            self.slice_email(value)
        except Exception as e:
            self.show_error_message("Input Error", f"Error processing input: \n\n{str(e)}")

    def slice_email(self, value):
        try:
            username, domain_extension = value.split("@", 1)
            if "." in domain_extension:
                domain, extension = domain_extension.rsplit(".", 1)
            else:
                self.show_error_message("Email Error", "Invalid domain format: Missing extension.")
                return
            if not username:
                self.show_error_message("Email Error", "Email username cannot be empty.")
                return
            if not domain:
                self.show_error_message("Email Error", "Email domain cannot be empty")
                return
            if not extension:
                self.show_error_message("Email Error", "Email extension cannot be empty")
                return

            self.insert_to_temp_table((username, domain, extension))
        
        except Exception as e:
            self.show_error_message("Email Error", f"Error slicing email: \n\n{str(e)}")

    def insert_to_temp_table(self, data):
        try:
            table = self.email_temp_table

            table.insertRow(0)
            table.setItem(0,0, QTableWidgetItem(data[0]))
            table.setItem(0,1, QTableWidgetItem(data[1]))
            table.setItem(0,2, QTableWidgetItem(data[2]))
        except Exception as e:
            self.show_error_message("Table Error", f"Error inserting data to table: \n\n{str(e)}")


    def get_temp_data_and_save(self):
        try:
            usernames = []  
            domains = []
            extensions = []
            table = self.email_temp_table

            for row in range(table.rowCount()):
                try:
                    u_i = table.item(row, 0).text()
                    d_i = table.item(row, 1).text()
                    e_i = table.item(row, 2).text()
                    usernames.append(u_i)
                    domains.append(d_i)
                    extensions.append(e_i)
                except Exception as e:
                    self.show_error_message("Data Error", f"Error reading temporary table row {row}: \n\n{str(e)}")
                    return False
            
            usernames.reverse()
            domains.reverse()
            extensions.reverse()

            if not usernames or not domains or not extensions:
                return False
            
            if len(usernames) != len(domains) or len(usernames) != len(extensions) or len(domains) != len(extensions):
                self.show_error_message("Database Error", "Data length mismatch. Cannot save to database.")
                return False

            sql.manage_SQL.commit_to_db(usernames, domains, extensions)
            self.update_db_table_data(usernames, domains, extensions)
            
            return True
        except Exception as e:
            self.show_error_message("Table Error", f"Error inserting data to table: \n\n{str(e)}")
            return False

    def update_db_table_data(self, usernames, domains, extensions, data_from_db=False):
        try:
            table = self.database_email_table

            if data_from_db:
                while table.rowCount()>0:
                    table.removeRow(0)

            for i in range(0, len(usernames)):
                try:
                    table.insertRow(0)
                    table.setItem(0,0, QTableWidgetItem(usernames[i]))
                    table.setItem(0,1, QTableWidgetItem(domains[i]))
                    table.setItem(0,2, QTableWidgetItem(extensions[i]))
                except Exception as e:
                    self.show_error_message("Table Error", f"Error updating database table row {i}: \n\n{str(e)}")
                    continue
        except Exception as e:
            self.show_error_message("Database Error", f"Error updating database table: \n\n{str(e)}")

    def get_db_table_data(self):
        try:
            data = sql.manage_SQL.get_data()
            usernames = []
            domains = []
            extensions = []
            for i in data:
                usernames.append(i[1])
                domains.append(i[2])
                extensions.append(i[3])

            self.update_db_table_data(usernames, domains, extensions, data_from_db=True)
        except Exception as e:
            self.show_error_message("Database Error", f"Error getting database table data: \n\n{str(e)}")

    def search_db_by_user(self):
        try:
            username = None
            while not username:
                username, ok1 = QInputDialog.getText(
                    self.widget,
                    'Search...', 
                    'Enter username to be searched: '
                )
                if not ok1:
                    return
                if not username.strip():
                    username = None

            username.strip()

            table = self.database_email_table
            possible = []
            row_number = []
            
            if table.rowCount() == 0:
                self.show_error_message("Search...", "Database table is empty.")
                return

            for row in range(table.rowCount()):
                if table.item(row, 0).text() == username:
                    row_number.append(row + 1)
                elif username in table.item(row, 0).text():
                    possible.append(row+1)
            
            if row_number and possible:
                text = (
                    f"Username match(es) found in row(s) - {row_number}\n"
                    f"Usernames containing entered characters in row(s) - {possible}"
                )
            elif row_number and not possible:
                text = f"Username match(es) found in row(s) {row_number}"
            elif not row_number and possible:
                text = (
                    "No rows found containing exact match\n"
                    f"Usernames containing entered characters in row(s) - {possible}"
                )
            elif not row_number and not possible:
                text = "No matches found."
                self.show_error_message("Search...", text)
                return
            self.show_success_message("Search...", text)

        except Exception as e:
            self.show_error_message("DB Search Error", f"Error searching db table for username. \n\n{str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    EmailSlicer = QtWidgets.QWidget()
    ui = EmailSlicerApp(EmailSlicer)

    EmailSlicer.show()
    sys.exit(app.exec_())
    