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


def test_title_gt_100(article):
    return len(article.title) > 100


class Ability(cancan.Ability):
    def __init__(self, user):
        self.alias_action('create', 'read', 'update', to='cru')

        if user.role == 'admin':
            self.add('manage', 'all')
            self.addnot('destroy', 'gem')
        elif user.role == 'editor':
            self.add('cru', Article)
            self.add(['read', 'create'], 'gem')
            self.add('delete', Article, function=test_title_gt_100)
        else:
            self.add('read', Article)
            self.add('create', Article)
            self.add('update', Article, user_id=user.id)
            self.add('create', 'bbb')


if __name__ == '__main__':

    admin = User(1, 'neven', 'admin')
    ability = Ability(admin)

    print('admin can read Article:', ability.can('read', Article))    # True
    print('admin can create Article:', ability.can('create', Article))  # True
    print('admin can delete Article:', ability.can('delete', Article))  # True
    print('admin can aaa Article:', ability.can('aaa', Article))     # True
    print('admin can create bbb:', ability.can('create', 'bbb'))    # True
    print('admin can create ccc:', ability.can('create', 'ccc'))    # True
    print('admin can destroy gem:', ability.can('destroy', 'gem'))    # False

    user = User(2, 'joe', 'user')
    ability2 = Ability(user)

    print('user can read Article:', ability2.can('read', Article))    # True
    print('user can create Article:', ability2.can('create', Article))  # True
    print('user can delete Article:', ability2.can('delete', Article))  # False
    print('user can aaa Article:', ability2.can('aaa', Article))     # False
    print('user can create bbb:', ability2.can('create', 'bbb'))    # True
    print('user can create ccc:', ability2.can('create', 'ccc'))    # False

    article = Article('hello', 2)
    print('admin can update article:', ability.can('update', article))   # True

    print('user can update article:', ability2.can('update', article))   # True
    print('user can update Article:', ability2.can('update', Article))  # True
    article = Article('hello', 1)
    print('user can update article:', ability2.can('update', article))  # False

    editor = User(3, 'kali', 'editor')
    ability3 = Ability(editor)

    print('editor can create Article:', ability3.can('create', Article))  # True
    print('editor can update Article:', ability3.can('update', Article))  # True
    print('editor can cru Article:', ability3.can('cru', Article))  # True
    print('editor can read gem:', ability3.can('read', 'gem'))  # True
    print('editor can create gem:', ability3.can('create', 'gem'))  # True

    article = Article('world', 1)
    print('editor can delete article:', ability3.can('delete', article))  # False

    article = Article('world'*100, 1)
    print('editor can delete article:', ability3.can('delete', article))  # True
