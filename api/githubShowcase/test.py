import requests
username = "xyzda"

API_URL = "https://api.github.com"
GITHUB_TOKEN = "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"
headers = {'Authorization': 'token %s' % GITHUB_TOKEN}
r_profile = requests.get(API_URL + "/users/{}".format(username),headers=headers)
r_repos = requests.get(API_URL+"/users/{}/repos".format(username),headers=headers)

print(r_profile.status_code)