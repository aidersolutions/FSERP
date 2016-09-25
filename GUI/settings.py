#! /usr/bin/env python

""" Shortcut settings"""

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

import cPickle
import logging

level = object
access = object
available_check = True
company = 'ERP'

default_shortcut = {
    'key_global_quit': 'Ctrl+Alt+Q',
    'key_tabs_inventory': 'Ctrl+Alt+I',
    'key_tabs_billing': 'Ctrl+Alt+B',
    'key_tabs_menu': 'Ctrl+Alt+M',
    'key_tabs_employee': 'Ctrl+Alt+E',
    'key_tabs_report': 'Ctrl+Alt+R',
    'key_tabs_waste': 'Ctrl+Alt+W',
    'inventorytab_stock': 'Shift+Alt+S',
    'key_tabcon_inventorystock_refresh': 'Ctrl+Shift+R',
    'key_tabcon_inventorystock_print': 'Ctrl+Shift+P',
    'inventorytab_add': 'Shift+Alt+A',
    'key_tabcon_inventoryadd_search': 'Ctrl+Shift+R',
    'key_tabcon_inventoryadd_newrow': 'Ctrl+Shift+N',
    'key_tabcon_inventoryadd_addstock': 'Ctrl+Shift+A',
    'inventorytab_release': 'Shift+Alt+R',
    'key_tabcon_inventoryrelease_todaysrelease': 'Ctrl+Shift+T',
    'key_tabcon_inventoryrelease_newrow': 'Ctrl+Shift+N',
    'key_tabcon_inventoryrelease_release': 'Ctrl+Shift+R',
    'key_tabcon_inventoryrelease_addnewrow': 'Ctrl+Shift+A',
    'key_tabcon_inventoryrelease_discard': 'Ctrl+Shift+D',
    'inventorytab_purchase': 'Shift+Alt+P',
    'key_tabcon_inventorypurchase_search': 'Ctrl+Shift+S',
    'key_tabcon_inventorypurchase_additem': 'Ctrl+Shift+A',
    'key_tabcon_inventorypurchase_print': 'Ctrl+Shift+P',
    'key_tabcon_inventorypurchase_today': 'Ctrl+Shift+T',
    'key_tabcon_inventorypurchase_tommorow': 'Ctrl+Shift+O',
    'key_tabcon_inventorypurchase_thismonth': 'Ctrl+Shift+I',
    'key_tabcon_inventorypurchase_thisweek': 'Ctrl+Shift+W',
    'key_tabcon_inventorypurchase_clear': 'Ctrl+Shift+C',
    'inventorytab_supplier': 'Shift+Alt+S',
    'key_tabcon_inventorysupplier_add': 'Ctrl+Shift+A',
    'key_tabcon_inventorysupplier_view': 'Ctrl+Shift+V',
    'inventorytab_item': 'Shift+Alt+I',
    'key_tabcon_inventoryitem_addnewitem': 'Ctrl+Shift+A',
    'key_tabcon_inventoryitem_view': 'Ctrl+Shift+V',
    'key_tabcon_billingbills_newbill': 'Ctrl+Shift+N',
    'key_tabcon_billingbills_reset': 'Ctrl+Shift+R',
    'key_tabcon_billingbills_search': 'Ctrl+Shift+S',
    'key_tabcon_billingbills_selectbill': 'Ctrl+Shift+O',
    'key_tabcon_billingbills_showcredit': 'Ctrl+Shift+D',
    'key_tabcon_billingbills_showcustomer': 'Ctrl+Shift+C',
    'key_tabcon_billingedit_pay': 'Ctrl+Shift+Y',
    'key_tabcon_billingedit_save': 'Ctrl+Shift+S',
    'key_tabcon_billingedit_print': 'Ctrl+Shift+P',
    'employeetab_employee': 'Shift+Alt+E',
    'key_tabcon_empmgtemployee_add': 'Ctrl+Shift+A',
    'key_tabcon_empmgtemployee_view': 'Ctrl+Shift+V',
    'employeetab_attendance': 'Shift+Alt+A',
    'key_tabcon_empmgtattendence_search': 'Ctrl+Shift+E',
    'key_tabcon_empmgtattendence_save': 'Ctrl+Shift+S',
    'key_tabcon_empmgtattendence_create': 'Ctrl+Shift+C',
    'employeetab_payroll': 'Shift+Alt+P',
    'key_tabcon_empmgtpayroll_search': 'Ctrl+Shift+E',
    'key_tabcon_empmgtpayroll_save': 'Ctrl+Shift+S',
    'employeetab_shift': 'Shift+Alt+F',
    'key_tabcon_empmgtshift_view': 'Ctrl+Shift+N',
    'key_tabcon_empmgtshift_add': 'Ctrl+Shift+A',
    'employeetab_salsettings': 'Shift+Alt+S',
    'key_tabcon_empmgtsal_view': 'Ctrl+Shift+V',
    'key_tabcon_empmgtsal_new': 'Ctrl+Shift+N',
    'key_tabcon_menumgtmenu_view': 'Ctrl+Shift+V',
    'key_tabcon_menumgtmenu_add': 'Ctrl+Shift+A',
    'key_tabcon_menumgtmonsun_view': 'Ctrl+Shift+V',
    'key_tabcon_menumgtmonsun_refresh': 'Ctrl+Shift+R',
    'key_tabcon_menumgtmonsun_add': 'Ctrl+Shift+A',
}

