from github_contributions import GithubUser
user = GithubUser("torvalds")
from datetime import date

def get_current_year():
    return (date.today()).year

total_year = 5
year = get_current_year()
data_contr_years = []
while total_year != 0:
    if int(2011) <= year:
        get_current_year_contr = last_year = user.contributions(start_date='{}-01-01'.format(year), end_date='{}-12-31'.format(year))
        data_contr_years.append(sum([day.count for day in get_current_year_contr.days]))
        total_year-=1
        year-=1
    else:
        break
print(data_contr_years)

