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

    def write_to_file(self, expression, file_name):
        with open(self.cypher_file, 'a') as f:
            f.write(expression)

if __name__ == '__main__':
    database_builder = databaseBuilder()
    database_builder.write_to_file('//FILE STARTS HERE', database_builder.cypher_file)
        