custom_shortcut = {
    'key_global_quit': 'Ctrl+Alt+Q',
    'key_tabs_inventory': 'Ctrl+Alt+I',
    'key_tabs_billing': 'Ctrl+Alt+B',
    'key_tabs_menu': 'Ctrl+Alt+M',
    'key_tabs_employee': 'Ctrl+Alt+E',
    'key_tabs_report': 'Ctrl+Alt+R',
    'key_tabs_waste': 'Ctrl+Alt+W',
    'inventorytab_stock': 'Shift+Alt+S',
    'key_tabcon_inventorystock_refresh': 'Ctrl+Shift+R',
    'key_tabcon_inventorystock_print': 'Ctrl+Shift+P',
    'inventorytab_add': 'Shift+Alt+A',
    'key_tabcon_inventoryadd_search': 'Ctrl+Shift+R',
    'key_tabcon_inventoryadd_newrow': 'Ctrl+Shift+N',
    'key_tabcon_inventoryadd_addstock': 'Ctrl+Shift+A',
    'inventorytab_release': 'Shift+Alt+R',
    'key_tabcon_inventoryrelease_todaysrelease': 'Ctrl+Shift+T',
    'key_tabcon_inventoryrelease_newrow': 'Ctrl+Shift+N',
    'key_tabcon_inventoryrelease_release': 'Ctrl+Shift+R',
    'key_tabcon_inventoryrelease_addnewrow': 'Ctrl+Shift+A',
    'key_tabcon_inventoryrelease_discard': 'Ctrl+Shift+D',
    'inventorytab_purchase': 'Shift+Alt+P',
    'key_tabcon_inventorypurchase_search': 'Ctrl+Shift+S',
    'key_tabcon_inventorypurchase_additem': 'Ctrl+Shift+A',
    'key_tabcon_inventorypurchase_print': 'Ctrl+Shift+P',
    'key_tabcon_inventorypurchase_today': 'Ctrl+Shift+T',
    'key_tabcon_inventorypurchase_tommorow': 'Ctrl+Shift+O',
    'key_tabcon_inventorypurchase_thismonth': 'Ctrl+Shift+I',
    'key_tabcon_inventorypurchase_thisweek': 'Ctrl+Shift+W',
    'key_tabcon_inventorypurchase_clear': 'Ctrl+Shift+C',
    'inventorytab_supplier': 'Shift+Alt+S',
    'key_tabcon_inventorysupplier_add': 'Ctrl+Shift+A',
    'key_tabcon_inventorysupplier_view': 'Ctrl+Shift+V',
    'inventorytab_item': 'Shift+Alt+I',
    'key_tabcon_inventoryitem_addnewitem': 'Ctrl+Shift+A',
    'key_tabcon_inventoryitem_view': 'Ctrl+Shift+V',
    'key_tabcon_billingbills_newbill': 'Ctrl+Shift+N',
    'key_tabcon_billingbills_reset': 'Ctrl+Shift+R',
    'key_tabcon_billingbills_search': 'Ctrl+Shift+S',
    'key_tabcon_billingbills_selectbill': 'Ctrl+Shift+O',
    'key_tabcon_billingbills_showcredit': 'Ctrl+Shift+D',
    'key_tabcon_billingbills_showcustomer': 'Ctrl+Shift+C',
    'key_tabcon_billingedit_pay': 'Ctrl+Shift+Y',
    'key_tabcon_billingedit_save': 'Ctrl+Shift+S',
    'key_tabcon_billingedit_print': 'Ctrl+Shift+P',
    'employeetab_employee': 'Shift+Alt+E',
    'key_tabcon_empmgtemployee_add': 'Ctrl+Shift+A',
    'key_tabcon_empmgtemployee_view': 'Ctrl+Shift+V',
    'employeetab_attendance': 'Shift+Alt+A',
    'key_tabcon_empmgtattendence_search': 'Ctrl+Shift+E',
    'key_tabcon_empmgtattendence_save': 'Ctrl+Shift+S',
    'key_tabcon_empmgtattendence_create': 'Ctrl+Shift+C',
    'employeetab_payroll': 'Shift+Alt+P',
    'key_tabcon_empmgtpayroll_search': 'Ctrl+Shift+E',
    'key_tabcon_empmgtpayroll_save': 'Ctrl+Shift+S',
    'employeetab_shift': 'Shift+Alt+F',
    'key_tabcon_empmgtshift_view': 'Ctrl+Shift+N',
    'key_tabcon_empmgtshift_add': 'Ctrl+Shift+A',
    'employeetab_salsettings': 'Shift+Alt+S',
    'key_tabcon_empmgtsal_view': 'Ctrl+Shift+V',
    'key_tabcon_empmgtsal_new': 'Ctrl+Shift+N',
    'key_tabcon_menumgtmenu_view': 'Ctrl+Shift+V',
    'key_tabcon_menumgtmenu_add': 'Ctrl+Shift+A',
    'key_tabcon_menumgtmonsun_view': 'Ctrl+Shift+V',
    'key_tabcon_menumgtmonsun_refresh': 'Ctrl+Shift+R',
    'key_tabcon_menumgtmonsun_add': 'Ctrl+Shift+A',
}


def get_settings():
    """unpickle the settings saved"""
    with open('settings.text', 'rb') as fhandle:
        data = cPickle.load(fhandle)
    global level, default_shortcut, custom_shortcut, access, available_check, company
    level = data['debug_mode']
    if data.get('default_shortcut'):
        default_shortcut = data['default_shortcut']
    if data.get('custom_shortcut'):
        custom_shortcut = data['custom_shortcut']
    if data.get('access'):
        access = data['access']
    if data.get('avaliable_check'):
        available_check = data['avaliable_check']
    if data.get('company'):
        company = data['company']


def set_settings():
    """pickeles the settings"""
    global level, default_shortcut, custom_shortcut, access, available_check, company
    data = {'debug_mode': level, 'default_shortcut': default_shortcut, 'custom_shortcut': custom_shortcut,
            'access': access, 'available_check': available_check, 'company' : company}
    with open('settings.text', 'wb') as fhandle:
        cPickle.dump(data, fhandle, cPickle.HIGHEST_PROTOCOL)


