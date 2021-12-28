from django.shortcuts import render
import requests

def get_data(username):

    data_combined_profile = {}
    repos_name = []
    def prepare_data_profile(data):
        CONST_KEYS = ["html_url","avatar_url","name","company","location","bio","public_repos","followers","following","created_at","login"]
        for i in range(len(CONST_KEYS)):
            data_combined_profile[CONST_KEYS[i]] = data[CONST_KEYS[i]]
        
        for j in range(len(repos_data.json())):
            if j == 50:
                break;
            repos_name.append(repos_data.json()[j]['name'])

        data_combined_profile['repos_name'] = repos_name

    # try:
    repos_data = requests.get("https://api.github.com/users/{}/repos".format(username))
    profile_data = requests.get("https://api.github.com/users/{}".format(username))
    if repos_data.status_code or profile_data.status_code == 403:
        return {"RateLimits":True}
    else:
        prepare_data_profile(profile_data.json())
    # except:
    #     return None

    return data_combined_profile
