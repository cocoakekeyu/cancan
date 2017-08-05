# -*- coding: utf-8 -*-
import inspect
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring

def listify(o):
    if isinstance(o, (list, tuple)):
        return o
    else:
        return [o]


class Rule(object):
    def __init__(self, base_behavior, action, subject, **conditions):
        """
        The first argument when initializing is the base_behavior which is a
            true/false value. True for "can" and false for "cannot".
        The next two arguments are the action and subject respectively.
        The third argument is a dict of conditions.

        """
        self.base_behavior = base_behavior
        self.actions = listify(action)
        self.subjects = listify(subject)
        self.conditions = conditions
        self.function = self.conditions.pop('function', None)

    def __str__(self):
        return 'Rule:{}{}'.format(self.actions, self.subjects)

    def is_relevant(self, action, subject):
        """
        Matches both the subject and action, not necessarily the conditions.
        """
        return self.matches_action(action) and self.matches_subject(subject)

    def matches_subject(self, subject):
        return 'all' in self.subjects or subject in self.subjects or \
            self.matches_subject_class(subject)

    def matches_action(self, action):
        return 'manage' in self.expanded_actions or \
            action in self.expanded_actions

    def matches_subject_class(self, subject):
        for sub in self.subjects:
            if inspect.isclass(sub):
                if inspect.isclass(subject):
                    return issubclass(subject, sub)
                else:
                    return isinstance(subject, sub)
            elif isinstance(sub, string_types):
                if inspect.isclass(subject):
                    return subject.__name__ == sub
                else:
                    return subject.__class__.__name__ == sub
        return False

    def matches_conditions(self, action, subject, **conditions):
        if self.function:
            return self.matches_function(action, subject)
        elif self.conditions == {}:
            return True
        elif inspect.isclass(subject):
            return True
        else:
            return self.matches_dict_conditions(action, subject)

    def matches_dict_conditions(self, action, subject):
        return all(getattr(subject, key) == value
                   for key, value in self.conditions.items())

    def matches_function(self, action, subject):
        return self.function(subject)

    @property
    def expanded_actions(self):
        try:
            return self._expaned_actions
        except AttributeError:
            return self.actions

    @expanded_actions.setter
    def expanded_actions(self, value):
        self._expaned_action = value
