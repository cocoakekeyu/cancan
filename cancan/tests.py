# -*- coding: utf-8 -*-
import unittest

from cancan.ability import Ability


class TestAbility(unittest.TestCase):

    def setUp(self):
        pass

    def test_base_ability(self):
        a = Ability()
        a.add('read', 'all')
        a.add('delete', 'ad')
        self.assertTrue(a.can('read', 'a'))
        self.assertTrue(a.can('read', 'all'))
        self.assertTrue(a.can('delete', 'ad'))

        b = Ability()
        b.add('manage', 'a')
        self.assertTrue(b.can('read', 'a'))
        self.assertFalse(b.can('read', 'b'))

        c = Ability()
        s = object()
        c.add('update', object)
        self.assertTrue(c.can('update', s))

    def test_list_action_or_subject(self):
        a = Ability()
        a.add(['read', 'update'], 'ad')
        self.assertTrue(a.can('update', 'ad'))

        b = Ability()
        b.add(['read', 'update'], ['ad', 'name'])
        self.assertTrue(b.can('update', 'ad'))
        self.assertTrue(b.can('read', 'name'))
        self.assertFalse(b.can('delete', 'name'))

    def test_not_action(self):
        a = Ability()
        a.addnot('update', 'ad')
        a.add('manage', 'all')
        self.assertFalse(a.can('update', 'ad'))
        self.assertTrue(a.can('update', 'name'))

    def test_alias_action(self):
        a = Ability()
        a.alias_action('create', 'read', 'update', 'delete', to='crud')
        a.add('crud', 'ad')
        self.assertTrue('read', 'ad')
        self.assertTrue('delete', 'ad')

    def test_conditions(self):
        class Article(object):
            def __init__(self, title, user_id):
                self.title = title
                self.user_id = user_id

        a = Ability()
        article = Article('hello', 1)
        article2 = Article('hello2', 2)
        a.add('update', Article, user_id=1)
        self.assertTrue(a.can('update', article))
        self.assertFalse(a.can('update', article2))
        self.assertTrue(a.can('update', Article))

    def test_fuction(self):
        class Article(object):
            def __init__(self, title, user_id):
                self.title = title
                self.user_id = user_id

        def user_id_less_10(subject):
            return subject.user_id < 10

        a = Ability()
        article = Article('hello', 1)
        a.add('update', Article, function=user_id_less_10)
        self.assertTrue(a.can('update', article))

        article = Article('hello', 15)
        self.assertFalse(a.can('update', article))


if __name__ == '__main__':
    unittest.main()
