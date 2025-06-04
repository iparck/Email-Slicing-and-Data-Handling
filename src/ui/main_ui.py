from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EmailSlicer(object):
    def setupUi(self, EmailSlicer):
        EmailSlicer.setObjectName("EmailSlicer")
        EmailSlicer.resize(1008, 580)
        EmailSlicer.setWindowTitle("Email Slicer & Data Handling")
        
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(EmailSlicer)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        
        self.Left_Main = QtWidgets.QVBoxLayout()
        self.Left_Main.setObjectName("Left_Main")
        
        self.titleLabel = QtWidgets.QLabel(EmailSlicer)
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(26)
        self.titleLabel.setFont(font)
        self.titleLabel.setText("Email Slicer & Data Handler")
        self.titleLabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.titleLabel.setMargin(10)
        self.titleLabel.setObjectName("titleLabel")
        self.Left_Main.addWidget(self.titleLabel)
        
        self.inputGroup = QtWidgets.QGroupBox(EmailSlicer)
        self.inputGroup.setTitle("Input Section")
        self.inputGroup.setObjectName("inputGroup")
        
        self.formLayout = QtWidgets.QFormLayout(self.inputGroup)
        self.formLayout.setObjectName("formLayout")
        
        self.emailLabel = QtWidgets.QLabel(self.inputGroup)
        self.emailLabel.setText("Email Address:")
        self.emailLabel.setObjectName("emailLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.emailLabel)
        
        self.email_input = QtWidgets.QLineEdit(self.inputGroup)
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setObjectName("email_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.email_input)
        
        self.Left_Main.addWidget(self.inputGroup)
        
        self.actionGroup = QtWidgets.QGroupBox(EmailSlicer)
        self.actionGroup.setTitle("Actions")
        self.actionGroup.setObjectName("actionGroup")
        
        self.buttonLayout = QtWidgets.QGridLayout(self.actionGroup)
        self.buttonLayout.setObjectName("buttonLayout")
        
        self.slice_button = QtWidgets.QPushButton(self.actionGroup)
        self.slice_button.setText("Slice Email")
        self.slice_button.setObjectName("slice_button")
        self.buttonLayout.addWidget(self.slice_button, 0, 0, 1, 1)
        
        self.load_db_button = QtWidgets.QPushButton(self.actionGroup)
        self.load_db_button.setText("Load from Database")
        self.load_db_button.setObjectName("load_db_button")
        self.buttonLayout.addWidget(self.load_db_button, 0, 1, 1, 1)
        
        self.bulk_upload_button = QtWidgets.QPushButton(self.actionGroup)
        self.bulk_upload_button.setText("Bulk Upload")
        self.bulk_upload_button.setObjectName("bulk_upload_button")
        self.buttonLayout.addWidget(self.bulk_upload_button, 0, 2, 1, 1)
        
        self.save_file_button = QtWidgets.QPushButton(self.actionGroup)
        self.save_file_button.setText("Save to File")
        self.save_file_button.setObjectName("save_file_button")
        self.buttonLayout.addWidget(self.save_file_button, 1, 0, 1, 1)
        
        self.load_file_button = QtWidgets.QPushButton(self.actionGroup)
        self.load_file_button.setText("Load from File")
        self.load_file_button.setObjectName("load_file_button")
        self.buttonLayout.addWidget(self.load_file_button, 1, 1, 1, 1)
        
        self.save_db_button = QtWidgets.QPushButton(self.actionGroup)
        self.save_db_button.setText("Save to Database")
        self.save_db_button.setObjectName("save_db_button")
        self.buttonLayout.addWidget(self.save_db_button, 1, 2, 1, 1)
        
        self.search_user_button = QtWidgets.QPushButton(self.actionGroup)
        self.search_user_button.setText("Search Database By Username")
        self.search_user_button.setObjectName("search_user_button")
        self.buttonLayout.addWidget(self.search_user_button, 2, 0, 1, 3)
        
        self.Left_Main.addWidget(self.actionGroup)
        
        self.tableGroup = QtWidgets.QGroupBox(EmailSlicer)
        self.tableGroup.setTitle("Email Data (temporary)")
        self.tableGroup.setObjectName("tableGroup")
        
        self.tableLayout = QtWidgets.QVBoxLayout(self.tableGroup)
        self.tableLayout.setObjectName("tableLayout")
        
        self.email_temp_table = QtWidgets.QTableWidget(self.tableGroup)
        self.email_temp_table.setRowCount(0)
        self.email_temp_table.setColumnCount(3)
        self.email_temp_table.setObjectName("email_temp_table")
        
        item = QtWidgets.QTableWidgetItem()
        item.setText("Username")
        self.email_temp_table.setHorizontalHeaderItem(0, item)
        
        item = QtWidgets.QTableWidgetItem()
        item.setText("Domain")
        self.email_temp_table.setHorizontalHeaderItem(1, item)
        
        item = QtWidgets.QTableWidgetItem()
        item.setText("Extension")
        self.email_temp_table.setHorizontalHeaderItem(2, item)
        
        self.tableLayout.addWidget(self.email_temp_table)
        self.Left_Main.addWidget(self.tableGroup)
        
        self.Right_Main = QtWidgets.QVBoxLayout()
        self.Right_Main.setObjectName("Right_Main")
        
        self.databaseGroup = QtWidgets.QGroupBox(EmailSlicer)
        self.databaseGroup.setTitle("Database")
        self.databaseGroup.setObjectName("databaseGroup")
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.databaseGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.database_email_table = QtWidgets.QTableWidget(self.databaseGroup)
        self.database_email_table.setColumnCount(3)
        self.database_email_table.setObjectName("database_email_table")
        
        item = QtWidgets.QTableWidgetItem()
        item.setText("Username")
        self.database_email_table.setHorizontalHeaderItem(0, item)
        
        item = QtWidgets.QTableWidgetItem()
        item.setText("Domain")
        self.database_email_table.setHorizontalHeaderItem(1, item)
        
        item = QtWidgets.QTableWidgetItem()
        item.setText("Extension")
        self.database_email_table.setHorizontalHeaderItem(2, item)
        
        self.verticalLayout_2.addWidget(self.database_email_table)
        self.Right_Main.addWidget(self.databaseGroup)
        
        self.horizontalLayout_3.addLayout(self.Left_Main, 5)
        self.horizontalLayout_3.addLayout(self.Right_Main, 4)

        QtCore.QMetaObject.connectSlotsByName(EmailSlicer)

    def retranslateUi(self, EmailSlicer):
        _translate = QtCore.QCoreApplication.translate
        EmailSlicer.setWindowTitle(_translate("EmailSlicer", "Email Slicer & Data Handling"))
        self.titleLabel.setText(_translate("EmailSlicer", "Email Slicer & Data Handler"))
        self.inputGroup.setTitle(_translate("EmailSlicer", "Input Section"))
        self.emailLabel.setText(_translate("EmailSlicer", "Email Address:"))
        self.email_input.setPlaceholderText(_translate("EmailSlicer", "Enter email address"))
        self.actionGroup.setTitle(_translate("EmailSlicer", "Actions"))
        self.slice_button.setText(_translate("EmailSlicer", "Slice Email"))
        self.load_db_button.setText(_translate("EmailSlicer", "Load from Database"))
        self.save_file_button.setText(_translate("EmailSlicer", "Save to File"))
        self.load_file_button.setText(_translate("EmailSlicer", "Load from File"))
        self.save_db_button.setText(_translate("EmailSlicer", "Save to Database"))
        self.bulk_upload_button.setText(_translate("EmailSlicer", "Bulk Upload"))
        self.search_user_button.setText(_translate("EmailSlicer", "Search Database By Username"))
        self.tableGroup.setTitle(_translate("EmailSlicer", "Email Data (temporary)"))
        self.databaseGroup.setTitle(_translate("EmailSlicer", "Database"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EmailSlicer = QtWidgets.QWidget()
    ui = Ui_EmailSlicer()
    ui.setupUi(EmailSlicer)
    EmailSlicer.show()
    sys.exit(app.exec_())