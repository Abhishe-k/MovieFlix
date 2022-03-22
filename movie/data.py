from .models import movie, actor
import imdb
NO_OF_MOVIES = 1000

class Data:

    movies = []

    def load_actors(self, m, movie_id):
        ia = imdb.IMDb()
        print('actors')
        print(actor.objects.filter(movieId=movie_id))

        # act = actor.objects.filter(movieId=movie_id)
        #
        actor1 = ''
        actor2 = ''
        actor3 = ''

        temp = None

        if 'cast' in m.keys():
            if len(m['cast']) >= 3:
                print("1st")
                actor1 = m['cast'][0].personID
                actor2 = m['cast'][1].personID
                actor3 = m['cast'][2].personID

            if len(m['cast']) == 2:
                print("2nd")
                actor1 = m['cast'][0].personID
                actor2 = m['cast'][1].personID

            if len(m['cast']) == 1:
                print("3rd")
                actor1 = m['cast'][0].personID

        movie_instance = movie.objects.filter(id=movie_id)
        mi = None
        for i in movie_instance:
            print(i)
            mi = i

        temp = actor(movieId=mi, actor1=actor1, actor2=actor2, actor3=actor3)
        temp.save()
        # act.update()

        print(temp)




    def get_movies(self):
        for i in range(1, 50):
            ia = imdb.IMDb()
            m = ia.get_movie(format(i, '07'))
            self.load_actors(m, format(i, '07'))
            # print(m.keys())
            if 'title' in m.keys():
                title = m['title']
            else:
                title = ''

            if 'cover url' in m.keys():
                imageUrl = m['cover url']
            else:
                imageUrl = ''

            if 'director' in m.keys():
                director = m['director'][0]['name']
            else:
                director = ''

            if 'releaseDate' in m.keys():
                releaseDate = m['original air date']
            else:
                releaseDate = ''

            if len(m['genres']) >= 2:
                genre1 = m['genres'][0]
                genre2 = m['genres'][1]
            elif len(m['genres']) == 1:
                genre1 = m['genres'][0]
                genre2 = ''
            else:
                genre1 = ''
                genre2 = ''

            if 'plot' in m.keys():
                plot = m['plot']
            elif 'plot outline' in m.keys():
                plot = m['plot outline']
            else:
                plot = 'No plot to display'

            if 'rating' in m.keys():
                rating = m['rating']
            else:
                rating = ''

            if 'votes' in m.keys():
                votes = m['votes']
            else:
                votes = ''

            if 'runtimes' in m.keys():
                runtime = m['runtimes']
            else:
                runtime = ''

            if 'year' in m.keys():
                year = m['year']
            else:
                year = 1600

            self.movies.append({'id': format(i, '07'),
                           'title': title,
                           'imageUrl': imageUrl,
                           'director': director,
                           'releaseDate': releaseDate,
                           'genre1': genre1,
                           'genre2': genre2,
                           'plot': plot,
                           'rating': rating,
                           'votes': votes,
                           'runtime': runtime,
                           'year': year})

            # print({'id': format(i, '07'),
            #                'title': title,
            #                'imageUrl': imageUrl,
            #                'director': director,
            #                'releaseDate': releaseDate,
            #                'genre1': genre1,
            #                'genre2': genre2,
            #                'plot': plot,
            #                'rating': rating,
            #                'votes': votes,
            #                'runtime': runtime,
            #                'year': year})

        # for m in self.movies:
        #     if not movie.objects.filter(id=m['id']):
        #         temp = movie(m['id'], m['title'], m['imageUrl'], m['director'], m['releaseDate'], m['genre1'],
        #                      m['genre2'], m['plot'], m['rating'], m['votes'], m['runtime'], m['year'])
        #         temp.save()
        #         print('Saved.')













