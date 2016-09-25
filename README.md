# [FSERP](#markdown-header-fserp)

Fserp is a erp built with [tryton](http://www.tryton.org/) as a backend and [PySide](https://pypi.python.org/pypi/PySide) as a front end.

### [Summary](#markdown-header-summary)
----

 - version 1.2
 - Tested on windows xp, 7, 8 and 10 and debian

### [Features](#markdown-header-features)
----

 - Stock Management
 - Menu Management
 - Invoicing
 - Employee Management
 - Waste Management

### [Setup](#markdown-header-setup)
----

1. Go to a separate directory in my case i used up the 'G:' as it creates less confusion. Download all the packages to the this directory.

2. Install Python and MS VC C++
Python requires certain steps to be followed on windows and hence follow this link [python for windows 32 direct download](https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi) and then read this [how to set up on windows](http://www.swaroopch.com/notes/python/#install_windows)
The vc ++ is required to process python on windows just install from [microsoft vc ++](https://www.microsoft.com/en-us/download/details.aspx?id=44266)

3. Got to system environment variables settings and set 'C:\Python27\Scripts' which will be required to use pip

4. Install postgress and go to c:\Programfiles(x86)\PostgreSQL\9.1\bin and start pdadmin.

    1. Create a new login role in pgadmin-III, with a secure password
    2. Create a user named 'tryton'
    3. Create a new database 'testdbkitchen' with 'tryton' as the owner 

5. Download win-psycopg from [win-psycopg2](http://www.stickpeople.com/projects/python/win-psycopg/)

6. Download [cdecimal](http://www.bytereef.org/software/mpdecimal/releases/cdecimal-2.3.tar.gz) 

7. Open CMD and got to a directory, Run this command

        hg clone https://jayarajanjn@bitbucket.org/jayarajanjn/fserpkitchen

8. Go to the fserpkitchen directory

        cd fserpkitchen

9. Go to the FSERP branch

        hg checkout FSERP

10. Run the setup file

        python setup.py

    >details like admin password and company name and new user should be entered when prompted

11. Run mainfile

        python mainfile.py

12. Write click on the mainfile and create a shortcut of the file  in the desktop.

### [Contribution guidelines](#markdown-header-contribution-guidlines)
----

* Writing tests
* Code review
* Other guidelines

### [Who do I talk to?](#markdown-header-who-do-i-talk-to-?)
----

* Repo owner or admin
* Other community or team contact