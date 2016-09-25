#! /usr/bin/env python

""" Menu Module Ui """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from PySide.QtGui import QWidget, QHBoxLayout, QTabWidget, QApplication, QTableWidgetItem, QSpacerItem, QSizePolicy, \
    QGridLayout, QTableWidget, QPushButton, QAbstractItemView, QDialog, QLineEdit, \
    QMessageBox, QCheckBox, QDoubleValidator, QComboBox, QIntValidator, QShortcut, QKeySequence

from PySide.QtCore import Qt
from menu_popupGUI.menu_add_dialogue import Ui_add_menu_dialogue
from menu_popupGUI.menu_for_each_week import Ui_menu_this_day
from menu_popupGUI.menu_add_eachweek import Ui_add_menu_eachweek
from menu_popupGUI.new_category import Ui_new_category
from menu_tryton import MenuProduct, WeeklyMenu, IngredientsInMenu, CategoryOfProduct
import logging
from GUI import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)


class MenuAddDialogue(QDialog):
    """popup to add new menu entry"""
    global logger

    def __init__(self, parent=None, args=None):
        logger.info('Inside MenuAddDialogue')
        QDialog.__init__(self)
        self.parent = parent
        self.dialogue = Ui_add_menu_dialogue()
        self.dialogue.setupUi(self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.focusInEvent = self.got_focus
        self.search = CategoryOfProduct()
        self.dialogue.menudialogu_delete_button.clicked.connect(self.delete_menu_item)
        self.dialogue.menudialogue_menuIngredients_table_addrow_button.clicked.connect(self.add_new_rows)
        self.dialogue.menudialogue_menuIngredients_table_save_button.clicked.connect(self.save_ingredients)
        self.dialogue.menudialogue_menuIngredients_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dialogue.menudialogue_menuIngredients_table.itemDoubleClicked.connect(self.popup_edit)
        self.dialogue.menudialogue_add_button.clicked.connect(self.add_menu)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.editable = False
        self.menuproduct = MenuProduct()
        self.dish = MenuProduct()
        self.complete_category()
        self.dialogue.menudialogue_rate_lineedit.setValidator(QDoubleValidator(1.000, 999.000, 3))
        self.dialogue.menudialogue_codenumber_linedit.setValidator(QIntValidator(0, 999))
        self.dialogue.menudialogue_newcategory_button.clicked.connect(self.create_category)
        self.dialogue.menudialogue_itemname_linedit.textChanged.connect(
            lambda: self.auto_capital(self.dialogue.menudialogue_itemname_linedit))
        self.id = None
        self.dialogue.menudialogue_serve_lineedit.setValidator(QIntValidator(0, 999))
        if not args:
            self.dialogue.menudialogu_delete_button.setDisabled(True)
            self.dialogue.menudialogu_delete_button.setToolTip("Cannot Delete Uncreated Dish")
            self.dialogue.menudialogue_codenumber_linedit.setPlaceholderText('Not Assigned')
            self.dialogue.menudialogue_menuIngredients_table_addrow_button.setToolTip(
                "Cannot Add ingredients of unsaved Menu")
            self.dialogue.menudialogue_serve_lineedit.setPlaceholderText('No of Servings')
            self.dialogue.menudialogue_menuIngredients_table_addrow_button.setDisabled(True)
            self.dialogue.menudialogue_menuIngredients_table_save_button.setDisabled(True)
        else:
            self.edit_mode(args.text())

    def edit_mode(self, args, load=True):
        """method to allow user to edit the dishes"""
        self.editable = True
        self.setWindowTitle('Edit Dish')
        self.dialogue.menudialogue_add_button.setText('Save')
        self.id = args
        self.dialogue.menudialogue_codenumber_linedit.setText(self.id)
        if load:
            self.update_ingredients()
            self.load_dish()
        else:
            self.dialogue.menudialogue_menuIngredients_table_addrow_button.setDisabled(False)
            self.dialogue.menudialogue_menuIngredients_table_save_button.setDisabled(False)
            self.dialogue.menudialogu_delete_button.setDisabled(False)

    def create_category(self):
        """pops up a new dialogue to create a new category"""
        category = CategoryAddDialogue()
        category.exec_()
        self.complete_category()
        itemfield = self.dialogue.menudialogue_itemcategory_combobox
        settext = category.category.categorydialogue_newcategory_linedit.text()
        index = itemfield.findText(settext)
        itemfield.setCurrentIndex(index)

    def complete_category(self, event=None):
        """
        fills the category in the combobox
        :return:none
        """
        itemfield = self.dialogue.menudialogue_itemcategory_combobox
        itemfield.setStyleSheet("QAbstractItemView{"
                                "background: #4B77BE;"
                                "}")
        itemfield.clear()
        itemfield.addItems(self.search.search_categories())

    def delete_menu_item(self):
        """
        :return: deletes the current item from the menu
        """
        logger.info('MenuAddDialogue delete menu initiated')
        ask = QMessageBox.question(self, "Confirm!!", "The current menu item will be deleted",
                                   QMessageBox.Yes | QMessageBox.No)
        if ask == QMessageBox.Yes:
            todelete = self.menuproduct
            todelete.delete_rows(self.id)
            self.close()
            self.parent.update_menu()

    def popup_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        table = self.dialogue.menudialogue_menuIngredients_table
        model_index = table.indexFromItem(item)
        row = model_index.row()
        item = table.item(row, 0)
        if item:
            self.remove_ingredient_item(table.item(row, 0).text())

    def remove_ingredient_item(self, code):
        """
        removes an ingredient
        :param code: code of the ingredient
        :return:None
        """
        logger.info('MenuAddDialogue remove ingredients initiated')
        code = code
        msg = QMessageBox.critical(self, "Confirm!!", "This will delete the ingredient with code %s" % code,
                                   QMessageBox.Cancel | QMessageBox.Ok)
        if msg == QMessageBox.Ok:
            ingredients = IngredientsInMenu(self.id)
            status = ingredients.remove_ingredient_item(code)
            if status:
                QMessageBox.information(self, "Success!!", "The Ingredient was removed", QMessageBox.Ok)
                self.update_ingredients()
            else:
                QMessageBox.critical(self, "Failure!!", "The Ingredient was not removed",
                                     QMessageBox.Ok)

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def update_ingredients(self):
        """
        updates the ingredients list
        :return:
        """
        ingredients = IngredientsInMenu(self.id)
        ingredientlist = ingredients.load_ingredients()
        if ingredientlist == []:
            self.load_rows(0)
        self.load_rows(*ingredientlist)

    def load_dish(self):
        """
        loads the dish and its values
        :return:none
        """
        dishvalues = self.dish.load_rows(self.id)
        self.dialogue.menudialogue_itemname_linedit.setText(dishvalues['name'])
        combo = self.dialogue.menudialogue_itemcategory_combobox.findText(dishvalues['category'])
        self.dialogue.menudialogue_itemcategory_combobox.setCurrentIndex(combo)
        self.dialogue.menudialogue_rate_lineedit.setText(dishvalues['rate'])
        self.dialogue.menudialogue_serve_lineedit.setText(dishvalues['serve'])


    def load_rows(self, *args):
        """
        :param args:item code
        :return:Loads the rows from the database
        """
        table = self.dialogue.menudialogue_menuIngredients_table
        if args:
            table.clearContents()
            table.setRowCount(0)
            if args[0] != 0:
                table.setRowCount(len(args))
                for i, j in enumerate(args):
                    item = QTableWidgetItem(j['code'])
                    table.setItem(i, 0, item)
                    item = QTableWidgetItem(j['item'])
                    table.setItem(i, 1, item)
                    item = QTableWidgetItem(j['category'])
                    table.setItem(i, 2, item)
                    combo = QComboBox()
                    self.fillunits(combo)
                    index = combo.findText(j['units'])
                    combo.setCurrentIndex(index)
                    table.setCellWidget(i, 3, combo)
                    quantity = QLineEdit(j['quantity'])
                    table.setCellWidget(i, 4, quantity)
        else:
            ###arranges the width each time we call this method
            table.setColumnWidth(1, table.width() / 5)
            table.setColumnWidth(2, table.width() / 5)
            table.setColumnWidth(3, table.width() / 5)

    def add_new_rows(self):
        """
        :return:adds a new row to the table
        """
        table = self.dialogue.menudialogue_menuIngredients_table
        rowcount = table.rowCount() + 1
        table.setRowCount(rowcount)
        edit = QLineEdit()
        edit.editingFinished.connect(lambda: self.get_details_of_code(rowcount))
        table.setCellWidget(rowcount - 1, 0, edit)
        combo = QComboBox()
        self.fillitem(combo)
        combo.currentIndexChanged.connect(lambda: self.get_details_of_item(rowcount))
        table.setCellWidget(rowcount - 1, 1, combo)
        category = QTableWidgetItem()
        table.setItem(rowcount - 1, 2, category)
        units = QComboBox()
        self.fillunits(units)
        table.setCellWidget(rowcount - 1, 3, units)
        quantity = QLineEdit()
        quantity.setValidator(QDoubleValidator(0.000, 999.999, 3))
        table.setCellWidget(rowcount - 1, 4, quantity)

    def fillitem(self, combo):
        """
        gets the item names for ingredients
        :param combo: combobox object
        :return:none
        """
        items = IngredientsInMenu(self.id)
        combo.setStyleSheet("QAbstractItemView{"
                            "background: #4B77BE;"
                            "}")
        combo.addItems(items.get_item())

    def fillunits(self, combo):
        """
        gets the measurement list from tryton
       :param combo: the combobox to be filled
       :return: none
        """
        units = IngredientsInMenu(self.id)
        combo.setStyleSheet("QAbstractItemView{"
                            "background: #4B77BE;"
                            "}")
        combo.addItems(units.get_quantity_uom())

    def get_details_of_code(self, rowcount):
        """
        fills the item, category and units based on the code
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.dialogue.menudialogue_menuIngredients_table
        details = IngredientsInMenu(self.id)
        codeline = table.cellWidget(row, 0)
        data = details.get_details_of_code(codeline.text())
        item = table.cellWidget(row, 1)
        index = item.findText(data['item'])
        item.setCurrentIndex(index)
        category = table.item(row, 2)
        category.setText(data['category'])
        units = table.cellWidget(row, 3)
        index = units.findText(data['units'])
        units.setCurrentIndex(index)


    def get_details_of_item(self, rowcount):
        """
        fills the code, category and units based on the item
        :param rowcount: the row count
        :return: none
        """
        row = rowcount - 1
        table = self.dialogue.menudialogue_menuIngredients_table
        details = IngredientsInMenu(self.id)
        itemcombo = table.cellWidget(row, 1)
        data = details.get_details_of_item(itemcombo.currentText())
        code = table.cellWidget(row, 0)
        code.setText(data['code'])
        category = table.item(row, 2)
        category.setText(data['category'])
        units = table.cellWidget(row, 3)
        index = units.findText(data['units'])
        units.setCurrentIndex(index)

    def add_menu(self):
        """
        adds the new menu item
        :return:none
        """
        logger.info('MenuAddDialogue add new menu initiated')
        name = self.dialogue.menudialogue_itemname_linedit.text()
        rate = self.dialogue.menudialogue_rate_lineedit.text()
        id = self.id if self.id else self.dialogue.menudialogue_codenumber_linedit.text()
        category = self.dialogue.menudialogue_itemcategory_combobox.currentText()
        serve = self.dialogue.menudialogue_serve_lineedit.text()
        obj = {'name': name, 'rate': rate, 'id': id, 'category': category, 'serve': serve}
        for i, j in obj.iteritems():
            if j == '':
                QMessageBox.critical(QMessageBox(), 'Error', 'Invalid %s value' % i.title(), QMessageBox.Ok)
                return False
        if self.editable:
            ret = self.menuproduct.update_dish(obj)
        else:
            ret = self.menuproduct.new_dish(obj)
        if not ret:
            QMessageBox.critical(QMessageBox(), 'Error', 'Duplicate Entry', QMessageBox.Ok)
            return False
        else:
            QMessageBox.information(QMessageBox(), 'Success', 'Dish Saved', QMessageBox.Ok)
            self.edit_mode(id, False)
            self.parent.update_menu()

    def got_focus(self, event):
        """
        just a focus receiving event
        :param event: focus in
        :return:none
        """
        self.load_rows()

    def save_ingredients(self):
        """
        saves the ingredients corresponding to the product
        :return:None
        """
        logger.info('MenuAddDialogue save ingredients initiated')
        data = self.get_data()
        saveingredients = IngredientsInMenu(self.id)
        status = saveingredients.update_ingredients(data)
        if status:
            msg = QMessageBox.information(self, "Success!!", "The ingredients were saved successfully", QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.update_ingredients()

    def get_data(self):
        """
        :return: fetches all the data for printing
        """
        table = self.dialogue.menudialogue_menuIngredients_table
        rows = table.rowCount()
        dataobj = []
        for i in range(rows):
            print "issue"
            dictionary = {}
            item = table.cellWidget(i, 0) if table.cellWidget(i, 0) is not None else table.item(i, 0)
            dictionary['code'] = item.text()
            if dictionary['code'] == '':
                break
            item = table.cellWidget(i, 1).currentText() if table.cellWidget(i, 1) is not None else table.item(i, 1).text()
            dictionary['item'] = item
            item = table.cellWidget(i, 2).currentText() if table.cellWidget(i, 2) is not None else table.item(i, 2).text()
            dictionary['category'] = item
            item = table.cellWidget(i, 3).currentText() if table.cellWidget(i, 3) is not None else table.item(i, 3).text()
            dictionary['units'] = item
            item = table.cellWidget(i, 4) if table.cellWidget(i, 4) is not None else table.item(i, 4)
            dictionary['quantity'] = item.text()
            if dictionary['quantity'] == '':
                self.show_error('Quantity')
                return False
            if dictionary['quantity'] == '0':
                continue
            dataobj.append(dictionary)
        return dataobj

    def show_error(self, text):
        """
        :return: pops up an error
        """
        QMessageBox.critical(QMessageBox(), 'Fail!!!', "Please Enter %s properly" % text, QMessageBox.Ok)


class CategoryAddDialogue(QDialog):
    """popup for category entry"""
    global logger

    def __init__(self):
        logger.info('Inside CategoryAddDialogue')
        QDialog.__init__(self)
        self.category = Ui_new_category()
        self.category.setupUi(self)
        self.newcategory = CategoryOfProduct()
        self.category.categorydialogue_newcategory_linedit.textChanged.connect(
            lambda: self.auto_capital(self.category.categorydialogue_newcategory_linedit))
        self.category.categorydialogue_addcategory_button.clicked.connect(self.add_category)

    def auto_capital(self, linedit):
        """
        :param linedit: the linedit object to be modified
        :return: none
        """
        edit = linedit
        text = edit.text()
        edit.setText(text.title())

    def add_category(self):
        """
        adds a new category to the category types
        :return: none
        """

        status = self.newcategory.create_category(self.category.categorydialogue_newcategory_linedit.text())
        if status:
            QMessageBox.information(self, "Success!!", "The Category was saved", QMessageBox.Ok)
            self.close()
        else:
            QMessageBox.critical(self, "Failure!!", "The Category was not saved, may be duplicate",
                                 QMessageBox.Ok)


class Menu():
    """Menu management main container"""
    def __init__(self):
        ####
        self.menu_tab_4 = QWidget()
        self.menu_tab_4.setStyleSheet("")
        self.menu_tab_4.setObjectName("menu_tab_4")
        self.horizontalLayout_7 = QHBoxLayout(self.menu_tab_4)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.menu_detail_tabWidget = QTabWidget(self.menu_tab_4)
        self.menu_detail_tabWidget.setObjectName("menu_detail_tabWidget")
        self.weeklytabs = None
        self.add_tabs()
        self.horizontalLayout_7.addWidget(self.menu_detail_tabWidget)
        ####signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.menu_detail_tabWidget.currentChanged.connect(self.change_focus)
        self.menu_tab_4.setFocusPolicy(Qt.StrongFocus)
        self.menu_tab_4.focusInEvent = self.change_focus


    def add_tabs(self):
        """
        :return: adds the tab
        """
        menu = MenuDetails()
        self.menu_detail_tabWidget.addTab(menu.menudetail_tab_1, "&Menu")
        self.weeklytabs = {}
        days = [('monday', 'Monday'),
                ('tuesday', 'Tuesday'),
                ('wednesday', 'Wednesday'),
                ('thursday', 'Thursday'),
                ('friday', 'Friday'),
                ('saturday', 'Saturday'),
                ('sunday', 'Sunday')]
        for n, i in enumerate(days):
            menu = MenuWeekday(day=i[0])
            index = n + 1
            self.weeklytabs[index] = menu
            self.menu_detail_tabWidget.addTab(menu.menudetail_tab_1, i[1])

    def change_focus(self, event=None):
        """
        focus event handler
        """
        wid = self.menu_detail_tabWidget.currentWidget()
        if wid.isVisible():
            wid.setFocus()


class MenuDetails():
    """Tab to manage menu entries"""
    global logger

    def __init__(self):
        ####
        logger.info('Inside MenuDetails')
        self.menudetail_tab_1 = QWidget()
        self.menudetail_tab_1.setObjectName("menudetail_tab_1")
        self.gridLayout_20 = QGridLayout(self.menudetail_tab_1)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.menu_table = QTableWidget(self.menudetail_tab_1)
        self.menu_table.setSortingEnabled(True)
        self.menu_table.setObjectName("menu_table")
        self.menu_table.setColumnCount(4)
        self.menu_table.setRowCount(0)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(3, item)
        self.menu_table.horizontalHeader().setCascadingSectionResizes(False)
        self.menu_table.horizontalHeader().setStretchLastSection(True)
        self.menu_table.verticalHeader().setVisible(True)
        self.menu_table.verticalHeader().setCascadingSectionResizes(True)
        self.gridLayout_20.addWidget(self.menu_table, 0, 0, 1, 2)
        spacerItem22 = QSpacerItem(612, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_20.addItem(spacerItem22, 1, 0, 1, 1)
        self.menu_table_add_button = QPushButton(self.menudetail_tab_1)
        self.menu_table_add_button.setObjectName("menu_table_add_button")
        self.gridLayout_20.addWidget(self.menu_table_add_button, 1, 1, 1, 1)
        ####retranslate
        self.menu_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Rate", None, QApplication.UnicodeUTF8))
        self.menu_table_add_button.setText(
            QApplication.translate("MainWindow", "Add New Dish", None, QApplication.UnicodeUTF8))
        # self.menu_table_add_button.setShortcut(
        # QApplication.translate("MainWindow", "Ctrl+E", None, QApplication.UnicodeUTF8))
        ###signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.menu = MenuProduct()
        self.menu_table_add_button.clicked.connect(self.add_menu)
        self.menu_table.itemDoubleClicked.connect(self.popup_edit)
        self.menu_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.menu_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.menu_table.setShowGrid(False)
        self.menu_table.setAlternatingRowColors(True)
        self.update_menu()
        self.popup = object
        self.menudetail_tab_1.setFocusPolicy(Qt.StrongFocus)
        self.menudetail_tab_1.focusInEvent = self.load_rows
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assign shortcuts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_menumgtmenu_view']),
                  self.menudetail_tab_1, self.row_selected)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_menumgtmenu_add']),
                  self.menudetail_tab_1, self.add_menu)

    def row_selected(self):
        """select the rows"""
        rows = sorted(set(index.row() for index in
                          self.menu_table.selectedIndexes()))
        if rows:
            self.add_menu(self.menu_table.item(rows[0], 0))


    def add_menu(self, *args):
        """
        :return: Pops up a new dialogue to add the menus
        """
        if not args:
            self.popup = MenuAddDialogue(parent=self)
            self.popup.exec_()
        else:
            self.popup = MenuAddDialogue(parent=self, args=args[0])
            self.popup.exec_()

    def update_menu(self):
        """
        :return:Populates the menu table
        """
        menulist = self.menu.load_menus()
        if menulist:
            self.add_row(*menulist)
        else:
            self.menu_table.clearContents()
            self.menu_table.setRowCount(0)

    def popup_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        model_index = self.menu_table.indexFromItem(item)
        row = model_index.row()
        self.add_menu(self.menu_table.item(row, 0))

    def add_row(self, *args):
        """add new row entries"""
        table = self.menu_table
        if args:
            table.setRowCount(len(args))
            for i, j in enumerate(args):
                item = QTableWidgetItem(j['item_no'])
                table.setItem(i, 0, item)
                item = QTableWidgetItem(j['item'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(j['category'])
                table.setItem(i, 2, item)
                item = QTableWidgetItem(j['rate'])
                table.setItem(i, 3, item)
        table.setColumnWidth(0, table.width() / 4)
        table.setColumnWidth(1, table.width() / 4)
        table.setColumnWidth(2, table.width() / 4)

    def load_rows(self, event):
        """
        :return:checks and adds new rows
        """
        self.add_row()


class MenuWeekday():
    """Tab to manage menu entry for each day"""
    global logger

    def __init__(self, day):
        ####
        logger.info('Inside MenuWeekday')
        self.menudetail_tab_1 = QWidget()
        self.menudetail_tab_1.setObjectName("menudetail_tab_1")
        self.gridLayout_20 = QGridLayout(self.menudetail_tab_1)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.menu_table = QTableWidget(self.menudetail_tab_1)
        self.menu_table.setSortingEnabled(True)
        self.menu_table.setObjectName("menu_table")
        self.menu_table.setColumnCount(6)
        self.menu_table.setRowCount(0)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.menu_table.setHorizontalHeaderItem(5, item)
        self.menu_table.horizontalHeader().setCascadingSectionResizes(False)
        self.menu_table.horizontalHeader().setStretchLastSection(True)
        self.menu_table.verticalHeader().setVisible(True)
        self.menu_table.verticalHeader().setCascadingSectionResizes(True)
        self.gridLayout_20.addWidget(self.menu_table, 0, 0, 1, 3)
        spacerItem22 = QSpacerItem(612, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_20.addItem(spacerItem22, 1, 0, 1, 1)
        self.menu_table_refresh_button = QPushButton(self.menudetail_tab_1)
        self.menu_table_refresh_button.setObjectName("menu_table_refresh_button")
        self.gridLayout_20.addWidget(self.menu_table_refresh_button, 1, 1, 1, 1)
        self.menu_table_add_button = QPushButton(self.menudetail_tab_1)
        self.menu_table_add_button.setObjectName("menu_table_add_button")
        self.gridLayout_20.addWidget(self.menu_table_add_button, 1, 2, 1, 1)
        ####retranslate
        self.menu_table.horizontalHeaderItem(0).setText(
            QApplication.translate("MainWindow", "Code", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(1).setText(
            QApplication.translate("MainWindow", "Item", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(2).setText(
            QApplication.translate("MainWindow", "Category", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(3).setText(
            QApplication.translate("MainWindow", "Rate", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(4).setText(
            QApplication.translate("MainWindow", "Per Day", None, QApplication.UnicodeUTF8))
        self.menu_table.horizontalHeaderItem(5).setText(
            QApplication.translate("MainWindow", "Available", None, QApplication.UnicodeUTF8))
        self.menu_table_refresh_button.setText(
            QApplication.translate("MainWindow", "Refresh", None, QApplication.UnicodeUTF8))
        self.menu_table_add_button.setText(
            QApplication.translate("MainWindow", "Add Dish", None, QApplication.UnicodeUTF8))
        ###signals and slots && other stuffs
        # self.mainwindow = Ui_MainWindow  # just for the ease of finding the attributes in pycharm
        self.day = day
        self.menu_table_add_button.clicked.connect(self.add_menu)
        self.menu_table.itemDoubleClicked.connect(self.popup_edit)
        self.menu_table_refresh_button.clicked.connect(self.update_menu)
        self.menu_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.menu_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.menu_table.setShowGrid(False)
        self.menu_table.setAlternatingRowColors(True)
        self.update_menu()
        self.popup = object
        self.menudetail_tab_1.setFocusPolicy(Qt.StrongFocus)
        self.menudetail_tab_1.focusInEvent = self.load_rows
        self.assign_shortcuts()

    def assign_shortcuts(self):
        """assign shortcuts"""
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_menumgtmonsun_view']),
                  self.menudetail_tab_1, self.row_selected)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_menumgtmonsun_refresh']),
                  self.menudetail_tab_1, self.update_menu)
        QShortcut(QKeySequence(settings.custom_shortcut['key_tabcon_menumgtmonsun_add']),
                  self.menudetail_tab_1, self.add_menu)

    def row_selected(self):
        """selets a row entry"""
        rows = sorted(set(index.row() for index in
                          self.menu_table.selectedIndexes()))
        if rows:
            code = self.menu_table.item(rows[0], 0).text()
            name = self.menu_table.item(rows[0], 1).text()
            quantity = self.menu_table.item(rows[0], 4).text()
            self.add_menu(code, name, quantity)

    def add_menu(self, *args):
        """
        :return: Pops up a new dialogue to add the menus
        """
        if not args:
            self.popup = AddMenuFromList(parent=self, day=self.day)
            self.popup.exec_()
        else:
            self.popup = MenuQuantityEditPopup(parent=self, day=self.day, code=args[0], name=args[1], quantity=args[2])
            self.popup.exec_()

    def update_menu(self):
        """
        :return:Populates the menu table
        """
        menu = WeeklyMenu(day=self.day)
        menulist = menu.load_dish_per_Day()
        if not menulist == []:
            self.add_row(*menulist)
        else:
            self.menu_table.clearContents()
            self.menu_table.setRowCount(0)

    def popup_edit(self, item):
        """
        Pops up the menu to be edited
        :param item: item clicked
        :return:none
        """
        model_index = self.menu_table.indexFromItem(item)
        row = model_index.row()
        code = self.menu_table.item(row, 0).text()
        name = self.menu_table.item(row, 1).text()
        quantity = self.menu_table.item(row, 4).text()
        self.add_menu(code, name, quantity)

    def add_row(self, *args):
        """creates a new row entry"""
        table = self.menu_table
        if args:
            table.setRowCount(len(args))
            for i, j in enumerate(args):
                item = QTableWidgetItem(j['item_no'])
                table.setItem(i, 0, item)
                item = QTableWidgetItem(j['item'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(j['category'])
                table.setItem(i, 2, item)
                item = QTableWidgetItem(j['rate'])
                table.setItem(i, 3, item)
                item = QTableWidgetItem(j['per_day'])
                table.setItem(i, 4, item)
                item = QTableWidgetItem(j['available'])
                table.setItem(i, 5, item)
        table.setColumnWidth(0, table.width() / 6)
        table.setColumnWidth(1, table.width() / 6)
        table.setColumnWidth(2, table.width() / 6)
        table.setColumnWidth(3, table.width() / 6)
        table.setColumnWidth(4, table.width() / 6)

    def load_rows(self, event):
        """
        :return:checks and adds new rows
        """
        self.add_row()


class MenuQuantityEditPopup(QDialog):
    """popup to manage menu entry for each day"""
    global logger

    def __init__(self, parent=None, code=None, name=None, day=None, quantity=None):
        logger.info('Inside MenuQuantityEditPopup')
        QDialog.__init__(self)
        self.today = Ui_menu_this_day()
        self.today.setupUi(self)
        self.parent = parent
        self.today.menuperday_quantity_linedit.setValidator(QIntValidator(0, 99999))
        self.today.menuperday_save_button.clicked.connect(self.update_weeklydata)
        self.today.menuperday_delete_button.clicked.connect(self.remove_from_weeklymenu)
        if code:
            self.code = code
            self.name = name
            self.day = day
            self.quantity = quantity
            self.today.menuperday_code_label.setText(self.code)
            self.today.menuperday_name_label.setText(self.name)
            self.today.menuperday_quantity_linedit.setText(self.quantity)
            self.week = WeeklyMenu(code=self.code, name=self.name, day=self.day, quantity=self.quantity)

    def update_weeklydata(self):
        """
        updates the value of the per day quantity of a dish
        :return: none
        """
        logger.info('MenuQuantityEditPopup updating weeklydata initiated')
        self.week.quantity = int(self.today.menuperday_quantity_linedit.text())
        state = self.week.update_weekly_row()
        if state:
            QMessageBox.information(self, "Success!!", "The quantity was saved", QMessageBox.Ok)
            self.parent.update_menu()
            self.close()
        else:
            QMessageBox.critical(self, 'Fail!!', 'The quantity was not saved!!', QMessageBox.Ok)

    def remove_from_weeklymenu(self):
        """
        deletes the entry
        :return:
        """
        logger.info('MenuQuantityEditPopup remove from weeklymenu initiated')
        msg = QMessageBox.critical(self, "Confirm?", "This will delete the entry in the %s table" % self.day,
                                   QMessageBox.Cancel | QMessageBox.Ok)
        if msg == QMessageBox.Ok:
            status = self.week.remove_weekly_row()
            if status:
                msg = QMessageBox.information(self, "Success!!", "The Dish was deleted successfully", QMessageBox.Ok)
                if msg == QMessageBox.Ok:
                    self.parent.update_menu()
                    self.close()


class AddMenuFromList(QDialog):
    """popup to add menu to the per day menu tab"""
    global logger

    def __init__(self, parent=None, day=None):
        logger.info('Inside AddMenuFromList')
        QDialog.__init__(self)
        self.addeachweek = Ui_add_menu_eachweek()
        self.addeachweek.setupUi(self)
        self.addeachweek.add_eachweek_table.horizontalHeader().sectionClicked.connect(self.select_all_rows)
        self.addeachweek.add_eachweek_add_button.clicked.connect(self.addmenu_this_day)
        self.parent = parent
        self.day = day
        self.setFocusPolicy(Qt.StrongFocus)
        self.focusInEvent = self.load_rows
        self.week = WeeklyMenu(day=self.day)
        menulist = self.week.load_dish_notin_per_Day()
        self.add_row(*menulist)

    def select_all_rows(self, item):
        """
        selects all rows in the 0th column
        :param item: column number
        :return:none
        """
        if item == 0:
            r = self.addeachweek.add_eachweek_table.rowCount()
            for i in range(r):
                chekbox = self.addeachweek.add_eachweek_table.cellWidget(i, item)
                if not chekbox.isChecked():
                    chekbox.setCheckState(Qt.Checked)
                else:
                    chekbox.setCheckState(Qt.Unchecked)

    def addmenu_this_day(self):
        """
        add the rows to the current day
        :return:none
        """
        logger.info('AddMenuFromList adding menu to this day initiated')
        data = []
        table = self.addeachweek.add_eachweek_table
        r = table.rowCount()
        for i in range(r):
            rows = {}
            checkbox = table.cellWidget(i, 0)
            if checkbox.isChecked():
                rows['code'] = table.item(i, 1).text()
                rows['day'] = self.day
                rows['quantity'] = table.cellWidget(i, 5).text()
                rows['model_item'] = table.item(i, 1)
                data.append(rows)
        status = self.week.save_dish_per_day(data)
        if status:
            message = QMessageBox.information(self, 'Success!', "The menu Items were added", QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.parent.update_menu()
                for i in data:
                    model_index = table.indexFromItem(i['model_item'])
                    row = model_index.row()
                    table.removeRow(row)
                self.close()
        else:
            QMessageBox.critical(self, 'Fail!!', 'The menu Item was not saved!!', QMessageBox.Ok)

    def add_row(self, *args):
        """adds a new row entry"""
        table = self.addeachweek.add_eachweek_table
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setShowGrid(False)
        table.setAlternatingRowColors(True)
        table.setStyleSheet("color:#000000;")
        if args:
            table.setRowCount(len(args))
            for i, j in enumerate(args):
                checkbox = QCheckBox()
                table.setCellWidget(i, 0, checkbox)
                item = QTableWidgetItem(j['item_no'])
                table.setItem(i, 1, item)
                item = QTableWidgetItem(j['item'])
                table.setItem(i, 2, item)
                item = QTableWidgetItem(j['category'])
                table.setItem(i, 3, item)
                item = QTableWidgetItem(j['rate'])
                table.setItem(i, 4, item)
                quantity = QLineEdit()
                quantity.setValidator(QIntValidator(0, 99999))
                table.setCellWidget(i, 5, quantity)
        table.setColumnWidth(0, table.width() / 9)
        table.setColumnWidth(1, table.width() / 5)
        table.setColumnWidth(2, table.width() / 5)
        table.setColumnWidth(3, table.width() / 5)
        table.setColumnWidth(4, table.width() / 5)

    def load_rows(self, event):
        """checks and adds new rows"""
        self.add_row()