from datetime import date
from github_contributions import GithubUser

CONST_KEYS = [
    "html_url",
    "avatar_url",
    "name",
    "company",
    "location",
    "bio",
    "public_repos",
    "followers",
    "following",
    "created_at",
    "login"
]


def get_current_year():
    return (date.today()).year

def get_current_month():
    return (date.today()).month

def get_current_year_contribution(username):
    user = GithubUser(username)
    this_year = user.contributions(start_date='{}-01-01'.format(get_current_year()), end_date='{}-12-31'.format(get_current_year()))
    return sum([day.count for day in this_year.days])

