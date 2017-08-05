import cancan
from django.core.exceptions import PermissionDenied
from .models import Article


class Ability(cancan.Ability):
    def __init__(self, user):
        self.user = user

        if user is None or user.is_anonymous:
            self.init_guest_ability()
        elif user.is_superuser:
            self.init_superuser_ability()
        else:
            self.init_user_ability()

    def init_guest_ability(self):
        self.add('read', Article)

    def init_user_ability(self):
        self.add('read', Article)
        self.add('create', Article)
        self.add('update', Article, user_id=self.user.id)

    def init_superuser_ability(self):
        self.add('manage', 'all')


def authorize(user, action, subject):
    if Ability(user).cannot(action, subject):
        raise PermissionDenied
