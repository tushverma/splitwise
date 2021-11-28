import json, uuid, datetime
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from splitwise import models, views


class TestSplitwise(TestCase):
    def setUp(self):
        self.id = uuid.uuid4()
        self.client = APIClient()
        self.user1 = models.UserProfile.objects.create(
            name='ABC',
            email='abc@gmail.com',
            password='qwerty'
        )
        self.user2 = models.UserProfile.objects.create(
            name='ABC2',
            email='abc2@gmail.com',
            password='qwerty'
        )
        self.group = models.Group.objects.create(
            group_name='test123'
        )
        self.user2.save()
        self.user1.save()
        self.group.save()

    def test_create_user(self):
        factory = APIRequestFactory()
        view = views.UserProfileApiView.as_view()
        # create 2 users
        request = factory.post('/createUser',
                               json.dumps({
                                   "email": "abc3@gmail.com",
                                   "name": "ABC3",
                                   "password": "qwerty"
                               }),
                               content_type='application/json')

        result = view(request)
        expected_response = {
            "message": "User ABC3 created successfully"
        }
        self.assertEqual(result.data, expected_response)

    def test_create_group(self):
        factory = APIRequestFactory()
        view = views.CreateGroupApiView.as_view()

        request = factory.post('/createGroup',
                               json.dumps({
                                   "group_name": "test2",
                                   "members": [
                                       "abc@gmail.com"
                                   ]
                               }),
                               content_type='application/json')
        result = view(request)
        expected_response = {
            "message": "Group test2 Created successfully"
        }
        self.assertEqual(result.data, expected_response)

    def test_add_member_to_group(self):
        factory = APIRequestFactory()
        view = views.AddUserToGroupApiView.as_view()

        request = factory.post('/addUserToGroup',
                               json.dumps({
                                   "group_name": "test123",
                                   "user_email": "abc2@gmail.com"
                               }),
                               content_type='application/json')
        result = view(request)
        expected_response = {
            "message": "User abc2@gmail.com successfully added to group test123"
        }
        self.assertEqual(result.data, expected_response)

    def test_add_expense(self):
        factory = APIRequestFactory()
        view = views.CreateExpenseApiView.as_view()

        request = factory.post('/addExpense',
                               json.dumps({
                                   "users": [
                                       "abc@gmail.com",
                                       "abc2@gmail.com"
                                   ],
                                   "description": "Party expense123",
                                   "amount": 1400,
                                   "paid_by": "abc@gmail.com",
                                   "group_name": "test123",
                                   "name": "expense12345"
                               }),
                               content_type='application/json')

        result = view(request)
        expected_response = {
            "message": "Expense Created successfully"
        }
        self.assertEqual(result.data, expected_response)
