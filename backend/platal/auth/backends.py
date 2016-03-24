# -*- coding: utf-8 -*-

import hashlib
import hmac

from . import models


class PlatalAuthBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            account = models.Account.objects.get(hruid=username)
        except models.Account.DoesNotExist:
            return None

        pwdhash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        if hmac.compare_digest(account.password, pwdhash):
            return account
        return None

    def get_user(self, user_id):
        return models.Account.objects.get(pk=user_id)

    def has_perm(self, user_obj, perm, obj=None):
        """
        Object-level access restrictions (for the API):
        * Read access is always allowed. Field-level access is managed in views.
        * Change (Write) access is only allowed:
          - for the account who owns the object (obj.get_owner() = logged user)
          - for administrators
        * Add and delete accesses are allowed:
          - for the owner if the object also has a field "owner_manageable"
          - for administrators
        """
        # Ignore app_label in perms:
        # we only do object-level permissions
        if '.' in perm:
            _, perm = perm.split('.')

        # Basic app-level permissions : only allow get
        if obj is None:
            if perm == 'view':
                return True
            else:
                return False

        # Allow superpowers to admins
        if user_obj.is_admin:
            return True

        if perm == 'view':
            return True
        elif perm == 'change':
            return hasattr(obj, 'get_owner') and obj.get_owner() == user_obj
        elif perm in ('add', 'delete'):
            return (getattr(obj, 'owner_manageable', False) and
                    hasattr(obj, 'get_owner') and
                    obj.get_owner() == user_obj)
        else:
            return False

    def get_all_permissions(self, user_obj, obj=None):
        perms = set(['view'])
        if obj is None:
            return perms
        if hasattr(obj, 'get_owner') and obj.get_owner() == user_obj:
            perms.add('change')
            if getattr(obj, 'owner_manageable', False):
                perms.add('add')
                perms.add('delete')
        return perms
