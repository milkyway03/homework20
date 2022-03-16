from unittest.mock import MagicMock

import pytest

from hw.dao.model.director import Director
from hw.dao.director import DirectorDAO
from hw.service.director import DirectorService


@pytest.fixture
def director_dao():
    director_dao = DirectorDAO(None)
    director1 = Director(
        id=1,
        name="Dir1",
    )
    director2 = Director(
        id=2,
        name="Dir2",
    )
    director3 = Director(
        id=3,
        name="Dir3",
    )
    dict_objects = {1: director1, 2: director2, 3: director3}
    director_dao.get_one = MagicMock(side_effect=dict_objects.get)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    director_dao.create = MagicMock(return_value=Director(id=4, name="Dir4"))
    director_dao.delete = MagicMock(side_effect=dict_objects.pop)
    director_dao.update = MagicMock()
    director_dao.partially_update = MagicMock()
    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director.id is not None

    def test_get_all(self):
        director = self.director_service.get_all()
        assert len(director) > 0

    def test_create(self):
        director_d = {
            'name': 'Dir4'
        }
        director = self.director_service.create(director_d)
        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)
        director = self.director_service.get_one(1)
        assert director is None

    def test_update(self):
        director_d = {
            'id': 2,
            'name': "Dir2",
        }
        self.director_service.update(director_d)
