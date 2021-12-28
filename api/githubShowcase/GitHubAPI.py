from os import write
import requests

def get_data(username):

    data_combined_profile = {}

    def prepare_data_profile(data):
        CONST_KEYS = ["html_url","avatar_url","name","company","location","bio","public_repos","followers","following","created_at"]
        for i in range(len(CONST_KEYS)):
            data_combined_profile[CONST_KEYS[i]] = data[CONST_KEYS[i]]
    
    #repos_data = requests.get("https://api.github.com/users/{}/repos".format(username))
    profile_data = requests.get("https://api.github.com/users/{}".format(username))
    prepare_data_profile(profile_data.json())
    return data_combined_profile

