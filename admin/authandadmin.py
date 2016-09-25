#! /usr/bin/env python

""" Authorization and Admin panel ui """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from contextlib import contextmanager
from authAndAdminGUI.admin_stack import Ui_Form as AdminPop
from authAndAdminGUI.addroles_popup import Ui_addroles as AddRolesPop
from authAndAdminGUI.newgroup_popup import Ui_newgroup as NewGroupPop
from authAndAdminGUI.assignuser_popup import Ui_adduser as AssignUserPop
from authAndAdminGUI.createuser_popup import Ui_newuser as NewUserPop
from authAndAdminGUI.login import Ui_Dialog as LoginPop
from PySide.QtGui import QDialog, QMessageBox, QWidget, QTableWidgetItem, QAbstractItemView
from PySide.QtCore import Qt
from authandadmin_tryton import AccessUser
import re
from GUI import settings

Roles = {'Inventory': False, 'Billing': False, 'Menu': False, 'Employee': False,
         'Waste': False,
         'Report': False, 'Admin': False}


def auto_capital(linedit):
    """
    capitalizes the character entered into the linedit
    :param linedit: the linedit object to be modified
    :return: none
    """
    edit = linedit
    text = edit.text()
    edit.setText(text.title())


class Login(QDialog):
    """
    login module to check the authenticity of the user
    """

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.ui = LoginPop()
        self.ui.setupUi(self)
        self.ui.loginpopup_reset_button.clicked.connect(self.clear_linedit)
        self.ui.loginpopup_login_button.clicked.connect(self.authenticate)
        self.valid = False
        self.access = AccessUser()
        self.user_admin = False

    def clear_linedit(self):
        """
        :return:clears the field from the line edit
        """
        self.ui.loginpopup_password_linedit.clear()
        self.ui.loginpopup_usename_linedit.clear()

    def authenticate(self):
        """
        :return: closes the dialog if the user is authenticated else the error is shown
        """
        global Roles
        username = self.ui.loginpopup_usename_linedit.text()
        password = self.ui.loginpopup_password_linedit.text()
        userid, tabs = self.access.validate_user(username, password)
        if userid != 0:
            if userid == 1:
                self.user_admin = True
                settings.access = {'Inventory': True, 'Billing': True, 'Menu': True, 'Employee': True, 'Waste': True,
                                   'Report': True, 'Admin': True}
            else:
                if tabs:
                    settings.access = tabs
                else:
                    settings.access = Roles
            settings.set_settings()
            self.valid = True
            self.close()
        else:
            self.ui.loginpopup_error_label.setText("Wrong Password")


class NewGroup(QDialog):
    """
    a pop up dialogue to add new groups
    """

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.parent = parent
        self.ui = NewGroupPop()
        self.ui.setupUi(self)
        self.ui.newgroup_create_button.clicked.connect(self.create_group)
        self.ui.newgroup_name_linedit.textChanged.connect(lambda: auto_capital(linedit=self.ui.newgroup_name_linedit))

    def create_group(self):
        """
        creates a new group
        """
        state = self.parent.login.access.save_group(self.ui.newgroup_name_linedit.text())
        if state[0]:
            QMessageBox.information(self, 'Success!!', state[1], QMessageBox.Ok)
            self.parent.fill_groups()
            self.close()
        else:
            QMessageBox.warning(self, 'Fail!!', state[1], QMessageBox.Ok)


class NewRoles(QDialog):
    """
    Provides a mechanism to handle roles to be assigned to the groups
    """

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.parent = parent
        self.ui = AddRolesPop()
        self.ui.setupUi(self)
        self.check_and_add()
        self.ui.addroles_add_button.clicked.connect(self.add_roles)

    def check_and_add(self):
        """
        checks the parent widgets table and provides only those roles that are not present
        """
        global Roles
        roles = Roles.copy()
        table = self.parent.ui.adminpopup_assign_roles_table
        rows = table.rowCount()
        for i in range(rows):
            item = table.item(i, 0).text()
            if item in roles.keys():
                del roles[item]
        combo = self.ui.addroles_combobox
        combo.addItem('')
        combo.addItems(roles.keys())

    def add_roles(self):
        """
        adds a new role to the parent widgets group selected
        """
        role = self.ui.addroles_combobox.currentText()
        table = self.parent.ui.adminpopup_assign_roles_table
        rows = table.rowCount()
        if role:
            group_name = self.parent.ui.adminpopup_assign_groupname_combobox.currentText()
            status = self.parent.login.access.add_role(group_name, role)
            if status[0]:
                QMessageBox.information(self, 'Success!!', status[1], QMessageBox.Ok)
                table.setRowCount(rows + 1)
                table.setItem(rows, 0, QTableWidgetItem(role))
            else:
                QMessageBox.warning(self, 'Fail!!', status[1], QMessageBox.Ok)


