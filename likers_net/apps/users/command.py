from django.core.management.base import BaseCommand, CommandError
from .models import User
from .models import Like
import requests
import config
import json
import random
import sys
from urllib import request, parse
from collections import Counter


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        pass

    # BASE_URL = 'http://127.0.0.1:8000/'
    #
    # def authenticate(user, password):
    #     """
    #     Login as user
    #     :param user:
    #     :param password:
    #     :return:
    #     """
    #     data = {
    #         'username': user,
    #         'password': password
    #     }
    #
    #     req = request.Request(BASE_URL + 'api-token-auth/')
    #
    #     with request.urlopen(req, data=parse.urlencode(data).encode('utf-8')) as f:
    #         resp = f.read()
    #         resp_dict = json.loads(resp)
    #
    #     return "JWT " + resp_dict['token']
    #
    # def make_users(num_users, token):
    #     """
    #     Create users
    #     :param num_users:
    #     :param token:
    #     :return:
    #     """
    #     for i in range(num_users):
    #         num = str(i)
    #         data = {
    #             "username": "user_" + num,
    #             "email": "misha+" + num + "@interglider.com",
    #             "password": "easypass" + num,
    #             "groups": []
    #         }
    #
    #         r = requests.post(BASE_URL + 'users/', data=data, headers={'Authorization': token})
    #         print("Creating user: ", r.status_code)
    #
    # def get_users(token):
    #     """
    #     Get list of all users
    #     :param token:
    #     :return:
    #     """
    #     r = requests.get(BASE_URL + 'users/', headers={'Authorization': token})
    #     return json.loads(r.content.decode('utf-8'))
    #
    # def make_posts(users):
    #     """
    #     Create posts as each user from list in random number
    #     :param users:
    #     :return:
    #     """
    #     for user in users:
    #         if user['id'] != 1:
    #             posts_to_make = random.randrange(1, config.MAX_POSTS_PER_USER)
    #             token = authenticate(user['username'], 'easypass' + user['username'][-1])
    #             user_id = str(user['id'])
    #
    #             for i in range(posts_to_make):
    #                 num = ''.join(random.choice('1234567890') for x in range(12))
    #                 code = num + user_id
    #                 data = {
    #                     "title": "Test Title " + code,
    #                     "lead": "Test Lead " + code,
    #                     "text": "Test Text " + code,
    #                     "public": True,
    #                     "language": "en",
    #                     "author": user_id
    #                 }
    #
    #                 r = requests.post(BASE_URL + 'posts/', data=data, headers={'Authorization': token})
    #                 print("Creating post as user " + user_id + ": ", r.status_code)
    #
    # def get_posts(token):
    #     """
    #     Get list of all posts
    #     :param token:
    #     :return:
    #     """
    #     r = requests.get(BASE_URL + 'posts/', headers={'Authorization': token})
    #     return json.loads(r.content.decode('utf-8'))
    #
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
    # def main(argv):
    #     """
    #     :param argv:
    #     :return:
    #     """
    #     token = authenticate(argv[0], argv[1])
    #     make_users(config.NUMBER_OF_USERS, token)
    #     users = get_users(token)
    #     make_posts(users)
    #     token = authenticate('admin', 'celikpromet')
    #     posts = get_posts(token)
    #     likePosts(posts, token)
    #     print("Done")
