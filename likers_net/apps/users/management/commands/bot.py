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

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS', config('NUMBER_OF_USERS')))
        MAX_POSTS_PER_USER = int(os.getenv('MAX_POSTS_PER_USER', config('MAX_POSTS_PER_USER')))
        MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER', config('MAX_LIKES_PER_USER')))

        if MAX_POSTS_PER_USER < MAX_LIKES_PER_USER:
            return "Likes per user must be less than max posts value if this script is to ever finish :)"

        # create users according to NUMBER_OF_USERS param
        users = self.make_users(NUMBER_OF_USERS)

        user_ids = []
        for key, value in users.items():
            token = self.authenticate(key, users[key]['password'])
            if user_ids == []:
                user_ids = self.get_users(token)
            for user_id in user_ids:
                if user_id[1] == key:
                    users[key]['id'] = user_id[0]
            # use token to make random number of posts
            num_posts = self.make_posts(key, token, MAX_POSTS_PER_USER)
            # update users dict
            users[key]['posts_num'] = num_posts

        print('List of users: ', users)

        # order users by the number of posts
        temp_list = []
        for k, v in users.items():
            temp_list.append([k, users[k]['password'], users[k]['id'], users[k]['posts_num']])
        users_order = [[x[0], x[1], x[2]] for x in reversed(sorted(temp_list, key=lambda x: x[3]))]

        print('Users order: ', users_order)

        done = False
        while not done:
            done = self.like_posts(users_order, MAX_LIKES_PER_USER)

        print('Have a nice day!')

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
        r = requests.get('http://' + self.BASE_URL + '/api/users', headers={'Authorization': token})
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
        r = requests.get('http://' + self.BASE_URL + f'/api/posts?author={user_id}', headers={'Authorization': 'Bearer ' + token})
        return json.loads(r.content.decode('utf-8'))

    def get_likes_by_post(self, token, post_id):
        """
        Get list of all likes by post id
        :param token:
        :return:
        """
        r = requests.get('http://' + self.BASE_URL + f'/api/likes?post={post_id}', headers={'Authorization': 'Bearer ' + token})
        likes = json.loads(r.content.decode('utf-8'))
        return likes

    def post_liked_by_user(self, token, post_id, user_id):
        """
        Check if post is lieked by a user
        :param token:
        :param post_id:
        :param user_id:
        :return:
        """
        r = requests.get('http://' + self.BASE_URL + f'/api/likes?post={post_id}&user={user_id}', headers={'Authorization': 'Bearer ' + token})
        likes = json.loads(r.content.decode('utf-8'))
        if len(likes) != []:
            return True
        return False

    def user_has_post_zero_likes(self, token, user_id):
        """
        Check is user has posts which has no likes
        :param token:
        :param user_id:
        :return:
        """
        posts = self.get_posts_by_user(token, user_id)
        for post in posts:
            likes = self.get_likes_by_post(token, post['id'])
            if len(likes) == 0:
                return True
        return False

    def is_finished(self, token):
        """
        Check if there are no posts which have no likes, which is end goal of the bot
        :param token:
        :return:
        """
        posts = self.get_posts(token)
        for post in posts:
            likes = self.get_likes_by_post(token, post['id'])
            if len(likes) == 0:
                return True
        return False

    def do_like(self, token, post_id):
        """
        Like post as a user
        :param token:
        :param post_id:
        :return:
        """
        try:
            r = requests.post('http://' + self.BASE_URL + f'/api/likes/{post_id}', headers={'Authorization': 'Bearer ' + token})
            print(f'Post {post_id} is liked!')
            return True
        except Exception as e:
            return False

    def like_posts(self, users, MAX_LIKES_PER_USER):
        """
        Like posts by other users until there are no posts without a like
        :param users:
        :param MAX_LIKES_PER_USER:
        :return:
        """
        token = None
        # iterate over users
        for user in users:
            print('Activating user ', user[0])
            token = self.authenticate(user[0], user[1])
            likes = 0
            # like till max likes number is reached
            while likes < MAX_LIKES_PER_USER:
                # like posts by other users
                for other_user in users:
                    if self.user_has_post_zero_likes(token, other_user[2]):
                        user_posts = self.get_posts_by_user(token, other_user[2])
                        liked = False
                        # pick one post randomly and try to like
                        while liked == False:
                            post = random.choice(user_posts)
                            if self.post_liked_by_user(token, post['id'], user[2]):
                                if self.do_like(token, post['id']):
                                    likes += 1
                                    liked = True
        if not token:
            token = self.authenticate(users[0][0], users[0][1])
        return self.is_finished(token)
