from django.contrib.auth.models import User
from ldap3 import Server, Connection, SUBTREE
from support_center.settings import LDAP_AUTH_URL, LDAP_AUTH_SEARCH_BASE,\
    LDAP_AUTH_CONNECTION_USERNAME, LDAP_AUTH_CONNECTION_PASSWORD


class LDAPBackend(object):

    def authenticate(self, username=None, password=None):
        server = Server(LDAP_AUTH_URL)

        c = Connection(server, user=LDAP_AUTH_CONNECTION_USERNAME, password=LDAP_AUTH_CONNECTION_PASSWORD)
        c.open()

        if c.bind():
            user_search_filter = '(uid={})'.format(username)
            c.search(search_base=LDAP_AUTH_SEARCH_BASE,
                     search_filter=user_search_filter,
                     search_scope=SUBTREE)

        common_name = c.response[0]['dn']

        if c.rebind(user=common_name, password=password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.save()

            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None