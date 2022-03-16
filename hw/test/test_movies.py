from unittest.mock import MagicMock

import pytest

from hw.dao.model.movie import Movie
from hw.dao.movie import MovieDAO
from hw.service.movie import MovieService


@pytest.fixture
def movie_dao():
    movie_dao = MovieDAO(None)
    movie1 = Movie(
        id=1,
        title="Movie1",
        description="description 1",
        trailer="trailer1",
        year=2001,
        rating=1,
        genre_id=1,
        director_id=1
    )
    movie2 = Movie(
        id=2,
        title="Movie2",
        description="description 2",
        trailer="trailer2",
        year=2002,
        rating=2,
        genre_id=2,
        director_id=2
    )
    movie3 = Movie(
        id=3,
        title="Movie3",
        description="description 3",
        trailer="trailer3",
        year=2003,
        rating=3,
        genre_id=3,
        director_id=3
    )
    dict_objects = {1: movie1, 2: movie2, 3: movie3}
    movie_dao.get_one = MagicMock(side_effect=dict_objects.get)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=4, title="Movie 4"))
    movie_dao.delete = MagicMock(side_effect=dict_objects.pop)
    movie_dao.update = MagicMock()
    movie_dao.partially_update = MagicMock()
    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie.id is not None

    def test_get_all(self):
        movie = self.movie_service.get_all()
        assert len(movie) > 0

    def test_create(self):
        movie_d = {
            'title': 'Movie4'
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)
        movie = self.movie_service.delete(1)
        assert movie is None

    def test_update(self):
        movie_d = {
            'id': 2,
            'title': "Movie2",
            'description': "description 2",
            'trailer': "trailer2",
            'year': 2002,
            'rating': 2,
            'genre_id': 2,
            'director_id': 2
        }
        self.movie_service.update(movie_d)


