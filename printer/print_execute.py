#! /usr/bin/env python

""" printing management Module """

__authors__ = ["Jitesh Nair", "Jayarajan J N"]
__copyright__ = "Copyright 2015, Aider Solutons Pvt. Ltd."
__credits__ = [" Aider Solutons Pvt. Ltd."]
__version__ = "0"
__maintainer__ = "Jayarajan J N"
__email__ = "jayarajanjn@gmail.com"
__status__ = "Developement"

from collections import OrderedDict
import pdfkit

from jinja2 import Environment, FileSystemLoader
import tempfile, os, subprocess, sys
from proteus import Model, Wizard, config
from datetime import date, datetime
import logging
from GUI import settings
from collections import OrderedDict

logger = logging.getLogger(__name__)
logger.setLevel(settings.level)
if sys.platform == 'win32':
    from win32com import client
    import win32api
    import win32print


class PrintNow():
    def __init__(self, printer, dataobj, printformat):
        self.environment = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(), 'printer')))  # linux dependent
        self.html = object
        self.printer = printer
        self.fileformat = {'bill': 'bill.html', 'stock': 'stock.html', 'purchase': 'purchase_schedule.html',
                           'payslip': 'payslip.html', 'ticket': 'bill.html', 'bill_report': 'bill.html'}
        self.dataobj = dataobj
        self.printformat = printformat

    def start_print(self):
        """
        :return:
        """
        for i, j in self.fileformat.iteritems():
            if self.printformat == i:
                self.start(j)

    def start(self, template):
        """
        starts printing
        :param template:
        :return:
        """
        self.html = self.environment.get_template(template)
        con = config.get_config()
        User = Model.get('res.user')
        party = User(id=con.user).main_company.party
        address = party.addresses[-1]

        if self.printformat == 'bill':
            user = {}
            menu_list = self.dataobj[0]
            user['company'] = os.path.join(os.getcwd(), 'printer', 'company.png')
            user['menu'] = menu_list
            data = self.dataobj[1]
            status = data['status']
            if status == 'Paid':
                user['status'] = 'Bill Paid'
            else:
                user['status'] = 'Bill Due'
            user['total'] = data['total']
            user['bill_number'] = str(data['bill_number'])
            user['servicetax'] = data['tax']
            user['servicetax_amount'] = data['tax_amount']
            user['grandtotal'] = data['grand']
            user['roundoff'] = data['roundoff']
            user['name'] = party.name.title()
            user['address'] = address.full_address
            user['date'] = datetime.now().strftime('[%d-%b-%Y] %I:%M %p')
            return self.print_bill(user=user)
        if self.printformat == 'ticket':
            user = {}
            menu_list = self.dataobj[0]
            user['menu'] = menu_list
            data = self.dataobj[1]
            user['ticket_no'] = str(data['ticket_no'])
            user['table_no'] = str(data['table_no'])
            user['name'] = party.name.title()
            user['address'] = address.full_address
            user['date'] = datetime.now().strftime('[%d-%b-%Y] %I:%M %p')
            return self.print_ticket(user=user)
        if self.printformat == 'bill_report':
            user = {}
            menu_list = self.dataobj[0]
            user['menu'] = menu_list
            data = self.dataobj[1]
            user['total'] = str(data['total'])
            user['from_date'] = str(data['from_date'])
            user['to_date'] = str(data['to_date'])
            user['name'] = party.name.title()
            user['address'] = address.full_address
            user['date'] = datetime.now().strftime('[%d-%b-%Y] %I:%M %p')
            return self.print_bill_report(user=user)
        elif self.printformat == 'purchase':
            user = {}
            purchase_list = self.dataobj[0]
            supplier = purchase_list[0]['supplier']
            user['purchase_list'] = purchase_list
            user['company'] = os.path.join(os.getcwd(), 'printer', 'company.png')
            user['batch'] = self.dataobj[1]
            user['name'] = party.name.title()
            user['address'] = address.full_address
            user['date'] = date.today()
            user['supplier'] = supplier
            return self.print_purchase(user=user)
        elif self.printformat == 'stock':
            user = {}
            stock_list = self.dataobj
            user['stock_list'] = stock_list
            user['company'] = os.path.join(os.getcwd(), 'printer', 'company.png')
            user['name'] = party.name.title()
            user['address'] = address.full_address
            user['date'] = date.today()
            return self.print_stock(user=user)
        elif self.printformat == 'payslip':
            user = {}
            pay_slip = self.dataobj
            user['company'] = os.path.join(os.getcwd(), 'printer', 'company.png')
            user['name'] = party.name.title()
            user['address'] = address.full_address
            user['date'] = date.today()
            user['employee'] = pay_slip['employee']
            user['designation'] = pay_slip['designation']
            user['pan'] = pay_slip['pan']
            user['pay_date'] = pay_slip['date'].strftime('%B %Y')
            user['basic_pay'] = str(pay_slip['basic_pay'])
            user['da'] = str(pay_slip['da'])
            user['gross'] = str(pay_slip['gross'])
            user['hra'] = str(pay_slip['hra'])
            user['pf'] = str(pay_slip['pf'])
            user['esi'] = str(pay_slip['esi'])
            user['professional_tax'] = str(pay_slip['professional_tax'])
            user['other_deductions'] = str(pay_slip['other_deductions'])
            user['total_deduction'] = str(pay_slip['total_deduction'])
            user['net'] = str(pay_slip['net'])
            user['rupees'] = str(pay_slip['rupees'])
            return self.print_payslip(user=user)

        else:
            ############################test object instad of selfdataobj
            user = {}
            menu = []
            menu_item = {'date': '10/15/2015', 'code': '542', 'item': 'rice', 'rate': '100', 'amount': '500',
                         'category': 'grains',
                         'quantity': '5', 'supplier': 'id2015'}
            for i in range(50):
                menu.append(menu_item)

            user['menu'] = menu
            user['total'] = '50000'
            user['servicetax'] = '12.5'
            user['grandtotal'] = '51250'
            ##############################
        try: #waste not used pdf format discarded
            handle, destination_file = tempfile.mkstemp(suffix='.pdf')
            # HTML(string=''.join(self.html.generate(user=user)),
            # base_url=os.path.join(os.getcwd(), 'printer')).write_pdf(
            # destination_file)
            pdfkit.from_string(''.join(self.html.generate(user=user)), destination_file)
            if sys.platform == 'win32':
                os.startfile(destination_file, 'print')
            else:
                command = 'lp -t testfile -d {0} {1}'.format(self.printer, destination_file)
                subprocess.call(command.split(), shell=False)
                # with open('lol.html', 'w') as f:
                # print "created file"
                # f.write(''.join(self.html.generate(user=user)))
        except Exception, e:
            print "In Printing", sys.exc_info()
        finally:
            if sys.platform == 'win32':
                try:
                    if os.access(destination_file, os.O_RDWR):
                        try:
                            os.remove(destination_file)
                        except Exception, e:
                            print "In removing", sys.exc_info()
                except Exception, e:
                    print "In Accessing", sys.exc_info()
            else:
                os.unlink(destination_file)

    def print_bill(self, user):
        """print in the format of the bill"""
        try:
            destination_file = os.path.join(os.getcwd(), 'printer', 'bill.txt')
            self.pretty_bill(user, destination_file)
            if sys.platform == 'win32':
                self.print_windows(destination_file)
            else:
                command = 'lp -t testfile -d {0} {1}'.format(self.printer, destination_file)
                subprocess.call(command.split(), shell=False)
        except Exception, e:
            print "In Printing", sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def print_ticket(self, user):
        """prints in the format of the ticket"""
        try:
            destination_file = os.path.join(os.getcwd(), 'printer', 'ticket.txt')
            self.pretty_ticket(user, destination_file)
            if sys.platform == 'win32':
                for _ in range(2):
                    self.print_windows(destination_file)
            else:
                for _ in range(2):
                    command = 'lp -t testfile -d {0} {1}'.format(self.printer, destination_file)
                    subprocess.call(command.split(), shell=False)
        except Exception, e:
            print "In Printing", sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def print_bill_report(self, user):
        """prints in the format of the report"""
        try:
            destination_file = os.path.join(os.getcwd(), 'printer', 'bill_report.txt')
            self.pretty_bill_report(user, destination_file)
            if sys.platform == 'win32':
                self.print_windows(destination_file)
            else:
                command = 'lp -t testfile -d {0} {1}'.format(self.printer, destination_file)
                subprocess.call(command.split(), shell=False)
        except Exception, e:
            print "In Printing", sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def print_purchase(self, user):
        """prints the purchase list"""
        try:
            destination_file = os.path.join(os.getcwd(), 'printer', 'purchase.txt')
            self.pretty_purchase(user, destination_file)
            if sys.platform == 'win32':
                self.print_windows(destination_file)
            else:
                command = 'lp -t testfile -d {0} {1}'.format(self.printer, destination_file)
                subprocess.call(command.split(), shell=False)
        except Exception, e:
            print "In Printing", sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def print_stock(self, user):
        """prints the stock details"""
        try:
            destination_file = os.path.join(os.getcwd(), 'printer', 'stock.txt')
            self.pretty_stock(user, destination_file)
            if sys.platform == 'win32':
                self.print_windows(destination_file)
            else:
                command = 'lp -t testfile -d {0} {1}'.format(self.printer, destination_file)
                subprocess.call(command.split(), shell=False)
        except Exception, e:
            print "In Printing", sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def print_payslip(self, user):
        """prints the payslip"""
        try:
            destination_file = os.path.join(os.getcwd(), 'printer', 'payslip.txt')
            self.pretty_payslip(user, destination_file)
            if sys.platform == 'win32':
                self.print_windows(destination_file)
            else:
                command = 'lp -t testfile -d {0} {1}'.format(self.printer, destination_file)
                subprocess.call(command.split(), shell=False)
        except Exception, e:
            print "In Printing", sys.exc_info()
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def print_windows(self, filename):
        """printing in the windows suystem"""
        win32api.ShellExecute(0, "print", filename, '/d:"%s"' % self.printer, ".", 0)

    def pretty_bill(self, user, destination_file):
        """prints in the bill format"""
        printer = PrinterClass()
        destination_file = open(destination_file, 'w')
        printer.total_chars = 34
        printer.name = user['name']
        printer.address = user['address']
        printer.title = [user['status'], 'Bill No:' + user['bill_number']]
        printer.date = user['date']
        printer.file = destination_file
        printer.columns = OrderedDict([('No', 10), ('Item', 40), ('Qty', 15), ('Rate', 15), ('Total', 20)])
        content = []
        for n, i in enumerate(user['menu']):
            value = OrderedDict([('No', str(n + 1)), ('Item', i['item']),
                                 ('Qty', i['quantity']), ('Rate', i['rate']),
                                 ('Total', i['amount'])])
            content.append(value)
        printer.content = content
        printer.footer = (('Net Total', user['total']),
                          (user['servicetax'] + '%', user['servicetax_amount']),
                          ('Round Off Amount', user['roundoff']),
                          ('Grand Total', user['grandtotal']))
        printer.write_page()
        destination_file.close()
        return True

    def pretty_ticket(self, user, destination_file):
        """prints in the ticket format"""
        printer = PrinterClass()
        destination_file = open(destination_file, 'w')
        printer.total_chars = 34
        printer.name = user['name']
        printer.address = user['address']
        printer.title = ['Ticket No:' + user['ticket_no'], 'Table No:' + user['table_no']]
        printer.date = user['date']
        printer.file = destination_file
        printer.columns = OrderedDict([('No', 20), ('Item', 50), ('Qty', 30)])
        content = []
        for n, i in enumerate(user['menu']):
            value = OrderedDict([('No', str(n + 1)), ('Item', i['item']),
                                 ('Qty', i['quantity'])])
            content.append(value)
        printer.content = content
        printer.write_page()
        destination_file.close()
        return True

    def pretty_bill_report(self, user, destination_file):
        """prints in the report format"""
        printer = PrinterClass()
        destination_file = open(destination_file, 'w')
        printer.total_chars = 34
        printer.name = user['name']
        printer.address = user['address']
        printer.title = ['From Date:' + user['from_date'], 'To Date:' + user['to_date'], 'Total:' + user['total']]
        printer.date = user['date']
        printer.file = destination_file
        printer.columns = OrderedDict([('No', 20), ('Bill', 20), ('Date', 30), ('Total', 30)])
        content = []
        for n, i in enumerate(user['menu']):
            value = OrderedDict([('No', str(n + 1)), ('Bill', i['bill_no']),
                                 ('Date', i['date']), ('Total', i['total'])])
            content.append(value)
        printer.content = content
        printer.write_page()
        destination_file.close()
        return True

    def pretty_purchase(self, user, destination_file):
        """prints in the purchase format"""
        printer = PrinterClass()
        destination_file = open(destination_file, 'w')
        printer.total_chars = 34
        printer.name = user['name']
        printer.address = user['address']
        printer.title = ['Purchase Order to ' + user['supplier'], 'Purchase Ledger' + user['batch']]
        printer.date = user['date']
        printer.file = destination_file
        printer.columns = OrderedDict(
            [('No', 10), ('Code', 15), ('Item', 20), ('Category', 25), ('Units', 15), ('Qty', 15)])
        content = []
        for n, i in enumerate(user['purchase_list']):
            value = OrderedDict([('No', str(n + 1)), ('Code', i['code']),
                                 ('Item', i['item']), ('Category', i['category']),
                                 ('Units', i['units']), ('Qty', i['quantity'])])
            content.append(value)
        printer.content = content
        printer.footer = (('Total Items', str(len(user['purchase_list']))),)
        printer.write_page()
        destination_file.close()
        return True

    def pretty_stock(self, user, destination_file):
        """prints in the stock format """
        printer = PrinterClass()
        destination_file = open(destination_file, 'w')
        printer.total_chars = 34
        printer.name = user['name']
        printer.address = user['address']
        printer.title = ['Stock']
        printer.date = user['date']
        printer.file = destination_file
        printer.columns = OrderedDict(
            [('No', 10), ('Code', 15), ('Item', 15), ('Qty', 15), ('Batch', 15), ('Supp', 15), ('Exp', 15)])
        content = []
        for n, i in enumerate(user['stock_list']):
            value = OrderedDict([('No', str(n + 1)), ('Code', i['code']),
                                 ('Item', i['item']), ('Qty', i['quantity']), ('Batch', i['batch_number']),
                                 ('Supp', i['supplier']), ('Exp', i['expiry_date'])])
            content.append(value)
        printer.content = content
        printer.write_page()
        destination_file.close()
        return True

    def pretty_payslip(self, user, destination_file):
        """prints in the payslip format"""
        printer = PrinterClass()
        destination_file = open(destination_file, 'w')
        printer.total_chars = 34
        printer.name = user['name']
        printer.address = user['address']
        printer.title = ['Employee Name:' + user['employee'], 'Designation:' + user['designation'],
                         'PAN Number:' + user['pan'], 'Month and Year:' + user['pay_date']]
        printer.date = user['date']
        printer.file = destination_file
        printer.payslip = OrderedDict(
            [('Basic Pay', user['basic_pay']), ('DA', user['da']), ('HRA', user['hra']), ('PF', '-' + user['pf']),
             ('ESI', '-' + user['esi']), ('Professional Tax', '-' + user['professional_tax']),
             ('Other Deductions', '-' + user['other_deductions'])])
        printer.footer = (('Gross', user['gross']), ('Total Deductions', '-' + user['total_deduction'])
                          , ('Net', user['net']), ('Rupees', user['rupees'].title()))
        printer.write_pay()
        destination_file.close()
        return True


