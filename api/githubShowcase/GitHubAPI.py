import requests
from . import Constants as CONST

def get_data(username):

    data_combined_profile = {}
    repos_name = []
    def prepare_data_profile(data):

        for i in range(len(CONST.CONST_KEYS)):
            data_combined_profile[CONST.CONST_KEYS[i]] = data[CONST.CONST_KEYS[i]]
        
        for j in range(len(r_repos.json())):
            if j == 50:
                break;
            repos_name.append(r_repos.json()[j]['name'])

        data_combined_profile['repos_name'] = repos_name
        data_combined_profile['current_year_contr'] = CONST.get_current_year_contribution(username)

        return data_combined_profile

    # try:
    API_URL = "https://api.github.com"
    GITHUB_TOKEN = "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"
    headers = {'Authorization': 'token %s' % GITHUB_TOKEN}
    r_profile = requests.get(API_URL + "/users/{}".format(username),headers=headers)
    r_repos = requests.get(API_URL+"/users/{}/repos".format(username),headers=headers)

    if r_profile.status_code and r_repos.status_code == 200:
        return prepare_data_profile(r_profile.json())
    else:
        return {"RateLimits":True}
    # except:
    #     return None
