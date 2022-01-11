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

def get_contribution(username,account_created):
    contribution_data = {}
    user = GithubUser(username)


    year = get_current_year()
    data_contr_years = []
    years_label = []


    while int(account_created[0:4]) <= year:
        get_current_year_contr =  user.contributions(start_date='{}-01-01'.format(year), end_date='{}-12-31'.format(year))
        data =  sum([day.count for day in get_current_year_contr.days])
        data_contr_years.append(data)
        years_label.append(str(year))
        year-=1


    contribution_data["years_label"] = years_label[::-1]
    contribution_data['years_data'] = data_contr_years[::-1]
    contribution_data['this_year'] = data_contr_years[0]
    contribution_data['last_year'] = data_contr_years[1]
    contribution_data['sum'] = sum(data_contr_years)

    return contribution_data

def get_current_year():
    return (date.today()).year

def get_current_month():
    return (date.today()).month

def get_today_date():
    return (date.today()).strftime("%y-%m-%d")

def prepare_data(username,data_profile,data_repos):
    data_combined = {}
    repos_name = []

    for i in range(len(CONST_KEYS)):
        data_combined[CONST_KEYS[i]] = data_profile[CONST_KEYS[i]]
    
    for j in range(len(data_repos)):
        if j == 50:
            break;
        repos_name.append(data_repos[j]['name'])

    data_combined['repos_name'] = repos_name
    data_combined['contribution'] = get_contribution(username,(data_profile["created_at"]).split("T")[0])
    return data_combined

