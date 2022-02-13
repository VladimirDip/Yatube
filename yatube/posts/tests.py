import django
import os
from yatube.settings import LOGIN_URL
from django.test.utils import setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube.settings')

django.setup()
setup_test_environment()

from django.test import TestCase, Client
from django.urls import reverse

from posts.models import User, Post


class RegistrationUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="james",
            email="bond_j@gmail.com",
            password="test_bond0987"
        )
        self.post = Post.objects.create(
            text="Bond... James Bond",
            author=self.user
        )

    def test_new_post_authorized_user(self):
        # login user and create post
        self.client.login(username="james", password="test_bond0987")
        self.client.post(
            reverse("new_post"),
            {
                "text": "test test"
            }
        )
        # Get profile new user and check how many posts have user, and the post can see on all urls
        response = self.client.get(reverse('profile', kwargs={'username': 'james'}))
        self.assertEqual(len(response.context["user_post"]), 2)
        for url in ("", "/james/", f"/james/{self.post.id}/"):
            response = self.client.get(url)
            self.assertContains(response, self.post.text)

    def test_edit_post(self):
        # Check to try to edit a user post
        self.client.login(username="james", password="test_bond0987")
        self.client.post(
            reverse("post_edit", kwargs={"username": "james", "post_id": self.post.id}),
            {
                "text": "edited post"
            }
        )
        self.assertEqual(Post.objects.get(id=self.post.id).text, "edited post")
        # Check to update post on all base pages
        for url in ("", "/james/", f"/james/{self.post.id}/"):
            response = self.client.get(url)
            self.assertContains(response, Post.objects.get(id=self.post.id).text)

    def test_new_post_unauthorized_user(self):
        self.client.post(
            reverse("new_post"),
            {
                "text": "test unauthorized user"
            }
        )
        # Check to change count posts
        response = self.client.get(reverse("profile", kwargs={"username": "james"}))
        self.assertEqual(len(response.context['user_post']),1)
        # Check redirect unautharized user when his want to add a new post
        response = self.client.get(reverse("new_post"))
        self.assertRedirects(response, '/auth/login/?next=/new/')


