#unuse4d files
import subprocess
import getpass


def update_all():
    password = getpass.getpass()
    check_update = ''
    try:
        pull = subprocess.check_output(
            ['hg', 'pull', '-u',
             'https://erpclient:' + password + '@bitbucket.org/jayarajanjn/fserp'])
        update = subprocess.call(['hg', 'update', '-r', 'FSERP', '-C'])
        check_update = subprocess.check_output(['hg', 'status', '--rev', '.^'])
    except subprocess.CalledProcessError as e:
        print 'Something went wrong, rerun the script'
    if 'M updated_scripts' in check_update:
        runner = subprocess.call(['python2.7', 'updated_scripts.py'])
    else:
        print 'Already upto date'

    raw_input('Press Enter to continue...................')


if __name__ == '__main__':
    update_all()
