import requests as req
from bs4 import BeautifulSoup

def request_github_trending(url):
    r = req.get(url)
    Request = r.text
    return Request

def extract(page):
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find_all('article', {'class': 'Box-row'})
    return rows

def transform(html_repos):
    data = []
    for row in html_repos:
        repos_name = row.find('h1').find('a').get('href')
        stars_num = row.find('div', {'class': 'f6 color-fg-muted mt-2'}).find('span', {'class': 'd-inline-block float-sm-right'}).text
        developers = row.find('div', {'class': 'f6 color-fg-muted mt-2'}).find('span', {'class': 'd-inline-block mr-3'}).find('a').get('href')
        data.append({
            'developer': developers[1:], 
            'repository_name': repos_name[1:], 
            'nbr_stars': stars_num[12:-1]
        })
    return data

def format(repositories_data):
    output = ['Developer, Repository name, Number of stars'] 
    for data in repositories_data:
        line = [data['developer'], data['repository_name'], data['nbr_stars']]
        output.append(', '.join(line))
    return "\n".join(output)

if __name__ == "__main__":
    url = 'https://github.com/trending'
    page = request_github_trending(url)
    html_repos = extract(page)
    repositories_data = transform(html_repos)
    format(repositories_data)

    # print(request_github_trending(url))
    # print(extract(page))
    # print(transform(html_repos))
    # print(format(repositories_data))
