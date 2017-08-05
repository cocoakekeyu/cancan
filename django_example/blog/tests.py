from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from blog.models import Article


class TestBlog(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='user', email='user@gmail.com', password='123456')
        admin = User.objects.create_superuser(
            username='admin', email='admin@gmail.com', password='123456')
        self.user_article = Article.objects.create(title='hello world', user=user)
        self.admin_article = Article.objects.create(title='welcom', user=admin)

    def test_user_index(self):
        c = Client()
        c.login(username='user', password='123456')
        response = c.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_guest_index(self):
        c = Client()
        c.login(username='user', password='123456')
        response = c.get('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_user_create(self):
        c = Client()
        c.login(username='user', password='123456')
        response = c.post('/articles/')
        self.assertEqual(response.status_code, 200)

    def test_guest_can_not_create(self):
        c = Client()
        response = c.post('/articles/')
        self.assertEqual(response.status_code, 403)

    def test_user_update_owner_article(self):
        c = Client()
        c.login(username='user', password='123456')
        response = c.put('/articles/' + str(self.user_article.id))
        self.assertEqual(response.status_code, 200)

    def test_user_can_not_update(self):
        c = Client()
        c.login(username='user', password='123456')
        response = c.put('/articles/' + str(self.admin_article.id))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_all(self):
        c = Client()
        c.login(username='admin', password='123456')
        response = c.put('/articles/' + str(self.user_article.id))
        self.assertEqual(response.status_code, 200)

    def test_user_can_not_delete(self):
        c = Client()
        c.login(username='user', password='123456')
        response = c.delete('/articles/' + str(self.user_article.id))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_all(self):
        c = Client()
        c.login(username='admin', password='123456')
        response = c.delete('/articles/' + str(self.user_article.id))
        self.assertEqual(response.status_code, 200)
