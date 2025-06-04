import sys


from ui.main_ui import Ui_EmailSlicer
import sql.manage_SQL

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from PyQt5 import QtWidgets


class EmailSlicerApp(Ui_EmailSlicer):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setupUi(widget)
        self.setup()

    def setup(self):
        self.slice_button.clicked.connect(self.get_input)
        self.save_db_button.clicked.connect(self.save_to_db)
        self.load_db_button.clicked.connect(self.get_database_info)

    def save_to_db(self):
        self.get_temp_data()
        self.clear_temp_table()

    def clear_temp_table(self):
        table = self.email_temp_table
        while table.rowCount()>0:
            table.removeRow(0)

    def get_database_info(self):
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
            
        sql.manage_SQL.setup(db_name, table_name)
        self.get_db_table_data()


    def get_input(self):
        value = self.email_input.text()
        if "@" not in value or "." not in value:
            return
        self.email_input.setText("")

        self.slice_email(value)

    def slice_email(self, value):
        username, domain_extension = value.split("@")
        domain, extension = domain_extension.split(".")

        self.insert_to_temp_table((username, domain, extension))

    def insert_to_temp_table(self, data):
        table = self.email_temp_table

        table.insertRow(0)
        table.setItem(0,0, QTableWidgetItem(data[0]))
        table.setItem(0,1, QTableWidgetItem(data[1]))
        table.setItem(0,2, QTableWidgetItem(data[2]))


    def get_temp_data(self):
        usernames = []
        domains = []
        extensions = []
        table = self.email_temp_table

        for row in range(table.rowCount()):
            u_i = table.item(row, 0).text()
            d_i = table.item(row, 1).text()
            e_i = table.item(row, 2).text()
            usernames.append(u_i)
            domains.append(d_i)
            extensions.append(e_i)
        
        usernames.reverse()
        domains.reverse()
        extensions.reverse()

        self.send_to_database(usernames, domains, extensions)
    
    def send_to_database(self, usernames, domains, extensions):
        sql.manage_SQL.commit_to_db(usernames, domains, extensions)
        self.update_db_table_data(usernames, domains, extensions)

    def update_db_table_data(self, usernames, domains, extensions, data_from_db=False):
        table = self.database_email_table

        if data_from_db:
            while table.rowCount()>0:
                table.removeRow(0)

        for i in range(0, len(usernames)):
            table.insertRow(0)
            table.setItem(0,0, QTableWidgetItem(usernames[i]))
            table.setItem(0,1, QTableWidgetItem(domains[i]))
            table.setItem(0,2, QTableWidgetItem(extensions[i]))

    def get_db_table_data(self):
        data = sql.manage_SQL.get_data()
        usernames = []
        domains = []
        extensions = []
        for i in data:
            usernames.append(i[1])
            domains.append(i[2])
            extensions.append(i[3])

        self.update_db_table_data(usernames, domains, extensions, data_from_db=True)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    EmailSlicer = QtWidgets.QWidget()
    ui = EmailSlicerApp(EmailSlicer)

    EmailSlicer.show()
    sys.exit(app.exec_())
    