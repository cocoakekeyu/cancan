# -*- coding: utf-8 -*-
import itertools

from cancan.rule import Rule


class Ability(object):
    """provide an Ability class define ability can do something.
       An example class looks like this:

       import cancan

       class Ability(cancan.Ability):
           def __init__(self, user):
               if user.role == 'admin':
                   self.add('manage', 'all')
               else:
                   self.add('read', 'all')
    """

    def add(self, action=None, subject=None, **conditions):
        """
        Add ability are allowed using two arguments.

        The first one is the action you're setting the permission for,
        the second one is the class of object you're setting it on.
        the third one is the subject's conditions must be matches or a function
        to be test.

        self.add('update', Article)
        self.add('update', Article, user_id=1)
        self.add('update', Article, user_id=1, title='hello')
        self.add('update', Article, function=test_title)
        """
        self.add_rule(Rule(True, action, subject, **conditions))

    def addnot(self, action=None, subject=None, **conditions):
        """
        Defines an ability which cannot be done.
        """
        self.add_rule(Rule(False, action, subject, **conditions))

    def add_rule(self, rule):
        self.rules.append(rule)

    def can(self, action, subject, **conditions):
        """
        Check if the user has permission to perform a given action on an object
        """
        for rule in self.relevant_rules_for_match(action, subject):
            if rule.matches_conditions(action, subject, **conditions):
                return rule.base_behavior
        return False

    def cannot(self, *args, **kwargs):
        """
        Convenience method which works the same as "can"
        but returns the opposite value.
        """
        return not self.can(*args, **kwargs)

    def relevant_rules_for_match(self, action, subject):
        """retrive match action and subject"""
        matches = []
        for rule in self.rules:
            rule.expanded_actions = self.expand_actions(rule.actions)
            if rule.is_relevant(action, subject):
                matches.append(rule)

        return self.optimize(matches[::-1])

    def optimize(self, rules):
        def has_all(rule):
            return 'all' not in rule.subjects

        # cannot rule are evaluated first and then 'all' in subjects
        rules.sort(key=lambda rule: (rule.base_behavior, has_all(rule)))

        return rules

    def expand_actions(self, actions):
        """
        Accepts an array of actions and returns an array of actions which match
        """
        r = []
        for action in actions:
            r.append(action)
            if action in self.aliased_actions:
                r.extend(self.aliased_actions[action])
        return r

    def alias_action(self, *args, **kwargs):
        """
        Alias one or more actions into another one.

        self.alias_action('create', 'read', 'update', 'delete', to='crud')

        """
        to = kwargs.pop('to', None)
        if not to:
            return
        error_message = ("You can't specify target ({}) as alias "
                         "because it is real action name".format(to)
                         )
        if to in list(itertools.chain(*self.aliased_actions.values())):
            raise Exception(error_message)

        self.aliased_actions.setdefault(to, []).extend(args)

    @property
    def aliased_actions(self):
        if hasattr(self, '_aliased_actions'):
            return self._aliased_actions
        else:
            setattr(self, '_aliased_actions', {})
            return self._aliased_actions

    @property
    def rules(self):
        try:
            return self._rules
        except AttributeError:
            self._rules = []
            return self._rules
