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
        token = self.authenticate('user_0', 'easypass0')
        print(self.get_posts(token))
        # get posts by user: localhost:8000/api/posts?author=1
        # get likes of post: localhost:8000/api/likes?post=1

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

    # def get_users(token):
    #     """
    #     Get list of all users
    #     :param token:
    #     :return:
    #     """
    #     r = requests.get(BASE_URL + 'users/', headers={'Authorization': token})
    #     return json.loads(r.content.decode('utf-8'))

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
        r = requests.get('http://' + self.BASE_URL + f'/api/posts/post={post_id}', headers={'Authorization': 'Bearer ' + token})
        return json.loads(r.content.decode('utf-8'))

    def user_has_post_zero_likes(self, token, user_id):
        post = self.get_posts_by_user(token, user_id)
        for p in post:
            likes = self.get_likes_by_post(token, p['id'])
            if len(likes) == 0:
                return True
        return False

    def check_finished(self, token, users):


    # def userLike(user):
    #     """
    #     Like post as a user
    #     :param user:
    #     :return:
    #     """
    #     liked = 0
    #     username = user['username']
    #     token = authenticate(username, 'easypass' + username[-1])
    #     posts = get_posts(token)
    #
    #     while liked < config.MAX_LIKES_PER_USER:
    #         r = requests.get(BASE_URL + 'likes/', headers={'Authorization': token})
    #         likes = json.loads(r.content.decode('utf-8'))
    #
    #         single_post = random.choice(posts)
    #         post_id = str(single_post['id'])
    #         author = single_post['author']
    #
    #         # prevent liking of own post and admins post
    #         if author != user['id'] and author != 1:
    #             for l in likes:
    #                 # case when user has already liked the post
    #                 if l[0] == single_post['id'] and l[1] == user['id']:
    #                     continue
    #
    #                 # checking if user has at least one post without like
    #                 user_posts = [x['id'] for x in posts if x['author'] == author]
    #                 user_posts_count = len(user_posts)
    #                 liked_posts_of_user = len(set([x[0] for x in likes if x[0] in user_posts]))
    #                 if user_posts_count == liked_posts_of_user:
    #                     continue
    #
    #             r = requests.post(BASE_URL + 'likes/' + post_id + '/', headers={'Authorization': token})
    #             print("Liking post " + post_id + " as user" + str(user['id']) + ": ", r.status_code)
    #             liked += 1
    #
    # def likePosts(posts, token):
    #     """
    #     Iterate over list of users and call user like function
    #     :param posts:
    #     :param token:
    #     :return:
    #     """
    #     posts_by_author_list = [k['author'] for k in posts if k.get('author') and k.get('author') != 1]
    #     posts_by_author_count = Counter(posts_by_author_list)
    #     for post_count in posts_by_author_count.most_common():
    #         r = requests.get(BASE_URL + 'users/' + str(post_count[0]) + '/', headers={'Authorization': token})
    #         user = json.loads(r.content.decode('utf-8'))
    #         userLike(user)
    #
