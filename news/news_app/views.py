from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

# links to news's webpages
yle = 'https://yle.fi/uutiset/tuoreimmat'
mz = 'https://meduza.io/en'

# create lists for storing future data
yle_data = []
mz_data = []

# function to extract data from first web page
def get_yle():
    r = requests.get(yle).text
    soup = BeautifulSoup(r, 'lxml')
    posts = soup.find_all('div', class_="FullWidthColorBand-sc-1hsyrgw-0 ExpandingHeadline__AlignedColorContainer-sc-d7qzpy-1 gyhLQW dlIrRV")

    # loop for getting tiles, links to the latiest news
    for post in posts:
        title = post.find('h6').text
        link = post.find('a', class_='GridSystem__GridRow-sc-15162af-1 xJCCA visitableLink').get('href')
        if 'https' in link:
            work_link = link
        else:
            work_link = 'https://yle.fi' + link

        time = post.find('time').text
        # make a dictionary for every article
        data = {
            'title': title,
            'link': work_link,
            'post_time': time
        }
        yle_data.append(data)


# function to extract data from another news resource
def get_mz():
    r = requests.get(mz).text
    soup = BeautifulSoup(r, 'lxml')
    posts = soup.find_all('h2')
     # loop for getting tiles, links to the latiest news
    for post in posts:
        title_1 = post.find_next('span')
        title_head = title_1.text
        title_2 = title_1.find_next('span')
        title_body = title_2.text
        title = title_head + title_body
        link = post.find('a').get('href')
        work_link = 'https://meduza.io'+ link
        data = {
            'title': title,
            'link': work_link
        }
        mz_data.append(data)

# call the function
get_yle()
get_mz()


# function corresponding for rendering
def home(request):
    content = {
        'yle_data': yle_data,
        'mz_data': mz_data
    }
    return render(request, 'news_app/home.html', content)
