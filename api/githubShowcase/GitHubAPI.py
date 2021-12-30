import requests
from . import helpers 

def get_data(username):

    try:
        API_URL = "https://api.github.com"
        GITHUB_TOKEN = "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"
        headers = {'Authorization': 'token %s' % GITHUB_TOKEN}
        r_profile = requests.get(API_URL + "/users/{}".format(username),headers=headers)
        r_repos = requests.get(API_URL+"/users/{}/repos".format(username),headers=headers)

        if r_profile.status_code and r_repos.status_code == 200:
            return helpers.prepare_data(username,r_profile.json(),r_repos.json())
        else:
            return {"RateLimits":True}
    except:
        return None

def check_github_username(username):
    API_URL = "https://api.github.com"
    GITHUB_TOKEN = "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"
    headers = {'Authorization': 'token %s' % GITHUB_TOKEN}
    r_profile = requests.get(API_URL + "/users/{}".format(username),headers=headers)

    if r_profile.status_code == 404:
        return False
    else:
        return True


