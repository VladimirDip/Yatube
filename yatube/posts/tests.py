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

from posts.models import User, Post, Follow


class SomeTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="james",
            email="bond_j@gmail.com",
            password="test_bond0987"
        )

    def _get_urls(self, post):
        urls = [reverse("index"),
                reverse("profile", kwargs={"username": post.author.username}),
                reverse("post", kwargs={"username": post.author.username,
                                        "post_id": post.id})]
        return urls

    def _check_post_on_page(self, url, post):
        """To test that post from arguments is on pages"""
        response = self.client.get(url)
        if "paginator" in response.context:
            posts_list = response.context["paginator"].object_list
            self.assertIn(post, posts_list)
        else:
            print(response.context["post"])
            self.assertEqual(response.context["post"], post)

    def test_post_on_pages(self):
        """To test that created post is on pages"""
        post = Post.objects.create(text="test text",
                                   author=self.user)
        urls = self._get_urls(post=post)
        for url in urls:
            self._check_post_on_page(url=url, post=post)

    def test_edit_post(self):
        """To test if author can edit post and post in on pages"""
        post = Post.objects.create(text="test text",
                                   author=self.user)
        print(post.id)
        response = self.client.post(
            reverse('post_edit', kwargs={
                "username": post.author.username,
                "post_id": post.id
            }),
            {"text": "edit text"}, follow=True
        )
        post = Post.objects.get(id=post.id)
        print(post)
        urls = self._get_urls(post=post)
        for url in urls:
            self._check_post_on_page(url=url, post=post)

    def test_new_post_unauthorized_user(self):
        self.client.post(
            reverse("new_post"),
            data={
                "text": "test unauthorized user"
            }
        )
        # Check to change count posts
        response = self.client.get(reverse("profile", kwargs={"username": "james"}))
        self.assertEqual(response.context["paginator"].count, 0)
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
        image = "../media/posts/1596020938825.png"

        self.post2 = Post.objects.create(
            text="Check image file",
            author=self.user,
            image=image
        )
        self.client.login(username=self.user.username, password=self.user.password)

    def test_contains_img_pages(self):
        response = self.client.get(reverse("profile", kwargs={"username": self.user.username}))
        # Check added new post
        self.assertEqual(response.context["paginator"].count, 2)
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
        with self.assertNumQueries(0):
            response = self.client.get(reverse("index"))
            self.assertEqual(response.status_code, 200)
            # Check my cache with second request
            response = self.client.get(reverse("index"))
            self.assertEqual(response.status_code, 200)


class TestFollowerFollowing(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@mail.ru",
            password="test12345678"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@mail.ru",
            password="test12345678"
        )

    def test_following_unfollowing(self):
        self.client.login(username="user1", password="test12345678")
        following_user1 = Follow.objects.filter(user=self.user1)
        self.assertEqual(following_user1.count(), 0)
        # Go to the url 'profile_follow' for user1 following user2
        following = self.client.post(reverse("profile_follow",
                                             kwargs={"username": self.user2}),
                                     follow=True)
        self.assertEqual(following.status_code, 200)
        self.assertEqual(following_user1.count(), 1)
        # Gp to the url 'profile_unfollow' for user1 unfollowing user2
        unfollowing = self.client.post(reverse("profile_unfollow",
                                               kwargs={"username": self.user2}),
                                       follow=True)
        self.assertEqual(unfollowing.status_code, 200)
        self.assertEqual(following_user1.count(), 0)
