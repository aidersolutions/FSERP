from subprocess import Popen, PIPE, STDOUT

def install_and_import(package):
    import importlib
    package_name = package.split("==")[0]
    package_name = package_name.split("-")[1] if '-' in package_name else package_name
    try:
        importlib.import_module(package_name)
    except ImportError:
        import pip

        pip.main(['install', package, '--allow-external', package])
    finally:
        globals()[package] = importlib.import_module(package_name)


def get_dependencies():
    install_and_import('proteus==3.6.0')
    install_and_import('lxml')
    install_and_import('relatorio')
    install_and_import('python-dateutil')
    install_and_import('polib')
    install_and_import('python-sql')
    install_and_import('pywebdav')
    install_and_import('pydot')
    install_and_import('sphinx')
    install_and_import('cdecimal')
    install_and_import('simplejson')
    install_and_import('python-Levenshtein')
    install_and_import('pdfkit')
    install_and_import('wkhtmltopdf')
    install_and_import('inflect')
    install_and_import('python-ldap')
    install_and_import('vobject')
    install_and_import('python-stdnum')
    install_and_import('simpleeval')
    install_and_import('cached_property')
    install_and_import('psycopg2')

if __name__ == '__main__':
    get_dependencies()
    print "Setting up Database"
    p = Popen(['python', 'FSERP/trytond/bin/trytond', '-vc', 'FSERP/trytond/etc/trytond.conf', '-d', "testdbkitchen", '--all'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    grep_stdout = p.communicate()[0]
    for i in grep_stdout.split("\n"):
            print "\n%s"%i 
    if p.returncode == 0:
        print "Setting up Modules"
        p = Popen(['python', 'install.py'])
        grep_stdout = p.communicate()[0]
        if p.returncode != 0:
            p = Popen(['python', 'install.py'])
            grep_stdout = p.communicate()[0]
        #for i in grep_stdout.split("\n"):
        #    print "\n%s"%i 
    
