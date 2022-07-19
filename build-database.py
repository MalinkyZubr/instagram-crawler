import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from py2neo import Graph
import instaloader
import csv
import os
import json
import multiprocessing

pwd = os.path.dirname(os.path.abspath(__file__))

class databaseBuilder:
    def __init__(self):
        self.cypher_file = os.path.join(pwd, r'user_database.cypher')

    def create_user(self, user_info:dict):
        expression = '''CREATE ({username:}:USER\{
                        userid:{user_id:}, 
                        fullname:{full_name:}, 
                        username:{username:}, 
                        isprivate:{is_private:}, 
                        isverified:{is_verified:}, 
                        mediacount:{media_count:}, 
                        numfollowers:{num_followers:}, 
                        numfollowing:{num_following:}
                        \})
                    '''
        for key, value in user_info:
            expression.format(key=value)

        return expression

    def create_relationship(self, node_1, node_2, relationship):
        expression = f'''{node_1}-[:{relationship}]->{node_2}'''
        return expression

    def read_json_file(self, file_name):
        with open(file_name, 'r') as f:
            data = f.read()
            data = json.loads(data)
        return data

    def make_nodes(self, user_info_file):
        user_info_path = os.path.join(pwd, user_info_file)
        file_list = os.listdir(user_info_path)
        info = {}
        for file_name in file_list:
            user_info = self.read_json_file(file_name)
            username = user_info['username']
            user_node = self.create_user(user_info)
            info[username] = user_node

        return info

    def make_follower_relationships(self, user_follower_file, user_following_file, user_nodes: dict):
        user_follower_path = os.path.join(pwd, user_follower_file)
        user_following_path = os.path.join(pwd, user_following_file)

        for user, user_node in user_nodes.items():
            followers = read_json_file(f"{user_follower_path}/{user}_FOLLOWERS")
            following = read_json_file(f"{user_follower_path}/{user}_FOLLOWING")

            for follower in followers:
                try:
                    follower_node = user_nodes[follower]
                    relationship = self.create_relationship(user_node, follower_node, 'FOLLOWED_BY')
                    self.write_to_file(relationship, self.cypher_file)
                except IndexError:
                    continue

            for followed in following:
                try:
                    followed_node = user_nodes[followed]
                    relationship = self.create_relationship(user_node, follower_node, 'FOLLOWING')
                    self.write_to_file(relationship, self.cypher_file)
                except IndexError:
                    continue

    def write_to_file(self, expression, file_name):
        with open(file_name, 'a') as f:
            f.write(expression)

if __name__ == '__main__':
    database_builder = databaseBuilder()
    database_builder.write_to_file('//FILE STARTS HERE', database_builder.cypher_file)
        