from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth.models import  User
from .views import *
from . models import Post
from category.models import Category
from  account.views import LoginView

# Create your tests here.

class PostTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = self.setUp_user()
        self.token = self.setUp_user_token()
        self.setUp_categoy()
        self.setUp_post()

    def setUp_user(self):
        return User.objects.create_superuser(username='test', password='1')
    
    def setUp_user_token(self):
        data = {
            'username':'test',
            'password':'1'
        }

        request = self.factory.post('account/login/', data)
        
        view = LoginView.as_view()
        response = view(request)

        return response.data['token']
    
    def setUp_categoy(self):
        Category.objects.create(name='Category1')

    def setUp_post(self):
        posts = [
            Post(owner=self.user, category=Category.objects.first(), title='title1', body='body1'),
            Post(owner=self.user, category=Category.objects.first(), title='title2', body='body2'),
            Post(owner=self.user, category=Category.objects.first(), title='title3', body='body3')
        ]
         
        Post.objects.bulk_create(posts)

    def test_get_post(self):
        request = self.factory.get('post/')
        view = PostViewSet.as_view({'get':'list'})
        response = view(request)
        # print(response.data)


        assert response.status_code == 200

    def test_post_post(self):
        img = open('/home/huawei/Pictures/admin_2019_10_28_keme.jpg', 'rb')
        data = {
            'category':Category.objects.first().pk,
            'title':'test_post',
            'img':img,
            'body':'body'
        }

        request = self.factory.post('post/', data, HTTP_AUTHORIZATION ='Token ' + self.token)

        img.close()
        view = PostViewSet.as_view({'post':'create'})
        response = view(request)
    
        assert response.status_code == 201
        assert response.data['owner'] == self.user.username
        