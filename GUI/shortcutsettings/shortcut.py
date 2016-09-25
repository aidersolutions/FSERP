#! /usr/bin/env python

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from PySide.QtGui import QTreeWidget, QTreeWidgetItem, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from PySide.QtCore import Qt
from customline.customline import CustomLine


class NewTreeWidget(QTreeWidget):
    def showEvent(self, event):
        width = self.header().width()
        self.header().resizeSection(0, width / 1.2)
        super(NewTreeWidget, self).showEvent(event)


class NewShortcut():
    def __init__(self):
        self.shortcut_setting = QWidget()
        vlayout = QVBoxLayout(self.shortcut_setting)

        self.globaltree = NewTreeWidget()
        self.globaltree.setObjectName('shortcut_tree')
        self.globaltree.setHeaderLabels(['Function Name', 'Shortcut'])
        self.root_set()
        self.tabs_set()
        self.tabscontrol_set()
        self.key_resetdefault_button = QPushButton('Reset Default')
        self.key_apply_button = QPushButton('Apply')
        tophlaout = QHBoxLayout()
        label = QLabel('Search')
        self.search_line = QLineEdit()
        tophlaout.addWidget(label)
        tophlaout.addWidget(self.search_line)
        tophlaout.insertStretch(-1)
        vlayout.addLayout(tophlaout)
        vlayout.addWidget(self.globaltree)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.key_resetdefault_button)
        hlayout.addWidget(self.key_apply_button)
        hlayout.insertStretch(0)
        hlayout.insertStretch(-1)
        vlayout.addLayout(hlayout)
        self.search_line.textChanged.connect(lambda: self.search_shorcut(self.search_line.text()))
        # self.key_apply_button.clicked.connect(self.search_short)

    def search_shorcut(self, text):
        self.globaltree.collapseAll()
        data = self.globaltree.findItems(text, Qt.MatchContains | Qt.MatchRecursive)
        for i in data:
            self.globaltree.scrollToItem(i)

    def search_short(self):  # waste not used
        self.globaltree.collapseAll()
        self.custom_box = []
        data = self.get_all_items(self.globaltree)
        for i in self.custom_box:
            print i.text(), i.objectName()

    def get_subtree_nodes(self, tree_widget_item):  # waste not used
        """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
        nodes = []
        nodes.append(tree_widget_item)
        for i in range(tree_widget_item.childCount()):
            nodes.extend(self.get_subtree_nodes(tree_widget_item.child(i)))
        if not tree_widget_item.childCount():
            self.custom_box.append(self.globaltree.itemWidget(tree_widget_item, 1))
        return nodes

    def get_all_items(self, tree_widget):  # waste not used
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
        self.all_items = []
        for i in range(tree_widget.topLevelItemCount()):
            top_item = tree_widget.topLevelItem(i)
            self.all_items.extend(self.get_subtree_nodes(top_item))
        return self.all_items

    def root_set(self):
        """creates a treee set entry for a particular tab to set a shortcut"""
        global_root = QTreeWidgetItem(self.globaltree, ["Global"])
        first_row = QTreeWidgetItem(global_root, ['Quit'])
        self.key_global_quit = CustomLine(self.globaltree)
        self.key_global_quit.setObjectName('key_global_quit')
        self.globaltree.setItemWidget(first_row, 1, self.key_global_quit)


    def tabs_set(self):
        """creates a treee set entry for a particular tab to set a shortcut"""
        tabs_root = QTreeWidgetItem(self.globaltree, ["Tabs"])

        first_row = QTreeWidgetItem(tabs_root, ['Inventory'])
        self.key_tabs_inventory = CustomLine(self.globaltree)
        self.key_tabs_inventory.setObjectName('key_tabs_inventory')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabs_inventory)

        second_row = QTreeWidgetItem(tabs_root, ['Billing'])
        self.key_tabs_billing = CustomLine(self.globaltree)
        self.key_tabs_billing.setObjectName('key_tabs_billing')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabs_billing)

        third_row = QTreeWidgetItem(tabs_root, ['Menu'])
        self.key_tabs_menu = CustomLine(self.globaltree)
        self.key_tabs_menu.setObjectName('key_tabs_menu')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabs_menu)

        fourth_row = QTreeWidgetItem(tabs_root, ['Employee'])
        self.key_tabs_employee = CustomLine(self.globaltree)
        self.key_tabs_employee.setObjectName('key_tabs_employee')
        self.globaltree.setItemWidget(fourth_row, 1, self.key_tabs_employee)

        fifth_row = QTreeWidgetItem(tabs_root, ['Report'])
        self.key_tabs_report = CustomLine(self.globaltree)
        self.key_tabs_report.setObjectName('key_tabs_report')
        self.globaltree.setItemWidget(fifth_row, 1, self.key_tabs_report)

        sixth_row = QTreeWidgetItem(tabs_root, ['Waste'])
        self.key_tabs_waste = CustomLine(self.globaltree)
        self.key_tabs_waste.setObjectName('key_tabs_waste')
        self.globaltree.setItemWidget(sixth_row, 1, self.key_tabs_waste)

    def tabscontrol_set(self):
        """creates a treee set entry for a particular tab to set a shortcut"""
        tabscontrol_root = QTreeWidgetItem(self.globaltree, ["Tabs Control"])
        self.inventorytab_set(parent=tabscontrol_root)
        self.billingtab_set(parent=tabscontrol_root)
        self.employeetab_set(parent=tabscontrol_root)
        self.menutab_set(parent=tabscontrol_root)


    def inventorytab_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        inventory_tab = QTreeWidgetItem(parent, ["Inventory"])
        self.inventorytab_stock_set(parent=inventory_tab)
        self.inventorytab_add_set(parent=inventory_tab)
        self.inventorytab_release_set(parent=inventory_tab)
        self.inventorytab_purchase_set(parent=inventory_tab)
        self.inventorytab_supplier_set(parent=inventory_tab)
        self.inventorytab_item_set(parent=inventory_tab)

    def inventorytab_stock_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        stock_tab = QTreeWidgetItem(parent, ["Stock"])
        self.inventorytab_stock = CustomLine(self.globaltree)
        self.inventorytab_stock.setObjectName('inventorytab_stock')
        self.globaltree.setItemWidget(stock_tab, 1, self.inventorytab_stock)

        first_row = QTreeWidgetItem(stock_tab, ['Refresh'])
        self.key_tabcon_inventorystock_refresh = CustomLine(self.globaltree)
        self.key_tabcon_inventorystock_refresh.setObjectName('key_tabcon_inventorystock_refresh')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_inventorystock_refresh)

        second_row = QTreeWidgetItem(stock_tab, ['Print'])
        self.key_tabcon_inventorystock_print = CustomLine(self.globaltree)
        self.key_tabcon_inventorystock_print.setObjectName('key_tabcon_inventorystock_print')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_inventorystock_print)

    def inventorytab_add_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        add_tab = QTreeWidgetItem(parent, ["Add"])
        self.inventorytab_add = CustomLine(self.globaltree)
        self.inventorytab_add.setObjectName('inventorytab_add')
        self.globaltree.setItemWidget(add_tab, 1, self.inventorytab_add)

        first_row = QTreeWidgetItem(add_tab, ['Search'])
        self.key_tabcon_inventoryadd_search = CustomLine(self.globaltree)
        self.key_tabcon_inventoryadd_search.setObjectName('key_tabcon_inventoryadd_search')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_inventoryadd_search)

        second_row = QTreeWidgetItem(add_tab, ['Insert New Row'])
        self.key_tabcon_inventoryadd_newrow = CustomLine(self.globaltree)
        self.key_tabcon_inventoryadd_newrow.setObjectName('key_tabcon_inventoryadd_newrow')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_inventoryadd_newrow)

        third_row = QTreeWidgetItem(add_tab, ['Add Stock'])
        self.key_tabcon_inventoryadd_addstock = CustomLine(self.globaltree)
        self.key_tabcon_inventoryadd_addstock.setObjectName('key_tabcon_inventoryadd_addstock')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabcon_inventoryadd_addstock)


    def inventorytab_release_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        release_tab = QTreeWidgetItem(parent, ["Release"])
        self.inventorytab_release = CustomLine(self.globaltree)
        self.inventorytab_release.setObjectName('inventorytab_release')
        self.globaltree.setItemWidget(release_tab, 1, self.inventorytab_release)

        first_row = QTreeWidgetItem(release_tab, ["Today\'s Release"])
        self.key_tabcon_inventoryrelease_todaysrelease = CustomLine(self.globaltree)
        self.key_tabcon_inventoryrelease_todaysrelease.setObjectName('key_tabcon_inventoryrelease_todaysrelease')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_inventoryrelease_todaysrelease)

        second_row = QTreeWidgetItem(release_tab, ['New Row'])
        self.key_tabcon_inventoryrelease_newrow = CustomLine(self.globaltree)
        self.key_tabcon_inventoryrelease_newrow.setObjectName('key_tabcon_inventoryrelease_newrow')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_inventoryrelease_newrow)

        third_row = QTreeWidgetItem(release_tab, ['Release'])
        self.key_tabcon_inventoryrelease_release = CustomLine(self.globaltree)
        self.key_tabcon_inventoryrelease_release.setObjectName('key_tabcon_inventoryrelease_release')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabcon_inventoryrelease_release)

        fourth_row = QTreeWidgetItem(release_tab, ['Add New Row'])
        self.key_tabcon_inventoryrelease_addnewrow = CustomLine(self.globaltree)
        self.key_tabcon_inventoryrelease_addnewrow.setObjectName('key_tabcon_inventoryrelease_addnewrow')
        self.globaltree.setItemWidget(fourth_row, 1, self.key_tabcon_inventoryrelease_addnewrow)

        fifth_row = QTreeWidgetItem(release_tab, ['Discard'])
        self.key_tabcon_inventoryrelease_discard = CustomLine(self.globaltree)
        self.key_tabcon_inventoryrelease_discard.setObjectName('key_tabcon_inventoryrelease_discard')
        self.globaltree.setItemWidget(fifth_row, 1, self.key_tabcon_inventoryrelease_discard)

    def inventorytab_purchase_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        purchase_tab = QTreeWidgetItem(parent, ["Purchase Schedule"])
        self.inventorytab_purchase = CustomLine(self.globaltree)
        self.inventorytab_purchase.setObjectName('inventorytab_purchase')
        self.globaltree.setItemWidget(purchase_tab, 1, self.inventorytab_purchase)

        first_row = QTreeWidgetItem(purchase_tab, ["Search"])
        self.key_tabcon_inventorypurchase_search = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_search.setObjectName('key_tabcon_inventorypurchase_search')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_inventorypurchase_search)

        second_row = QTreeWidgetItem(purchase_tab, ['Add Item'])
        self.key_tabcon_inventorypurchase_additem = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_additem.setObjectName('key_tabcon_inventorypurchase_additem')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_inventorypurchase_additem)

        third_row = QTreeWidgetItem(purchase_tab, ['Print'])
        self.key_tabcon_inventorypurchase_print = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_print.setObjectName('key_tabcon_inventorypurchase_print')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabcon_inventorypurchase_print)

        fourth_row = QTreeWidgetItem(purchase_tab, ['Today'])
        self.key_tabcon_inventorypurchase_today = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_today.setObjectName('key_tabcon_inventorypurchase_today')
        self.globaltree.setItemWidget(fourth_row, 1, self.key_tabcon_inventorypurchase_today)

        fifth_row = QTreeWidgetItem(purchase_tab, ['Tommorow'])
        self.key_tabcon_inventorypurchase_tommorow = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_tommorow.setObjectName('key_tabcon_inventorypurchase_tommorow')
        self.globaltree.setItemWidget(fifth_row, 1, self.key_tabcon_inventorypurchase_tommorow)

        sixth_row = QTreeWidgetItem(purchase_tab, ['This Month'])
        self.key_tabcon_inventorypurchase_thismonth = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_thismonth.setObjectName('key_tabcon_inventorypurchase_thismonth')
        self.globaltree.setItemWidget(sixth_row, 1, self.key_tabcon_inventorypurchase_thismonth)

        seventh_row = QTreeWidgetItem(purchase_tab, ['This Week'])
        self.key_tabcon_inventorypurchase_thisweek = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_thisweek.setObjectName('key_tabcon_inventorypurchase_thisweek')
        self.globaltree.setItemWidget(seventh_row, 1, self.key_tabcon_inventorypurchase_thisweek)

        eighth_row = QTreeWidgetItem(purchase_tab, ['Clear'])
        self.key_tabcon_inventorypurchase_clear = CustomLine(self.globaltree)
        self.key_tabcon_inventorypurchase_clear.setObjectName('key_tabcon_inventorypurchase_clear')
        self.globaltree.setItemWidget(eighth_row, 1, self.key_tabcon_inventorypurchase_clear)

    def inventorytab_supplier_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        stock_tab = QTreeWidgetItem(parent, ["Supplier"])
        self.inventorytab_supplier = CustomLine(self.globaltree)
        self.inventorytab_supplier.setObjectName('inventorytab_supplier')
        self.globaltree.setItemWidget(stock_tab, 1, self.inventorytab_supplier)

        first_row = QTreeWidgetItem(stock_tab, ['Add'])
        self.key_tabcon_inventorysupplier_add = CustomLine(self.globaltree)
        self.key_tabcon_inventorysupplier_add.setObjectName('key_tabcon_inventorysupplier_add')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_inventorysupplier_add)

        second_row = QTreeWidgetItem(stock_tab, ['View'])
        self.key_tabcon_inventorysupplier_view = CustomLine(self.globaltree)
        self.key_tabcon_inventorysupplier_view.setObjectName('key_tabcon_inventorysupplier_view')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_inventorysupplier_view)

    def inventorytab_item_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        item_tab = QTreeWidgetItem(parent, ["Item"])
        self.inventorytab_item = CustomLine(self.globaltree)
        self.inventorytab_item.setObjectName('inventorytab_item')
        self.globaltree.setItemWidget(item_tab, 1, self.inventorytab_item)

        first_row = QTreeWidgetItem(item_tab, ['Add New Item'])
        self.key_tabcon_inventoryitem_addnewitem = CustomLine(self.globaltree)
        self.key_tabcon_inventoryitem_addnewitem.setObjectName('key_tabcon_inventoryitem_addnewitem')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_inventoryitem_addnewitem)

        second_row = QTreeWidgetItem(item_tab, ['View'])
        self.key_tabcon_inventoryitem_view = CustomLine(self.globaltree)
        self.key_tabcon_inventoryitem_view.setObjectName('key_tabcon_inventoryitem_view')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_inventoryitem_view)

    def billingtab_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        billing_tab = QTreeWidgetItem(parent, ["Billing"])
        self.billingtab_bills_set(parent=billing_tab)
        self.billingtab_editbills_set(parent=billing_tab)

    def billingtab_bills_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        bills_tab = QTreeWidgetItem(parent, ["Bills"])

        first_row = QTreeWidgetItem(bills_tab, ['New Bill'])
        self.key_tabcon_billingbills_newbill = CustomLine(self.globaltree)
        self.key_tabcon_billingbills_newbill.setObjectName('key_tabcon_billingbills_newbill')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_billingbills_newbill)

        second_row = QTreeWidgetItem(bills_tab, ['Reset'])
        self.key_tabcon_billingbills_reset = CustomLine(self.globaltree)
        self.key_tabcon_billingbills_reset.setObjectName('key_tabcon_billingbills_reset')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_billingbills_reset)

        third_row = QTreeWidgetItem(bills_tab, ['Search'])
        self.key_tabcon_billingbills_search = CustomLine(self.globaltree)
        self.key_tabcon_billingbills_search.setObjectName('key_tabcon_billingbills_search')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabcon_billingbills_search)

        fourth_row = QTreeWidgetItem(bills_tab, ['Select Bill'])
        self.key_tabcon_billingbills_selectbill = CustomLine(self.globaltree)
        self.key_tabcon_billingbills_selectbill.setObjectName('key_tabcon_billingbills_selectbill')
        self.globaltree.setItemWidget(fourth_row, 1, self.key_tabcon_billingbills_selectbill)

        fifth_row = QTreeWidgetItem(bills_tab, ["Show Credits"])
        self.key_tabcon_billingbills_showcredit = CustomLine(self.globaltree)
        self.key_tabcon_billingbills_showcredit.setObjectName('key_tabcon_billingbills_showcredit')
        self.globaltree.setItemWidget(fifth_row, 1, self.key_tabcon_billingbills_showcredit)

        sixth_row = QTreeWidgetItem(bills_tab, ["Show Customers"])
        self.key_tabcon_billingbills_showcustomer = CustomLine(self.globaltree)
        self.key_tabcon_billingbills_showcustomer.setObjectName('key_tabcon_billingbills_showcustomer')
        self.globaltree.setItemWidget(sixth_row, 1, self.key_tabcon_billingbills_showcustomer)

    def billingtab_editbills_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        edit_tab = QTreeWidgetItem(parent, ["Edit Bills"])

        first_row = QTreeWidgetItem(edit_tab, ['Pay'])
        self.key_tabcon_billingedit_pay = CustomLine(self.globaltree)
        self.key_tabcon_billingedit_pay.setObjectName('key_tabcon_billingedit_pay')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_billingedit_pay)

        second_row = QTreeWidgetItem(edit_tab, ['Save'])
        self.key_tabcon_billingedit_save = CustomLine(self.globaltree)
        self.key_tabcon_billingedit_save.setObjectName('key_tabcon_billingedit_save')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_billingedit_save)

        third_row = QTreeWidgetItem(edit_tab, ['Print'])
        self.key_tabcon_billingedit_print = CustomLine(self.globaltree)
        self.key_tabcon_billingedit_print.setObjectName('key_tabcon_billingedit_print')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabcon_billingedit_print)

    def employeetab_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        employeemgt_tab = QTreeWidgetItem(parent, ["Employee"])
        self.employeetab_employee_set(parent=employeemgt_tab)
        self.employeetab_attendance_set(parent=employeemgt_tab)
        self.employeetab_payroll_set(parent=employeemgt_tab)
        self.employeetab_shift_set(parent=employeemgt_tab)
        self.employeetab_salsettings_set(parent=employeemgt_tab)


    def employeetab_employee_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        employee_tab = QTreeWidgetItem(parent, ["Employee"])
        self.employeetab_employee = CustomLine(self.globaltree)
        self.employeetab_employee.setObjectName('employeetab_employee')
        self.globaltree.setItemWidget(employee_tab, 1, self.employeetab_employee)

        first_row = QTreeWidgetItem(employee_tab, ['Add'])
        self.key_tabcon_empmgtemployee_add = CustomLine(self.globaltree)
        self.key_tabcon_empmgtemployee_add.setObjectName('key_tabcon_empmgtemployee_add')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_empmgtemployee_add)

        second_row = QTreeWidgetItem(employee_tab, ['View'])
        self.key_tabcon_empmgtemployee_view = CustomLine(self.globaltree)
        self.key_tabcon_empmgtemployee_view.setObjectName('key_tabcon_empmgtemployee_view')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_empmgtemployee_view)

    def employeetab_attendance_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        attendance_tab = QTreeWidgetItem(parent, ["Attendance"])
        self.employeetab_attendance = CustomLine(self.globaltree)
        self.employeetab_attendance.setObjectName('employeetab_attendance')
        self.globaltree.setItemWidget(attendance_tab, 1, self.employeetab_attendance)

        first_row = QTreeWidgetItem(attendance_tab, ['Search'])
        self.key_tabcon_empmgtattendence_search = CustomLine(self.globaltree)
        self.key_tabcon_empmgtattendence_search.setObjectName('key_tabcon_empmgtattendence_search')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_empmgtattendence_search)

        second_row = QTreeWidgetItem(attendance_tab, ['Create Attendance'])
        self.key_tabcon_empmgtattendence_create = CustomLine(self.globaltree)
        self.key_tabcon_empmgtattendence_create.setObjectName('key_tabcon_empmgtattendence_create')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_empmgtattendence_create)

        third_row = QTreeWidgetItem(attendance_tab, ['Save'])
        self.key_tabcon_empmgtattendence_save = CustomLine(self.globaltree)
        self.key_tabcon_empmgtattendence_save.setObjectName('key_tabcon_empmgtattendence_save')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabcon_empmgtattendence_save)

    def employeetab_payroll_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        payroll_tab = QTreeWidgetItem(parent, ["Payroll"])
        self.employeetab_payroll = CustomLine(self.globaltree)
        self.employeetab_payroll.setObjectName('employeetab_payroll')
        self.globaltree.setItemWidget(payroll_tab, 1, self.employeetab_payroll)

        first_row = QTreeWidgetItem(payroll_tab, ['Search'])
        self.key_tabcon_empmgtpayroll_search = CustomLine(self.globaltree)
        self.key_tabcon_empmgtpayroll_search.setObjectName('key_tabcon_empmgtpayroll_search')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_empmgtpayroll_search)

        second_row = QTreeWidgetItem(payroll_tab, ['Save'])
        self.key_tabcon_empmgtpayroll_save = CustomLine(self.globaltree)
        self.key_tabcon_empmgtpayroll_save.setObjectName('key_tabcon_empmgtpayroll_save')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_empmgtpayroll_save)

    def employeetab_shift_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        shift_tab = QTreeWidgetItem(parent, ["Shift"])
        self.employeetab_shift = CustomLine(self.globaltree)
        self.employeetab_shift.setObjectName('employeetab_shift')
        self.globaltree.setItemWidget(shift_tab, 1, self.employeetab_shift)

        first_row = QTreeWidgetItem(shift_tab, ['View'])
        self.key_tabcon_empmgtshift_view = CustomLine(self.globaltree)
        self.key_tabcon_empmgtshift_view.setObjectName('key_tabcon_empmgtshift_view')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_empmgtshift_view)

        second_row = QTreeWidgetItem(shift_tab, ['Add Shift'])
        self.key_tabcon_empmgtshift_add = CustomLine(self.globaltree)
        self.key_tabcon_empmgtshift_add.setObjectName('key_tabcon_empmgtshift_add')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_empmgtshift_add)

    def employeetab_salsettings_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        employee_tab = QTreeWidgetItem(parent, ["Salary Settings"])
        self.employeetab_salsettings = CustomLine(self.globaltree)
        self.employeetab_salsettings.setObjectName('employeetab_salsettings')
        self.globaltree.setItemWidget(employee_tab, 1, self.employeetab_salsettings)

        first_row = QTreeWidgetItem(employee_tab, ['View'])
        self.key_tabcon_empmgtsal_view = CustomLine(self.globaltree)
        self.key_tabcon_empmgtsal_view.setObjectName('key_tabcon_empmgtsal_view')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_empmgtsal_view)

        second_row = QTreeWidgetItem(employee_tab, ['New Salary Settings'])
        self.key_tabcon_empmgtsal_new = CustomLine(self.globaltree)
        self.key_tabcon_empmgtsal_new.setObjectName('key_tabcon_empmgtsal_new')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_empmgtsal_new)

    def menutab_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        menumgt_tab = QTreeWidgetItem(parent, ["Menu Management"])
        self.menutab_menu_set(parent=menumgt_tab)
        self.menutab_monsun_set(parent=menumgt_tab)

    def menutab_menu_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        menu_tab = QTreeWidgetItem(parent, ["Menu"])

        first_row = QTreeWidgetItem(menu_tab, ['View'])
        self.key_tabcon_menumgtmenu_view = CustomLine(self.globaltree)
        self.key_tabcon_menumgtmenu_view.setObjectName('key_tabcon_menumgtmenu_view')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_menumgtmenu_view)

        second_row = QTreeWidgetItem(menu_tab, ['Add New Dish'])
        self.key_tabcon_menumgtmenu_add = CustomLine(self.globaltree)
        self.key_tabcon_menumgtmenu_add.setObjectName('key_tabcon_menumgtmenu_add')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_menumgtmenu_add)

    def menutab_monsun_set(self, parent):
        """creates a treee set entry for a particular tab to set a shortcut"""
        monsun_tab = QTreeWidgetItem(parent, ["MON-SUN"])

        first_row = QTreeWidgetItem(monsun_tab, ['View'])
        self.key_tabcon_menumgtmonsun_view = CustomLine(self.globaltree)
        self.key_tabcon_menumgtmonsun_view.setObjectName('key_tabcon_menumgtmonsun_view')
        self.globaltree.setItemWidget(first_row, 1, self.key_tabcon_menumgtmonsun_view)

        second_row = QTreeWidgetItem(monsun_tab, ['Refresh'])
        self.key_tabcon_menumgtmonsun_refresh = CustomLine(self.globaltree)
        self.key_tabcon_menumgtmonsun_refresh.setObjectName('key_tabcon_menumgtmonsun_refresh')
        self.globaltree.setItemWidget(second_row, 1, self.key_tabcon_menumgtmonsun_refresh)

        third_row = QTreeWidgetItem(monsun_tab, ['Add New Dish'])
        self.key_tabcon_menumgtmonsun_add = CustomLine(self.globaltree)
        self.key_tabcon_menumgtmonsun_add.setObjectName('key_tabcon_menumgtmonsun_add')
        self.globaltree.setItemWidget(third_row, 1, self.key_tabcon_menumgtmonsun_add)