class AssignUser(QDialog):
    """
    Manages users to be added to the parent widgets groups
    """

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.parent = parent
        self.ui = AssignUserPop()
        self.ui.setupUi(self)
        self.ui.adduser_add_button.clicked.connect(self.add_user)
        self.fill_users()

    def fill_users(self):
        """
        fills the users to the combobox
        """
        group = self.parent.ui.adminpopup_assign_groupname_combobox.currentText()
        users = self.parent.login.access.fill_users(group)
        self.ui.adduser_combobox.addItems(users)

    def add_user(self):
        """
        adds a user to the parents widgets selected group
        """
        user = self.ui.adduser_combobox.currentText()
        group = self.parent.ui.adminpopup_assign_groupname_combobox.currentText()
        status = self.parent.login.access.add_user(group_name=group, user_name=user)
        table = self.parent.ui.adminpopup_assign_members_table
        rows = table.rowCount()
        if status[0]:
            QMessageBox.information(self, 'Success!!', status[1], QMessageBox.Ok)
            table.setRowCount(rows + 1)
            table.setItem(rows, 0, QTableWidgetItem(user))
        else:
            QMessageBox.warning(self, 'Fail!!', status[1], QMessageBox.Ok)


class NewUser(QDialog):
    """
    Provides a mechanism to add a new user
    """

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.parent = parent
        self.ui = NewUserPop()
        self.ui.setupUi(self)
        self.ui.newuser_save_button.clicked.connect(self.save_user)
        self.ui.newuser_name_linedit.textChanged.connect(lambda: auto_capital(linedit=self.ui.newuser_name_linedit))

    def save_user(self):
        """
        creates a new user and saves the details passed
        """
        name = self.ui.newuser_name_linedit.text()
        username = self.ui.newuser_username_linedit.text()
        password = self.ui.newuser_password_linedit.text()
        status = self.parent.login.access.create_user(name=name, username=username, password=password)
        if status[0]:
            QMessageBox.information(self, 'Successful!!', status[1], QMessageBox.Ok)
            self.parent.fill_users()
            self.parent.get_user_details()
            self.close()
        else:
            QMessageBox.warning(self, 'Fail!!', status[1], QMessageBox.Ok)


