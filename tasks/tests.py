from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Task

class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123', first_name='Test')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass123', first_name='Other')

        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.access_token = response.data['access']
        self.auth_header = f'Bearer {self.access_token}'

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'newpass123',
            'first_name': 'New',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_and_get_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertIn('access', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        response = self.client.post(reverse('task_list_create'), {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'new',
        }, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_get_own_tasks(self):
        Task.objects.create(title="My Task", user=self.user)
        Task.objects.create(title="Other Task", user=self.other_user)

        response = self.client.get(reverse('task_list_create') + '?mytasks=true', HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'My Task')

    def test_update_task_by_owner(self):
        task = Task.objects.create(title="Updatable Task", user=self.user)
        url = reverse('task_detail', args=[task.id])
        response = self.client.patch(url, {'status': 'completed'}, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')

    def test_cannot_update_task_by_other(self):
        task = Task.objects.create(title="Other Task", user=self.other_user)
        url = reverse('task_detail', args=[task.id])
        response = self.client.patch(url, {'status': 'completed'}, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_completed(self):
        task = Task.objects.create(title="Incomplete Task", user=self.user)
        url = reverse('mark_completed', args=[task.id])
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')

    def test_filter_by_status(self):
        Task.objects.create(title="New Task", user=self.user, status="new")
        Task.objects.create(title="Completed Task", user=self.user, status="completed")
        response = self.client.get(reverse('task_list_create') + '?status=completed', HTTP_AUTHORIZATION=self.auth_header)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['status'], 'completed')
