import re
from cti.models import User
from ldap3 import Server, Connection, SUBTREE
from support_center.settings import LDAP_AUTH_URL, LDAP_AUTH_SEARCH_BASE,\
    LDAP_AUTH_CONNECTION_USERNAME, LDAP_AUTH_CONNECTION_PASSWORD


class LDAPBackend(object):

    def __init__(self):
        self.connection = None
        self.user_data = ''

    def authenticate(self, username=None, password=None):
        pattern = r"^(\d+)@edu.p.lodz.pl$"
        match = re.search(pattern, username)

        if match:
            username = match.group(1)

        if self.make_connection():
            self.get_user_data(username, password)

            return self.get_or_create_user(username, password)

        return None

    def get_user(self, user):
        try:
            return User.objects.get(pk=user)
        except User.DoesNotExist:
            return None

    def make_connection(self):
        server = Server(LDAP_AUTH_URL)

        self.connection = Connection(server, user=LDAP_AUTH_CONNECTION_USERNAME, password=LDAP_AUTH_CONNECTION_PASSWORD)
        self.connection.open()

        return True if self.connection.bind() else False

    def get_user_data(self, username, password):
        user_search_filter = '(uid={})'.format(username)

        if self.connection.search(search_base=LDAP_AUTH_SEARCH_BASE,
                                  search_filter=user_search_filter,
                                  search_scope=SUBTREE):
            user_data = self.connection.response[0]['dn']

            if self.connection.rebind(user=user_data, password=password):
                self.user_data = user_data

    def get_or_create_user(self, username, password):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username, password=password)

            pattern = r"cn=(\w+)\s+(\w+)\s+(\d+)"
            match = re.search(pattern, self.user_data)

            if match:
                user.first_name = match.group(1)
                user.last_name = match.group(2)
                user.email = "{}@edu.p.lodz.pl".format(match.group(3))
                user.is_superuser = False
                user.is_staff = False

            user.save()

            return user
