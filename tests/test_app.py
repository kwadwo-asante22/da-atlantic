"""Test for app.py."""

import sqlite3 as sql

import mock
import pytest

from src.app import (
    allowed_file,
    connect_to_db,
    get_column_names_from_db_table
)
from src.constant import ALLOWED_EXTENSIONS


def test_allowed_file():
    """Test to assert file type."""
    assert allowed_file('/sample_data/atlantic_file.csv')


test_query = """select * from test where rownum <= 5"""


class MockCursor():
    """Mock the cursor interface."""

    def __init__(self, *args, **kwargs):
        """Create defaults."""
        self.description = [('Header0'), ('Header1')]
        self.count = 0

    def __iter__(self):
        """Support Iteration."""
        return self

    def execute(self, query):
        """Implement required method."""
        pass

    def close(self):
        """Implement close method."""

    def next(self):
        """Support Iteration."""
        if self.count == 2:
            raise StopIteration
        else:
            self.count += 1
            return ['A', 'B']


@mock.patch('src.app.sql')
def test_connect_to_db(mock_sql):
    """Test an empty connection response."""
    mock_connection = mock_sql.connect.return_value
    
    response = connect_to_db('table')

    assert response is None
