import instaloader
import os
import json
import multiprocessing
import time
import getpass

pwd = os.path.dirname(os.path.abspath(__file__))

class InstagramCrawler:
    def __init__(self, username, password):
        self.L = instaloader.Instaloader()
        self.L.login(username, password)
        print("LOGIN SUCCESS")

    def get_account_information(self, account_username:str) -> tuple:
        profile = instaloader.Profile.from_username(self.L.context, account_username)
        profile_information = {'user_id':profile.userid,
                                'full_name':profile.full_name,
                                'username':account_username,
                                'is_private':profile.is_private,
                                'is_verified':profile.is_verified,
                                'media_count':profile.mediacount,
                                'num_followers':profile.followers,
                                'num_following':profile.followees}
  
        # create generator objects for follower and followee list
        if not profile_information['is_private']:
            followers_unprocessed = profile.get_followers()
            followees_unprocessed = profile.get_followees()

            followers = (user.username for user in followers_unprocessed)
            following = (user.username for user in followees_unprocessed)

        return (profile_information, followers, following)

    def retrieve_follow_information(self, followers, following):
        followers = [user for user in followers]
        following = [user for user in following]

        return (followers, following)

    def write_json(self, file_name, contents):
        json_content = json.dumps(contents)
        with open(file_name, 'w') as f:
            f.write(json_content)
            
    def write_file(self, username):
        user_information_file = os.path.join(r'instagram-analytics\user_information', f'{username}_INFO.json') 
        user_followers_file = os.path.join(r'instagram-analytics\user_followers', f'{username}_FOLLOWERS.json')
        user_following_file = os.path.join(r'instagram-analytics\user_following', f'{username}_FOLLOWING.json')

        info, followers_unprocessed, following_unprocessed = self.get_account_information(username)
        followers, following = self.retrieve_follow_information(followers_unprocessed, following_unprocessed)

        self.write_json(user_information_file, info)
        self.write_json(user_followers_file, followers)
        self.write_json(user_following_file, following)

    def write_files(self, usernames: list, batch_size):
        usernames_processes = [multiprocessing.Process(target=self.write_file, args=[username]) for username in usernames]

        while usernames_processes:
            print("STARTING NEXT BATCH")
            if len(usernames_processes) >= batch_size:
                batch = usernames_processes[:batch_size]
            else:
                batch = usernames_processes
                usernames_processes = False
            
            for process in batch:
                print(f'Starting {process}')
                process.start()
                if usernames_processes is not False:
                    usernames_processes.remove(process)
            
            for process in batch:
                map(lambda x: x.join(), batch)
            
            batch = None

if __name__ == '__main__':
    username = str(input("enter username: "))
    password = getpass.getpass(prompt='Password: ', stream=None)
    instagram_crawler = InstagramCrawler(username, password)
    #instagram_crawler.write_files(['luke.m.monson'], 10)

    with open(r'C:\Users\ahuma\Desktop\python projects\Misc Projects\instagram-analytics\user_followers\luke.m.monson_FOLLOWERS.json', 'r') as f:
        users = json.loads(f.read())
    instagram_crawler.write_files(users, 1) 



