FSERP(trytond 3.6.0, proteus 3.6.0)

Notations:
    <text> : input from the user required for the type of value mentioned between the brackets.

Dependencies:
    weasyprint,
    proteus 3.6.0,
    pyside

Note:
    This part of the code consists of different version of trytond and proteus,
    separate from the versions we are currently using and hence the following code
    should be executed when we use it for the first time.

    >>> bin/trytond -c etc/trytond.conf -d <databasename> --all

    After this the database and the trytond will be ready to be worked upon

Steps:Follow them the first time only
    1) In the Ipython shell run the following lines

    >>> import FSERP
    >>> from proteus import config,Model,Wizard
    >>> con=config.set_trytond(user='admin',database='testdb',config_file="<location of the trytond.conf")
    >>> User=Model.get('res.user') ####steps to create a user
    >>> user=User()
    >>> user.name=<name>
    >>> user.password=<password>
    >>> user.login=<username>
    >>> user.save()
    >>> Party=Model.get('party.party') ###steps to create a party
    >>> party=Party()
    >>> party.name='Aider'
    >>> party.save()
    >>> Currency=Model.get('currency.currency') ### steps to create a currency
    >>> currencies=Currency.find([('code','=','INR')])
    >>> currency,=currencies
    >>> company_config=Wizard('company.company.config')### steps to create a company
    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> con._context = User.get_preferences(True, con.context)
    >>> company_config.execute('company')
    >>> company=company_config.form
    >>> company.party=party
    >>> company.currency=currency
    >>> company_config.execute('add')

    2) Run the mainfile.py
    3) Enter the username and password
    4) Then click at admin panel
    5) Enter the credentials
    6) Edit the values and then save it.This should modify the company details.

Report:
    If you find any bug or error kindly contact me on jitesh.aider@gmail.com