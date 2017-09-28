# cancan

## Introduction

**cancan** is a tiny permission controller base on ruby cancan library. Once defined user ability, can easily check user's permission.

## Install

`pip install cancan`

## Basic Usage

inherit from cancan.Ability

use `add` method to add user Ability

```python
def add(self, action=None, subject=None, **conditions)`
    """
    Add ability are allowed using two arguments.

    The first one is the action you're setting the permission for,
    the second one is the class of object you're setting it on.
    the third one is the subject's attributes must be matches or a function
    to be test.

    self.add('update', Article)
    self.add('update', Article, user_id=1)
    self.add('update', Article, user_id=1, title='hello')
    self.add('update', Article, function=test_title)
    """
```

```python
import cancan

class User(object):
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

class Article(object):
    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

class Ability(cancan.Ability):
    def __init__(self, user):
        if user.role == 'admin':
            self.add('manage', 'all')
        else:
            self.add('read', Article)
            self.add('create', Article)
            self.add('update', Article, user_id=user.id)
            self.add('create', 'bbb')


admin = User(1, 'neven', 'admin')
ability = Ability(admin)

# admin
ability.can('read', Article)    # True
ability.can('create', Article)  # True
ability.can('delete', Article)  # True
ability.can('aaa', Article)     # True
ability.can('create', 'bbb')    # True
ability.can('create', 'ccc')    # True

user = User(2, 'joe', 'user')
ability2 = Ability(user)

# user
ability2.can('read', Article)   # True
ability2.can('create', Article) # True
ability2.can('delete', Article) # False
ability2.can('aaa', Article)    # False
ability2.can('create', 'bbb')   # True
ability2.can('create', 'ccc')   # False

article = Article('hello', 2)
# admin
ability.can('update', article) # True

# user
ability2.can('update', article) # True
ability2.can('update', Article) # True(class dont check conditions)
```

## Advanced

```python
import cancan


def test_title_gt_100(article):
    return len(article.title) > 100

def anoter_test(article, id, len_title):
    return article.user_id < id and len(article.title) > len_article

class Ability(cancan.Ability):
    def __init__(self, user):
        self.alias_action('create', 'read', 'update', to='cru')

        if user.role == 'admin':
            self.add('manage', 'all')
            self.addnot('destroy', 'gem')
        elif user.role == 'editor':
            self.add('cru', Article)
            self.add(['read', 'create'], 'gem')
            self.add('update', Article, function=test_title_gt_100)
            self.add('delete', Article, function=another_test, func_args=(10,), func_kwargs={"len_title": 4})
        else:
            self.add('create', Article)
            self.add('update', Article, user_id=user.id)
            self.add('create', 'bbb')

editor = User(3, 'kali', 'editor')
ability3 = Ability(editor)

# editor
ability3.can('create', Article)  # True
ability3.can('update', Article)  # True
ability3.can('cru', Article)  # True
ability3.can('read', 'gem')  # True
ability3.can('create', 'gem')  # True

article = Article('world', 1)
ability3.can('update', article)  # False
ability3.can('delete', article)  # True

article = Article('world'*100, 1)
ability3.can('delete', article)  # True

```

## Example

see example.py

## Integrate Django

see django_example
