from django.core.management.base import BaseCommand, CommandError
from apps.users.models import User
from apps.users.models import Like
import requests, json, sys, os, random
# import config
from urllib import request, parse
from collections import Counter
from decouple import config
import django.core.management.commands.runserver as runserver


class Command(BaseCommand):
    help = 'Create User, Posts and Likes all the while testing our humble app'
    BASE_URL = os.getenv('BASE_URL', config('BASE_URL'))

    users = {'user_0': {'email': 'misha+0@interglider.com', 'password': 'easypass0', 'likes': 0, 'posts_num': 2},
             'user_1': {'email': 'misha+1@interglider.com', 'password': 'easypass1', 'likes': 0, 'posts_num': 8},
             'user_2': {'email': 'misha+2@interglider.com', 'password': 'easypass2', 'likes': 0, 'posts_num': 5},
             'user_3': {'email': 'misha+3@interglider.com', 'password': 'easypass3', 'likes': 0, 'posts_num': 6},
             'user_4': {'email': 'misha+4@interglider.com', 'password': 'easypass4', 'likes': 0, 'posts_num': 3},
             'user_5': {'email': 'misha+5@interglider.com', 'password': 'easypass5', 'likes': 0, 'posts_num': 8},
             'user_6': {'email': 'misha+6@interglider.com', 'password': 'easypass6', 'likes': 0, 'posts_num': 9},
             'user_7': {'email': 'misha+7@interglider.com', 'password': 'easypass7', 'likes': 0, 'posts_num': 8},
             'user_8': {'email': 'misha+8@interglider.com', 'password': 'easypass8', 'likes': 0, 'posts_num': 4},
             'user_9': {'email': 'misha+9@interglider.com', 'password': 'easypass9', 'likes': 0, 'posts_num': 8},
             'user_10': {'email': 'misha+10@interglider.com', 'password': 'easypass10', 'likes': 0, 'posts_num': 4},
             'user_11': {'email': 'misha+11@interglider.com', 'password': 'easypass11', 'likes': 0, 'posts_num': 9}
             }


    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS', config('NUMBER_OF_USERS')))
        MAX_POSTS_PER_USER = int(os.getenv('MAX_POSTS_PER_USER', config('MAX_POSTS_PER_USER')))
        MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER', config('MAX_LIKES_PER_USER')))

        # create users according to NUMBER_OF_USERS param
        # users = self.make_users(NUMBER_OF_USERS)

        # for key, value in users.items():
        #     token = self.authenticate(key, users[key]['password'])
        #     # use token to make random number of posts
        #     num_posts = self.make_posts(key, token, MAX_POSTS_PER_USER)
        #     # update users dict
        #     users[key]['posts_num'] = num_posts

        # order users by the number of posts
        temp_list = []
        for k, v in self.users.items():
            temp_list.append([k, self.users[k]['password'], self.users[k]['posts_num']])
        users_order = [[x[0], x[1]] for x in reversed(sorted(temp_list, key=lambda x: x[2]))]

        done = False
        while not done:
            done = self.like_posts(users_order, MAX_LIKES_PER_USER)

    def authenticate(self, user, password):
        """
        Login as user
        :param user:
        :param password:
        :return:
        """
        data = {
            'username': user,
            'password': password
        }

        req = request.Request('http://' + self.BASE_URL + '/api/token/')

        with request.urlopen(req, data=parse.urlencode(data).encode('utf-8')) as f:
            resp = f.read()
            resp_dict = json.loads(resp)

        return resp_dict['access']

    def make_users(self, NUMBER_OF_USERS):
        """
        Create users
        :param num_users:
        :param token:
        :return:
        """
        users = {}
        for i in range(NUMBER_OF_USERS):
            num = str(i)
            username = "user_" + num
            password = "easypass" + num
            email = "misha+" + num + "@interglider.com"
            data = {
                "username": username,
                "email": email,
                "password": password
            }

            r = requests.post('http://' + self.BASE_URL + '/api/users', data=data)
            print(f"Creating user: {num} ", r.status_code)
            users[username] = {'email': email, 'password': password, 'likes': 0, 'posts_num': 0}
        return users

    def get_users(self, token):
        """
        Get list of all users
        :param token:
        :return:
        """
        r = requests.get('http://' + BASE_URL + '/api/users/', headers={'Authorization': token})
        return json.loads(r.content.decode('utf-8'))

    def make_posts(self, username, token, MAX_POSTS_PER_USER):
        """
        Create posts as each user from list in random number
        :param users:
        :return:
        """
        posts_to_make = random.randrange(1, MAX_POSTS_PER_USER)

        for i in range(posts_to_make):
            num = ''.join(random.choice('1234567890') for x in range(12))
            code = num + ' ' + username
            data = {
                "title": "Test Title " + code,
                "lead": "Test Lead " + code,
                "text": "Test Text " + code,
                "public": True,
                "language": "en",
                "authot": username
            }

            r = requests.post('http://' + self.BASE_URL + '/api/posts/', data=data, headers={'Authorization': 'Bearer ' + token})
            print("Creating post as user " + username + ": ", r.status_code)

        return posts_to_make

    def get_posts(self, token):
        """
        Get list of all posts
        :param token:
        :return:
        """
        r = requests.get('http://' + self.BASE_URL + '/api/posts/', headers={'Authorization': 'Bearer ' + token})
        return json.loads(r.content.decode('utf-8'))

    def get_posts_by_user(self, token, user_id):
        """
        Get list of all posts by user
        :param token:
        :return:
        """
        r = requests.get('http://' + self.BASE_URL + f'/api/posts/author={user_id}', headers={'Authorization': 'Bearer ' + token})
        return json.loads(r.content.decode('utf-8'))

    def get_likes_by_post(self, token, post_id):
        """
        Get list of all likes by post id
        :param token:
        :return:
        """
        r = requests.get('http://' + self.BASE_URL + f'/api/likes/post={post_id}', headers={'Authorization': 'Bearer ' + token})
        likes = json.loads(r.content.decode('utf-8'))
        return likes

    def post_liked_by_user(self, token, post_id, user_id):
        r = requests.get('http://' + self.BASE_URL + f'/api/likes/post={post_id}&user={user_id}', headers={'Authorization': 'Bearer ' + token})
        likes = json.loads(r.content.decode('utf-8'))
        if len(likes) != []:
            return True
        return False

    def user_has_post_zero_likes(self, token, user_id):
        post = self.get_posts_by_user(token, user_id)
        for p in post:
            likes = self.get_likes_by_post(token, p['id'])
            if len(likes) == 0:
                return True
        return False

    def is_finished(self, token):
        posts = self.get_posts(token)
        for post in posts:
            likes = self.get_likes_by_post(token, post['id'])
            if len(likes) == 0:
                return True
        return False

    def do_like(self, token, post_id):
        r = requests.post('http://' + self.BASE_URL + f'/api/likes/post={post_id}', headers={'Authorization': 'Bearer ' + token})
        try:
            if 'error' in json.loads(r.content.decode('utf-8')):
                return False
        except Exception as e:
            return True


    def like_posts(self, users, MAX_LIKES_PER_USER):
        for u in users:
            token = self.authenticate(u[0], u[1])
            likes = 0
            while likes < MAX_LIKES_PER_USER or self.is_finished(token) is False:
                users = self.get_users(token)
                for user in users:
                    if self.user_has_post_zero_likes(token, user[0]):
                        user_posts = self.get_posts_by_user(token, user[0])
                        liked = False
                        while liked == False:
                            post = random.choice(user_posts)
                            if self.post_liked_by_user(token, post['id'], user[0]):
                                if self.do_like(token, post['id']):
                                    likes += 1

        return self.is_finished(token)