class PrinterClass():
    """the class that creates the printing output"""
    def __init__(self, total_chars=34):
        self.total_chars = total_chars #34 is default after checking the ouptut in the printed page
        self.title = []
        self.name = None
        self.address = None
        self.date = None
        self.file = None
        self.columns = None
        self.content = None
        self.footer = None
        self.payslip = None

    def write_name(self):
        """writes the name at the center"""
        print >> self.file, self.name.center(self.total_chars)

    def write_address(self):
        """writes the address"""
        address = self.address.replace('\n', ',').split(',')
        for i in address:
            print >> self.file, i.center(self.total_chars)

    def write_title(self):
        """writes the title of the page"""
        for i in self.title:
            print >> self.file, i.ljust(self.total_chars)

    def write_date(self):
        """writes the date"""
        data = datetime.now().strftime('[%d-%b-%Y] %I:%M %p')
        print >> self.file, data.rjust(self.total_chars)

    def table_header(self):
        """writes the header of the table"""
        for i, j in self.columns.iteritems():
            self.file.write(
                str('{}'.format(i.title().ljust(self._percent(j)))) if i != self.columns.keys()[-1] else str(
                    '{}'.format(i.title().rjust(self._percent(j)))))
        self.file.write('\n')

    def table_content(self):
        """writes the content of the table"""
        for i in self.content:
            steps = OrderedDict()
            start = False
            for key, values in i.iteritems():
                length = self._percent(self.columns[key])
                if len(values) > length:
                    start = True
                    chunks = self.chunk(values, (length - 1))
                    self.file.write(str('{}'.format(str(chunks[0]).ljust(length))) if key != i.keys()[-1] else str(
                        '{}'.format(str(chunks[0]).rjust(length))))
                    steps[key] = chunks[1]
                else:
                    steps[key] = ''
                    self.file.write(str('{}'.format(values.ljust(length))) if key != i.keys()[-1] else str(
                        '{}'.format(values.rjust(length))))
            if start:
                self.file.write('\n')
                for key, values in steps.iteritems():
                    length = self._percent(self.columns[key])
                    self.file.write(str('{}'.format(str(values).ljust(length))))
            self.file.write('\n')

    def chunk(self, sting, length):
        """breaks the content of the content into chunks to fit perfectly into the page"""
        return [sting[0 + i:length + i] for i in range(0, len(sting), length)]

    def table_footer(self):
        """table footer details printer"""
        for key, values in self.footer:
            data = str('{}{}'.format(str(key + ':').rjust(self._percent(60)), values.rjust(self._percent(40))))
            print >> self.file, data

    def conclusion(self):
        """prints the conclusion"""
        self.file.write('\n')
        print >> self.file, 'Authorized Signatory'.rjust(self.total_chars)

    def page_footer(self):
        """adds the footes to the page"""
        self.file.write('\n')
        print >> self.file, 'AIDER SOLUTIONS'.center(self.total_chars)
        print >> self.file, '(C)http://www.aidersolutions.in/'.center(self.total_chars)

    def _percent(self, value):
        """calclucate the percentage"""
        return int(round((float(value) / float(100)) * self.total_chars))

    def write_page(self):
        """writes the data to the page"""
        try:
            if not self.file:
                return False
            if self.name:
                self.write_name()
            if self.address:
                self.write_address()
            print >> self.file, '#' * 34
            if self.title:
                self.write_title()
            if self.date:
                self.write_date()
            print >> self.file, '=' * 34
            if self.columns:
                self.table_header()
            print >> self.file, '=' * 34
            if self.content:
                self.table_content()
            print >> self.file, '=' * 34
            if self.footer:
                self.table_footer()
            self.conclusion()
            self.page_footer()
        except Exception as e:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'

    def payslip_content(self):
        """writes the content for the payslip"""
        for key, value in self.payslip.iteritems():
            data = str('{}{}'.format(str(key + ':').rjust(self._percent(60)), value.rjust(self._percent(40))))
            print >> self.file, data

    def write_pay(self):
        """write method for payslip"""
        try:
            if not self.file:
                return False
            if self.name:
                self.write_name()
            if self.address:
                self.write_address()
            print >> self.file, '#' * 34
            if self.title:
                self.write_title()
            if self.date:
                self.write_date()
            print >> self.file, '=' * 34
            if self.payslip:
                self.payslip_content()
            print >> self.file, '=' * 34
            if self.footer:
                self.table_footer()
            self.conclusion()
            self.page_footer()
        except Exception as e:
            if settings.level == 10:
                logger.exception('raised exception')
            return False, 'Some Internal Error'