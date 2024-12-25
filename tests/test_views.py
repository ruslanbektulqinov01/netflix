from django.test import TestCase, Client

from netflix_app.models import Movie


class TestMovieListView(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie", year="2019", imdb=8.0, genre="Fantastic"
        )
        self.client = Client()

    def test_movie_list(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, 200)


class TestMovieSearchView(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie", year=2019, imdb=8.0, genre="Fantastic"
        )
        self.client = Client()

    def test_movie_search(self):
        response = self.client.get("/api/movies/?title=Test")
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.movie.title)
        assert data[0]["year"] == self.movie.year
        assert data[0]["id"] is not None
        self.assertIsNotNone(data[0]["imdb"])


class TestMovieSortImdbView(TestCase):
    def setUp(self):
        self.movie1 = Movie.objects.create(
            title="Test Movie", year=2019, imdb=4.0, genre="Fantastic"
        )
        self.movie2 = Movie.objects.create(
            title="Test Movie 2", year=2020, imdb=6.0, genre="Drama"
        )
        self.movie3 = Movie.objects.create(
            title="Test Movie 3", year=2020, imdb=2.0, genre="Drama"
        )
        self.client = Client()

    def test_movie_sort_imdb(self):
        response = self.client.get("/api/movies/?ordering=imdb")
        data = response.data
        self.assertEqual(data[0]["imdb"], self.movie3.imdb)
        self.assertEqual(data[1]["imdb"], self.movie1.imdb)
        self.assertEqual(data[2]["imdb"], self.movie2.imdb)
        self.assertEqual(response.status_code, 200)