class Admin(QWidget):
    """
    manages the entire admin stack
    """

    def __init__(self, parent=None):
        super(Admin, self).__init__(parent)
        self.ui = AdminPop()
        self.ui.setupUi(self)
        self.setAutoFillBackground(True)
        self.ui.adminFrame.setStyleSheet('#adminFrame{border:1px solid rgb(76, 142, 250);}')
        self.ui.assignFrame.setStyleSheet('#assignFrame{border:1px solid rgb(76, 142, 250);}')
        self.ui.createFrame.setStyleSheet('#createFrame{border:1px solid rgb(76, 142, 250);}')
        self.ui.adminpopup_save_button.clicked.connect(self.save)
        self.ui.adminpopup_dev_checkbox.stateChanged.connect(self.change_level)
        self.ui.adminpopup_assign_groupname_combobox.currentIndexChanged.connect(lambda: self.update_tables())
        self.ui.adminpopup_assign_roles_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.adminpopup_assign_roles_table.itemDoubleClicked.connect(self.popup_edit_roles)
        self.ui.adminpopup_assign_newgroup_button.clicked.connect(self.new_group)
        self.ui.adminpopup_assign_deletegroup_button.clicked.connect(self.delete_group)
        self.ui.adminpopup_assign_addroles_button.clicked.connect(self.add_roles)
        self.ui.adminpopup_assign_addmembers_button.clicked.connect(self.assign_users)
        self.ui.adminpopup_assign_members_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.adminpopup_assign_members_table.itemDoubleClicked.connect(self.popup_edit_users)
        self.ui.adminpopup_assign_delete_button.clicked.connect(self.select_and_delete_user)
        self.ui.adminpopup_createuser_username_combobox.currentIndexChanged.connect(lambda: self.get_user_details())
        self.ui.adminpopup_createuser_delete_button.clicked.connect(self.delete_user)
        self.ui.adminpopup_createuser_save_button.clicked.connect(self.save_user)
        self.ui.adminpopup_createuser_create_button.clicked.connect(self.create_user)
        self.login = None
        # self.authenticate()

    @contextmanager
    def authenticate(self):
        """
        authenticates if the user has an access permission
        :return:yields True or False
        """
        self.login = Login(self)
        self.login.exec_()
        if self.login.user_admin:
            self.load_details()
            self.fill_groups()
            self.fill_users()
            yield True
            self.login.user_admin = False
        else:
            yield False

    def change_level(self, value):
        """
        changes the values of the logging levels in the settings file imported
        :param value:0 or 1
        """
        if value:
            settings.level = 10
        else:
            settings.level = 20
        settings.set_settings()

    def save(self):
        """
        :return:saves the details of the user
        """
        name = self.ui.adminpopup_hotelname_linedit.text()
        street = self.ui.adminpopup_street_linedit.text()
        city = self.ui.adminpopup_city_linedit.text()
        pin = self.ui.adminpopup_pin_linedit.text()
        longitude = self.ui.adminpopup_longitude_linedit.text()
        latitude = self.ui.adminpopup_latitude_linedit.text()
        apikey = self.ui.adminpopup_apikey_linedit.text()
        tax = self.ui.adminpopup_tax_linedit.text()
        profileid = self.ui.adminpopup_profileid_linedit.text()
        password = self.ui.adminpopup_password_linedit.text()
        fssai = self.ui.adminpopup_fssai_linedit.text()
        tin = self.ui.adminpopup_tin_linedit.text()
        pattern = re.compile("xxxxxxxxxx")
        searching = pattern.search(password)
        if not searching:
            ask = QMessageBox.question(self, 'Confirm',
                                       'The password has been changed, do you want to save the new password?',
                                       QMessageBox.Yes | QMessageBox.No)
            if ask == QMessageBox.Yes:
                pass
            else:
                password = None
        details = {'name': name, 'street': street, 'city': city, 'pin': pin, 'longitude': longitude,
                   'latitude': latitude, 'apikey': apikey, 'tax': tax, 'fssai': fssai, 'tin': tin,
                   'profileid': profileid, 'password': password}
        for i, j in details.iteritems():
            if not j:
                QMessageBox.critical(self, 'Error',
                                     'The field %s is not filled properly' % i.title(), QMessageBox.Ok)
                return False
        status = self.login.access.save_details(
            details)  ###also check if the password is changed and prompt a message box
        if status:
            QMessageBox.information(self, "Success!!!", "The details have been saved", QMessageBox.Ok)

    def load_details(self):
        """
        :return:load the fields
        """
        details = self.login.access.get_details()
        if details:
            self.ui.adminpopup_hotelname_linedit.setText(details['name'])
            self.ui.adminpopup_street_linedit.setText(details['street'])
            self.ui.adminpopup_city_linedit.setText(details['city'])
            self.ui.adminpopup_pin_linedit.setText(details['pin'])
            self.ui.adminpopup_longitude_linedit.setText(details['longitude'])
            self.ui.adminpopup_latitude_linedit.setText(details['latitude'])
            self.ui.adminpopup_apikey_linedit.setText(details['apikey'])
            self.ui.adminpopup_tax_linedit.setText(details['tax'])
            self.ui.adminpopup_profileid_linedit.setText(details['profileid'])
            self.ui.adminpopup_password_linedit.setText(details['password'])
            self.ui.adminpopup_fssai_linedit.setText(details['fssai'])
            self.ui.adminpopup_tin_linedit.setText(details['tin'])
        if settings.level == 10:
            self.ui.adminpopup_dev_checkbox.setCheckState(Qt.Checked)

    def fill_groups(self):
        """
        fills the name of the groups in the access roles combobox
        :return:none
        """
        combo = self.ui.adminpopup_assign_groupname_combobox
        combo.clear()
        combo.addItem('')
        combo.addItems(self.login.access.get_group_list())

    def update_tables(self):
        """
        updates the roles table
        :return:none
        """
        group = self.ui.adminpopup_assign_groupname_combobox.currentText()
        table = self.ui.adminpopup_assign_roles_table
        member_table = self.ui.adminpopup_assign_members_table
        if group:
            roles = self.login.access.get_roles(group)
            table.setRowCount(len(roles))
            for i, role in enumerate(roles):
                table.setItem(i, 0, QTableWidgetItem(role))
            users = self.login.access.list_group_users(group)
            member_table.setRowCount(len(users))
            for i, user in enumerate(users):
                member_table.setItem(i, 0, QTableWidgetItem(user))
        else:
            table.clearContents()
            table.setRowCount(0)
            member_table.clearContents()
            member_table.setRowCount(0)


    def new_group(self):
        """
        pops up a dialogue to add a new group
        :return:none
        """
        group = NewGroup(parent=self)
        group.exec_()

    def delete_group(self):
        """
        deletes the selected group in the assign
        :return:none
        """
        group = self.ui.adminpopup_assign_groupname_combobox.currentText()
        if group:
            status = self.login.access.delete_group(group)
            if status[0]:
                QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
                self.fill_groups()
            else:
                QMessageBox.warning(self, 'Fail', status[1], QMessageBox.Ok)

    def add_roles(self):
        """
        add the roles to the group
        :return:none
        """
        roles = NewRoles(parent=self)
        roles.exec_()

    def popup_edit_roles(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        table = self.ui.adminpopup_assign_roles_table
        model_index = table.indexFromItem(item)
        row = model_index.row()
        item = table.item(row, 0)
        role = item.text()
        group = self.ui.adminpopup_assign_groupname_combobox.currentText()
        if item:
            ask = QMessageBox.question(self, 'Confirm',
                                       'Role will be removed from the group',
                                       QMessageBox.Yes | QMessageBox.No)
            if ask == QMessageBox.Yes:
                status = self.login.access.delete_role(group_name=group, role=role)
                if status[0]:
                    QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
                    table.removeRow(row)
                else:
                    QMessageBox.warning(self, 'Fail', status[1], QMessageBox.Ok)


    def assign_users(self):
        """
        assigns a new user to the group
        :return:none
        """
        assign = AssignUser(parent=self)
        assign.exec_()

    def select_and_delete_user(self):
        """
        searches the selected row in the assign table
        :return:none
        """
        table = self.ui.adminpopup_assign_members_table
        rows = sorted(set(index.row() for index in
                          table.selectedIndexes()))
        if rows:
            self.popup_edit_users(table.item(rows[0], 0))

    def popup_edit_users(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        table = self.ui.adminpopup_assign_members_table
        model_index = table.indexFromItem(item)
        row = model_index.row()
        item = table.item(row, 0)
        members = item.text()
        if item:
            ask = QMessageBox.question(self, 'Confirm',
                                       'The user will be removed from the group, are you sure?',
                                       QMessageBox.Yes | QMessageBox.No)
            if ask == QMessageBox.Yes:
                status = self.login.access.delete_table_user(username=members)
                if status[0]:
                    QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
                    table.removeRow(row)
                else:
                    QMessageBox.warning(self, 'Fail', status[1], QMessageBox.Ok)

    def fill_users(self):
        """
        fills the combo box in create user section
        """
        userlist = self.login.access.get_userlist()
        combo = self.ui.adminpopup_createuser_username_combobox
        combo.clear()
        combo.addItem('')
        combo.addItems(userlist)

    def delete_user(self):
        """
        deletes the selected
        """
        user = self.ui.adminpopup_createuser_name_linedit.text()
        status = self.login.access.delete_user(name=user)
        if status[0]:
            QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
            self.fill_users()
            self.get_user_details()
        else:
            QMessageBox.warning(self, 'Fail', status[1], QMessageBox.Ok)

    def get_user_details(self):
        """
        gets the information of the user selected
        """
        name = self.ui.adminpopup_createuser_username_combobox.currentText()
        if name:
            details = self.login.access.get_user_details(name=name)
            if details:
                self.ui.adminpopup_createuser_name_linedit.setText(details[0])
                self.ui.adminpopup_createuser_username_linedit.setText(details[1])
                self.ui.adminpopup_createuser_password_linedit.setText(details[2])
        else:
            self.ui.adminpopup_createuser_name_linedit.setText('')
            self.ui.adminpopup_createuser_username_linedit.setText('')
            self.ui.adminpopup_createuser_password_linedit.setText('')

    def save_user(self):
        """
        saves the user details of the selected user
        """
        name = self.ui.adminpopup_createuser_name_linedit.text()
        username = self.ui.adminpopup_createuser_username_linedit.text()
        password = self.ui.adminpopup_createuser_password_linedit.text()
        pattern = re.compile("xxxxxxxxxx")
        searching = pattern.search(password)
        if not searching:
            ask = QMessageBox.question(self, 'Confirm',
                                       'The password has been changed, do you want to save the new password?',
                                       QMessageBox.Yes | QMessageBox.No)
            if ask == QMessageBox.Yes:
                pass
            else:
                password = None
        status = self.login.access.save_user_details(name=name, username=username, password=password)
        if status[0]:
            QMessageBox.information(self, 'Success', status[1], QMessageBox.Ok)
            self.fill_users()
        else:
            QMessageBox.warning(self, 'Fail', status[1], QMessageBox.Ok)

    def create_user(self):
        """
        pops up a dialogue to add a new user
        """
        user = NewUser(self)
        user.exec_()