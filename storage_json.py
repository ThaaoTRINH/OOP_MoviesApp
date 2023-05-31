from istorage import IStorage
import requests
import json
import statistics
import random
import matplotlib.pyplot as plt

file_source = "data.json"

class StorageJson(IStorage):

    def __init__(self, file_path):
        self.file_path = file_path
        self.movies = self.get_data()
        self.length = len(self.movies)

    @staticmethod
    def get_data():
        with open(file_source, "r") as handle:
            datas = json.loads(handle.read())
        return datas

    @staticmethod
    def save_to_json(movies):
        new_data = json.dumps(movies)
        with open("data.json", "w") as handle:
            handle.write(new_data)

    def list_movies(self):
        n = 1
        print('LIST ALL MOVIES')
        for movie in self.movies:
            for key, value in movie.items():
                print(f'{n}. {key.upper()} | Rating: {value["rating"]} | '
                      f'Actors: {value["actors"]}')
                n += 1

    def check_movie_exist(self, title):
        movie_name_list = []
        for movie in self.movies:
            for movie_title in movie.keys():
                movie_name_list.append(movie_title.upper())
        if title.upper() in movie_name_list:
            return True

    @staticmethod
    def input_movie():
        while True:
            movie_title = input("Add a movie title: ")
            if not movie_title:
                print('Movie title is required! ')
                continue
            try:
                movie_title.upper()
            except ValueError:
                print('Invalid! Input again pls')
                continue
            return movie_title.upper()

    def add_movie(self):
        title = self.input_movie()
        print('Title input: ', title)
        if self.check_movie_exist(title):
            print(f'Movie {title} was already exist')
            return self.input_movie()
        else:
            url = 'https://www.omdbapi.com/?apikey=99b0f16a&t=' + f'{title}'
            data = requests.get(url)
            data = data.json()
            print(data)
            movie_title = data['Title'].upper()
            year_release = data['Year']
            rating = data['imdbRating']
            director = data['Director']
            actors = data['Actors']
            awards = data['Awards']
            genre = data['Genre']
            content = data['Plot']

            movie = {
                movie_title: {
                    'year': year_release,
                    'rating': rating,
                    'director': director,
                    'actors': actors,
                    'awards': awards,
                    'genre': genre,
                    'content': content,
                }
            }
            self.movies.append(movie)
            self.save_to_json(self.movies)
            print(f'Movie {movie_title} successfully added')

    def delete_movie(self):
        print('----- DELETE A MOVIE -----')
        title = self.input_movie()
        if self.check_movie_exist(title):
            for movie in self.movies:
                for key, value in movie.items():
                    if key == title:
                        self.movies.remove(movie)
            print(f'Movie "{title}" successfully deleted.')
        else:
            print(f'Movie "{title}" does not exist.')
        self.save_to_json(self.movies)
        print("-----------------")

    def update_movie(self):
        print('----- UPDATE A MOVIE -----')
        title = self.input_movie()
        self.check_movie_exist(title)
        try:
            new_rating = float(input("Enter a new rating: "))
        except ValueError:
            print('Invalid number" Try again!')
            return

        for movie in self.movies:
            for key, value in movie.items():
                if title.upper() == key:
                    value['rating'] = new_rating

        self.save_to_json(self.movies)
        print(f'A new rating of movie {title.upper()} already updated')
        print("-----------------")

    def stats_movie(self):
        rating_list = []
        for movie in self.movies:
            for key, value in movie.items():
                rating_list.append(float(value['rating']))

        print(f'Average rating: {round(sum(rating_list)/self.length,2)}')
        print(f'Median rating: {statistics.median(rating_list)}')
        print(f'Highest rating: {max(rating_list)}')
        print(f'Lowest rating: {min(rating_list)}')

    def random_movie(self):
        random_movie = random.choice(self.movies)
        for key, value in random_movie.items():
            print(f"Your movie for tonight: '\033[1m'\033[96m{key.upper()}. It's rated {value['rating']}'"
                  f"\033[0m\033[00m'\nActors: {value['actors']} \n'\033[3m {value['content']}\033[0m")

    def search_movie(self):
        print('SEARCH MOVIE')
        movie_name = input("Enter movie name (enter for skip) : ")
        movie_rating = 0
        while True:
            movie_rating_input = input("Enter rating (enter for skip) : ")
            if movie_rating_input == '':
                break
            try:
                movie_rating = float(movie_rating_input)
                break
            except ValueError:
                print('Invalid! Re-enter: ')
        movie_actor = input("Enter actor (enter for skip) : ")
        movie_director = input("Enter director (enter for skip) : ")
        movie_genre = input("Enter movie genre (enter for skip) : ")
        print('--------------------------------------------------------------------------------------')
        for movie in self.movies:
            for key, value in movie.items():
                display = f'{key.upper()} was release in {value["year"]} and rating is {value["rating"]} \n' \
                          f'. Director: {value["director"]} | Actors: {value["actors"]}'
                if key.upper() == movie_name.upper():
                    print(display)
                elif (movie_rating != 0) and (float(value["rating"]) >= movie_rating):
                    print(display)
                elif movie_actor and (movie_actor.upper() in value['actors'].upper()):
                    print(display)
                elif movie_director and (movie_director.upper() in value['director'].upper()):
                    print(display)
                elif movie_genre and (movie_genre.upper() in value['genre'].upper()):
                    print(display)
        print('--------------------------------------------------------------------------------------')

    def sort_movies(self):
        sorted_movie = sorted(self.movies, key=lambda x: float(x[list(x.keys())[0]]['rating']), reverse=True)
        print('--------------------------------------------------------------------------------------')
        print('SORT MOVIES BY THE RATING :')
        print('--------------------------------------------------------------------------------------')
        n = 1
        for movie in sorted_movie:
            for key, value in movie.items():
                print(f'{n}. {key.upper()} | Rating: {value["rating"]} | Actors: {value["actors"]}')
                n += 1

    @staticmethod
    def poster_search(movie_name):
        poster_link = ''
        url = 'https://www.omdbapi.com/?apikey=99b0f16a&t='+f'{movie_name}'
        data = requests.get(url)
        data = data.json()
        if movie_name.upper() in data['Title'].upper():
            poster_link = data['Poster']

        return poster_link

    def generate_web(self):
        # list_movies()
        output_list = []
        for movie in self.movies:
            for key, value in movie.items():
                output = ' '
                output += '<li>'
                output += '<div class ="movie">'
                output += f'<img class ="movie-poster" src = "{self.poster_search(key.lower())}" title = ""/>'
                output += f'<div class ="movie-title"> {key} </div>'
                output += f'<div class ="movie-year"> {value["year"]} </div>'
                output += f'<div class ="star">*</div>'
                output += f'<div class ="movie-year">(rating: {value["rating"]})</div>'

                output += '</div>'
                output += '</li>'
                output_list.append(output)

        outfile_name: str = 'index.html'
        html_head = """
                <html>
                <head>
                    <title>My Movie App</title>
                <link rel="stylesheet" href="style.css"/>
                </head>
                <body>
                <div class="list-movies-title">
                    <h1>My Movie App</h1>
                </div>
                <div>
                    <ol class="movie-grid">
                """

        html_end = """
    
                    </ol>
                </div>
                </body>
                </html>"""

        export_file = open(outfile_name, 'w')
        export_file.write(html_head)
        for movie in output_list:
            export_file.write(str(movie))
        export_file.write(html_end)
        export_file.close()

    def favorite_movies(self):
        movie_name_list = []
        favorite_list = []

        n = 1
        for movie in self.movies:
            for key, value in movie.items():
                movie_name_list.append(key)
                print(f'{n}. {key}')
                n += 1

        while True:
            movie_number_input = input("Enter your favorite movie # (press enter to skip): ")
            if movie_number_input == '':
                break
            else:
                movie_number = int(movie_number_input)
                favorite_list.append(movie_name_list[movie_number - 1].upper())
        output_list = []
        for movie in self.movies:
            for key, value in movie.items():
                if key.upper() in favorite_list:
                    favorite_name_movie = "&#11088;"
                else:
                    favorite_name_movie = " "
                output = ' '
                output += '<li>'
                output += '<div class ="movie">'
                output += f'<img class ="movie-poster" src = "{self.poster_search(key)}" title = ""/>'
                output += f'<div class ="movie-title"> {key} </div>'
                output += f'<div class ="movie-year"> {value["year"]} </div>'
                output += f'<div class ="movie-year">( rating: {value["rating"]} )</div>'
                output += f'<span class="favorite-movie">{favorite_name_movie}</span>'
                output += '</div>'
                output += '</li>'
                output_list.append(output)

        outfile_name: str = 'index.html'
        html_head = """
            <html>
            <head>
                <title>My Movie App</title>
            <link rel="stylesheet" href="style.css"/>
            </head>
            <body>
            <div class="list-movies-title">
                <h1>My Movie App</h1>
            </div>
            <div>
                <ol class="movie-grid">
            """

        html_end = """
    
                </ol>
            </div>
            </body>
            </html>"""

        export_file = open(outfile_name, 'w')
        export_file.write(html_head)
        for movie in output_list:
            export_file.write(str(movie))
        export_file.write(html_end)
        export_file.close()

    def movies_histogram(self):
        movie_rating_list = []
        for movie in self.movies:
            for key, value in movie.items():
                movie_rating_list.append((key, value['rating']))
        movie_names = [movie[0] for movie in movie_rating_list]
        ratings = [movie[1] for movie in movie_rating_list]

        fig, ax = plt.subplots()
        ax.bar(movie_names, ratings, color='lightblue')
        plt.xticks(rotation=90, ha="right")
        plt.xlabel("Movie Title", fontsize=12, fontweight='bold')
        plt.ylabel("Rating", fontsize=12, fontweight='bold')
        plt.title("MOVIE AND RATING HISTOGRAM", fontsize=18, fontweight='bold', color='sky-blue')

        filename = input("Enter a filename for the histogram: ")
        filetype = input("which filetype (jpeg, jpg) for the histogram ? ")
        if filetype in "eps, jpeg, jpg, pdf, pgf, png, ps, raw, rgba, svg, tif, tiff":
            file_name = filename + "." + filetype
            plt.savefig(file_name)
            plt.tight_layout()
            plt.show()
            return self.movies
        raise ValueError("Unsupported Format")
