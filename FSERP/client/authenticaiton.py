from FSERP import cleint


class Authentication(object):
    """ Autheticaiton and user related"""

    def __init__(self):
        pool = Pool()

    def get_admin(self):
        with Transaction().start(dbname, 0) as transaction:
            user_obj = pool.get('res.user')
            user = user_obj.search([('login', '=', 'admin')], limit=1)[0]
            return user.id
        return None

    def login(self, username, password):
        with Transaction().start(dbname, 0) as transaction:
            pass  # TODO
