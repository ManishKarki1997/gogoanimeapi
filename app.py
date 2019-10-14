import requests
from bs4 import BeautifulSoup
import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return """
            <h1 style='margin-bottom:5rem;'>Each api should be called at <span> https://gogoanimeapi.herokuapp.com/api/</span></h1>
    <h3>To fetch animes of certain genres, the api endpoint is
        <i>https://gogoanimeapi.herokuapp.com/api/genre/{genre_name}/{page_number}</i> </h3>
    <h3>To search for certain anime, the api endpoint is https://gogoanimeapi.herokuapp.com/api/search/{anime_name}</h3>
    <i>for eg. https://gogoanimeapi.herokuapp.com/api/search/Hunter X Hunter</i>
    <p>Note that You get a unique anime_id for each anime that you can use to search for that anime below.</p>
    <h3>To fetch details of an anime, the api endpoint is <i>
            https://gogoanimeapi.herokuapp.com/api/anime/{anime-id}</i></h3>
    <i>for eg. https://gogoanimeapi.herokuapp.com/api/anime/hunter-hunter</i>
    <h3>To fetch video links of an episode, the api endpoint is <i>
            https://gogoanimeapi.herokuapp.com/api/watch/{anime_id}/{episode_number}</i></h3>
    <i>for eg. https://gogoanimeapi.herokuapp.com/api/anime/hunter-x-hunter/20</i>
    """


class AnimeSearch(Resource):
    def get(self, name):
        anime_results = []
        # url_formatted_name = '%20'.join(name.split())
        result = requests.get(
            'https://www9.gogoanime.io//search.html?keyword=' + name)

        site_content = result.content

        soup = BeautifulSoup(site_content, 'lxml')
        items = soup.find_all('ul', {'class': 'items'})

        for item in items:
            for list in item.find_all('li'):

                anime_title = list.a.get('title')
                anime_poster = list.a.img['src']
                anime_id = list.a.get('href')

                anime = {'anime_title': anime_title,
                         'anime_poster': anime_poster, 'anime_id': anime_id[10:]}
                anime_results.append(anime)

        return anime_results, 200


class AnimeDetail(Resource):
    def get(self, animeId):
        URL = 'https://www9.gogoanime.io/category/' + animeId
        response = requests.get(URL)
        data = response.content

        soup = BeautifulSoup(data, 'lxml')
        anime_episodes = soup.find('ul', {'id': 'episode_page'})

        total_episodes = anime_episodes.li.a.get('ep_end')

        anime_info = soup.find('div', {'class': 'anime_info_body_bg'})
        anime_plot_wrapper = anime_info.find_all('p', {'class': 'type'})

        anime_plot = ''
        anime_status = ''
        anime_released_date = ''
        anime_genre = []
        anime_name = soup.find('h1').get_text()
        anime_id = soup.find(
            'link', {'rel': 'alternate'}).get('href')[10:]

        for item in anime_plot_wrapper:
            if('Plot Summary: ' in item.span.text):
                anime_plot = item.text[14:]

            if('Released: ' in item.span.text):
                anime_released_date = item.text[10:]

            if('Status: ' in item.span.text):
                anime_status = item.text[8:]

            if('Genre: ' in item.span.text):

                genre_lists = item.find_all('a')

                for genre in genre_lists:
                    anime_genre.append(genre.get('title'))

        anime_detail = {'anime_name': anime_name, 'anime_id': anime_id, 'anime_status': anime_status, 'anime_genre': anime_genre, 'released_date': anime_released_date, 'total_episodes': total_episodes,
                        'anime_plot': anime_plot}

        return anime_detail, 200


class AnimeLinks(Resource):
    def get(self, anime_id, anime_episode):

        site_url = "https://www9.gogoanime.io/" + \
            anime_id + '-episode-' + anime_episode
        print(site_url)
        result = requests.get(site_url)
        site_content = result.content

        soup = BeautifulSoup(site_content, 'lxml')
        links = soup.find_all("a")

        watchable_links = []

        for link in links:
            if(link.get('data-video')):
                watchable_links.append(link.get('data-video'))

        return watchable_links, 200


class AnimeGenre(Resource):
    def get(self, genre, page_number):
        if(page_number == None):
            page_number = 1

        anime_results = []
        result = requests.get(
            'https://www9.gogoanime.io/genre/' + genre + '?page=' + page_number)

        site_content = result.content

        soup = BeautifulSoup(site_content, 'lxml')
        items = soup.find_all('ul', {'class': 'items'})

        pagination = soup.find('ul', {'class': 'pagination-list'})
        pagination_list = []
        for pag in pagination:
            pagination_list.append(pag.a.get('data-page'))

        for item in items:
            for list in item.find_all('li'):

                anime_title = list.a.get('title')
                anime_poster = list.a.img['src']
                anime_id = list.a.get('href')

                anime = {'anime_title': anime_title,
                         'anime_poster': anime_poster, 'anime_id': anime_id[10:]}
                anime_results.append(anime)

        current_page = soup.find(
            'li', {'class': 'selected'}).a.get('data-page')

        to_send_data = {'current_page': current_page, 'total_pages': max(
            pagination_list), 'animes': anime_results}
        return to_send_data, 200


api.add_resource(AnimeSearch, '/api/search/<string:name>')
api.add_resource(AnimeDetail, '/api/anime/<string:animeId>')
api.add_resource(
    AnimeLinks, '/api/watch/<string:anime_id>/<string:anime_episode>')
api.add_resource(AnimeGenre, '/api/genre/<string:genre>/<string:page_number>')


# app.run(debug=True)
if __name__ == '__main__':
    app.run()
