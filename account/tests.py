from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        User.objects.create_user(email='normal@user.com', password='foo')
        user = User.objects.get(email='normal@user.com')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        User.objects.create_superuser(email='super@user.com', password='foo')
        super_user = User.objects.get(email='super@user.com')
        self.assertEqual(super_user.email, 'super@user.com')
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        try:
            self.assertIsNone(super_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)

    def test_login(self):
        User = get_user_model()
        User.objects.create_user(email='normal@user.com', password='foo')
        user = User.objects.get(email='normal@user.com')
        c = Client()
        logged_in = c.login(email=user.email, password='foo')
        self.assertTrue(logged_in)

    def test_change_password(self):
        User = get_user_model()
        User.objects.create_user(email='normal@user.com', password='foo')
        user = User.objects.get(email='normal@user.com')
        self.assertEquals(user.check_password("foo"), True)
        self.assertEquals(user.check_password("bar"), False)
        user = User.objects.change_password(email='normal@user.com',
                                            password='foo',
                                            new_password='bar')
        self.assertEquals(user.check_password("bar"), True)
        self.assertEquals(user.check_password("foo"), False)
