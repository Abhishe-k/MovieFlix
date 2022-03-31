from .models import movie, actor, topmovie
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
            print(m['cast'])

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


    def get_movies(self, top):
        temp = None
        ia = imdb.IMDb()

        rnge = 100
        if top:
            temp = ia.get_top250_movies()
            rnge = 250

        print(rnge)
        for i in range(1, rnge + 1):
            if top:
                m = ia.get_movie(temp[i - 1].movieID)
                print(i, temp[i - 1].movieID)
                # self.load_actors(m, temp[0].movieID)
            else:
                m = ia.get_movie(format(i, '07'))
                # self.load_actors(m, format(i, '07'))

            # print(m.keys())
            if 'title' in m.keys():
                title = m['title']
            else:
                title = ''

            if 'full-size cover url' in m.keys():
                imageUrl = m['full-size cover url']
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

            if 'cast' in m.keys():
                cast = m['cast']
            else:
                cast = ''

            if top:
                id = temp[i - 1].movieID
            else:
                id = format(i, '07')

            self.movies.append({'id': id,
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
                           'year': year,
                            'cast': cast})

            print(self.movies[i - 1])
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

        rank = 1
        for m in self.movies:

            if top:
                mv = list(movie.objects.filter(id=m['id']))
                print(mv[0])

                temp = topmovie(topId=mv[0], rank=rank)
                temp.save()
                rank += 1



            if not movie.objects.filter(id=m['id']):
                print('Adding to database', m['id'])

                temp = movie(m['id'], m['title'], m['imageUrl'], m['director'], m['releaseDate'], m['genre1'],
                             m['genre2'], m['plot'], m['rating'], m['votes'], m['runtime'], m['year'])
                temp.save()

                print('Saved.')


            # self.load_actors(m, m['id'])

        if top:
            return self.movies

    def update_image(self):

        mvs = list(movie.objects.all())
        ia = imdb.IMDb()

        for m in mvs:
            temp_movie = ia.get_movie(str(m.id))

            if 'full-size cover url' in temp_movie.keys():
                m.imageUrl = temp_movie['full-size cover url']
            else:
                m.imageUrl = ''

            m.save()
