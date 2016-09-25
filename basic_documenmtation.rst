1] An unused file is marked "unused" in the top of the file

   These files are kept without deleting, so that certain details and approach of the code and erp implemetation can be fetched form them

   These provide the methods that were used but later discarded but can be used in future if required



2] An unused method is marked as "waste not used"

   These functions are kept without deleting, again for the same reason as above

3] files wil extension .ui are files used in qteditor which creates corresponding .py files with a warning in the heading like the one in below


   # -*- coding: utf-8 -*-

   # Form implementation generated from reading ui file 'notificationbottom_template.ui'
   #
   # Created: Fri Jul 24 19:44:01 2015
   #      by: pyside-uic 0.2.13 running on PySide 1.1.1
   #
   # WARNING! All changes made in this file will be lost!

   These .py files should only be edited from qt editor by loading the .ui files

4] Tryton models are similar to any other ORMS with some small changes in the syntaxes but provides good abstraction and a good google search "tryton model queries" can provide some very good results

5] We have used `Transactions()` to access the db, it provides better context managers and faster backed access.

6] Querying are simple ORM queries the important things to note are regarding the inter-relation of the modules like between the Party, Company, Accounts which are related to the accounting domain