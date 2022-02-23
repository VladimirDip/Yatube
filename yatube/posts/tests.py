import django
from django.core.cache import caches
import os
from yatube.settings import LOGIN_URL
from django.test.utils import setup_test_environment

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube.settings')

django.setup()
setup_test_environment()

from django.test import TestCase, Client
from django.urls import reverse

from posts.models import User, Post


class SomeTests(TestCase):

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
        # print(response.context)
        self.assertEqual(response.context["count_posts"], 2)
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
        self.assertEqual(response.context["count_posts"], 1)
        # Check redirect unautharized user when his want to add a new post
        response = self.client.get(reverse("new_post"))
        self.assertRedirects(response, '/auth/login/?next=/new/')


class TestPageError(TestCase):

    def setUp(self):
        self.client = Client()

    def test_page_404(self):
        response = self.client.get("/hhhh/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed("template/misc/404.html")


class TestImageOnPages(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="james",
            email="bond_j@gmail.com",
            password="test_bond0987"
        )
        self.post = Post.objects.create(
            text="I check my image",
            author=self.user,

        )
        image = "../media/posts/IMG_0607.JPG"

        self.post2 = Post.objects.create(
                text="Check image file",
                author=self.user,
                image=image
            )

    def test_contains_img_pages(self):
        response = self.client.get(reverse("profile", kwargs={"username": "james"}))
        # Check added new post
        self.assertEqual(response.context["count_posts"], 2)
        # Check screening <img> on page
        self.assertContains(response, "img")

    def test_contains_img_all_main_pages(self):
        for url in ("", "/james/", f"/james/{self.post2.id}/"):
            response = self.client.get(url)
            self.assertContains(response, '<img class="card-img"')

    def test_protection_against_not_image_files(self):
        self.client.login(username="james", password="test_bond0987")
        with open("models.py", "rb") as img:
            post = self.client.post("/new/", {"author": self.user,
                                              "text": "anymore text",
                                              "image": img})
            # Check to screen a error when loading an invalid format file
            self.assertContains(post, "alert alert-danger")

class TestCacheIndexPage(TestCase):

    def setUp(self):
        self.client = Client()


    def test_working_cache(self):
        with self.assertNumQueries(6):
            response = self.client.get(reverse("index"))
            self.assertEqual(response.status_code, 200)
            # Check my cache with second request
            response = self.client.get(reverse("index"))
            self.assertEqual(response.status_code, 200)

