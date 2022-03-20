import http.client, json


class Actor:
    actors = [{}] * 501

    def get_actors(self):

        conn = http.client.HTTPSConnection("data-imdb1.p.rapidapi.com")

        headers = {
            'x-rapidapi-host': "data-imdb1.p.rapidapi.com",
            'x-rapidapi-key': "c722563d14mshfb13129f4a41155p1c55abjsn9b962eb4bf04"
            }

        for i in range(1, 501):
            print("/actors/" + "nm" + format(i, '07'))
            conn.request("GET", "/actors/" + "nm" + format(i, '07'), headers=headers)

            res = conn.getresponse()
            data = res.read()

            # print(data.decode("utf-8"))

            d = json.loads(data.decode('utf-8'))

            # temp = d['results']['knownForTitles'].split(',')
            # movies = [''] * 4
            # for i in range(0, len(temp)):
            movies = d['results']['knownForTitles'].split(',')
            if len(movies) < 4:
                continue

            self.actors[i] = {'id': d['results']['nconst'],
                            'name': d['results']['primaryName'],
                            'birthYear': d['results']['birthYear'],
                            'deathYear': d['results']['deathYear'],
                            'movie1': movies[0],
                            'movie2': movies[1],
                            'movie3': movies[2],
                            'movie4': movies[3]}
            print(self.actors[i])

        print(self.actors)
        return self.actors


