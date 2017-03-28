import re
from cti.models import User
from ldap3 import Server, Connection, SUBTREE
from support_center.settings import LDAP_AUTH_URL, LDAP_AUTH_SEARCH_BASE,\
    LDAP_AUTH_CONNECTION_USERNAME, LDAP_AUTH_CONNECTION_PASSWORD
from django.db import connections
from .models import Object


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
            if self.get_user_data(username, password):
                return self.get_or_create_user(username)

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
            self.user_data = self.connection.response[0]['dn']

        return True if self.connection.rebind(user=self.user_data, password=password) else False

    def get_or_create_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)

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


class InvbookBackend(object):

    def __init__(self):
        self.connection = None
        self.tables = []

    def get_object_information(self):
        tables = ['b010t4', 'b010t6', 'b010t8', 'b011t4', 'b011t6', 'b011t8', 'b020']
        rows = []

        context = {}

        c = connections['invbook'].cursor()

        for table in tables:
            query = 'SELECT ' \
                    'nr_fabryczny_przychodu AS object_number ,' \
                    'nazwa_przedmiotu AS name ,' \
                    'data_przychodu AS date ,' \
                    'pomieszczenie AS room ,' \
                    'ilosc_przychod AS status , ' \
                    'cena_jednostkowa AS price , ' \
                    'uwagi AS comments ' \
                    'FROM invbook.{} WHERE nr_fabryczny_przychodu={}'.format(table, '1000019856')

            if c.execute(query):
                data = c.fetchone()

                try:
                    Object.objects.get(object_number=data[0])
                except Object.DoesNotExist:
                    dupa = Object(object_number=data[0])

                    dupa.object_name = data[1]
                    dupa.created_at = data[2]
                    dupa.room = data[3]
                    dupa.status = data[4]
                    dupa.price = data[5]
                    dupa.comments = data[6]

                    dupa.save()
                rows.append(data)

                context = {'object_number': data[0],
                           'object_name': data[1],
                           'created_at': data[2],
                           'room': data[3],
                           'status': data[4],
                           'price': data[5],
                           'comments': data[6]}

        return context
