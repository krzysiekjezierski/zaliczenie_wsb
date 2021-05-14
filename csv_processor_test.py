from unittest.mock import patch, mock_open

import pytest

from csv_processor import CSVProcessor


@pytest.fixture
def simple_int_csv():
    return "col1,col2,col3\n1,8,3\n4,5,6\n0,5,7\n"


@pytest.fixture
def multiple_types_csv():
    return "col1,col2,col3\n0,'str3',13.1\n1,'str2',6.2\n2,'str1',7.9\n"


def test_sort_without_key(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])
    processor.sort()

    assert processor.csv == [[0, 5, 7], [1, 8, 3], [4, 5, 6]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_sort_with_key(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])
    processor.sort(key=1)

    assert processor.csv == [[4, 5, 6], [0, 5, 7], [1, 8, 3]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_top(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])

    assert processor.top(2) == [[1, 8, 3], [4, 5, 6]]


def test_tail(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])

    assert processor.tail(2) == [[4, 5, 6], [0, 5, 7]]


def test_get_column(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])

    assert processor.get_column(2) == [3, 6, 7]


def test_get_columns(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])

    assert processor.get_columns((0, 1)) == [[1, 8], [4, 5], [0, 5]]


def test_drop_column(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])
    processor.drop_column(2)

    assert processor.csv == [[1, 8], [4, 5], [0, 5]]
    assert processor.header == ['col1', 'col2']


def test_drop_columns(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])
    processor.drop_columns((0, 2))

    assert processor.csv == [[8], [5], [5]]
    assert processor.header == ['col2']


def test_get_rows_by_column_value(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])

    assert processor.get_rows_by_column_value(1, 5) == [[4, 5, 6], [0, 5, 7]]


def test_casting_to_str_and_back(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])

    s = str(processor)
    print(s)
    csv_processor = CSVProcessor(s, types=(int, int, int))
    print(csv_processor)
    assert csv_processor == processor


def test_indexing(simple_int_csv):
    processor = CSVProcessor(simple_int_csv, types=[int, int, int])

    assert processor[0::2] == [[1, 8, 3], [0, 5, 7]]


@patch("builtins.open", new_callable=mock_open, read_data="col1,col2,col3\n1,8,3\n4,5,6\n0,5,7\n")
def test_from_file(mock_file, simple_int_csv):
    path = 'path/to/file'
    processor_from_file = CSVProcessor.from_file(path)

    assert processor_from_file == CSVProcessor(simple_int_csv)
    # mock_file.assert_called_once_with(path)


def test_sort_without_key_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])
    processor.sort()

    assert processor.csv == [[0, "'str3'", 13.1], [1, "'str2'", 6.2], [2, "'str1'", 7.9]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_sort_with_key_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])
    processor.sort(key=1)

    assert processor.csv == [[2, "'str1'", 7.9], [1, "'str2'", 6.2], [0, "'str3'", 13.1]]
    assert processor.header == ['col1', 'col2', 'col3']


def test_top_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])

    assert processor.top(2) == [[0, "'str3'", 13.1], [1, "'str2'", 6.2]]


def test_tail_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])

    assert processor.tail(2) == [[1, "'str2'", 6.2], [2, "'str1'", 7.9]]


def test_get_column_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])

    assert processor.get_column(2) == [13.1, 6.2, 7.9]


def test_get_columns_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])

    assert processor.get_columns((0, 1)) == [[0, "'str3'"], [1, "'str2'"], [2, "'str1'"]]


def test_drop_column_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])
    processor.drop_column(2)

    assert processor.csv == [[0, "'str3'"], [1, "'str2'"], [2, "'str1'"]]
    assert processor.header == ['col1', 'col2']


def test_drop_columns_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])
    processor.drop_columns((0, 2))

    assert processor.csv == [["'str3'"], ["'str2'"], ["'str1'"]]
    assert processor.header == ['col2']


def test_get_rows_by_column_value_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])

    assert processor.get_rows_by_column_value(0, 0) == [[0, "'str3'", 13.1]]


def test_casting_to_str_and_back_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])

    s = str(processor)
    csv_processor = CSVProcessor(s, types=(int, str, float))
    assert csv_processor == processor


def test_indexing_multi(multiple_types_csv):
    processor = CSVProcessor(multiple_types_csv, types=[int, str, float])

    assert processor[0::2] == [[0, "'str3'", 13.1], [2, "'str1'", 7.9]]


@patch("builtins.open", new_callable=mock_open, read_data="col1,col2,col3\n0,'str3',13.1\n1,'str2',6.2\n2,'str1',7.9\n")
def test_from_file_multi(mock_file, multiple_types_csv):
    path = 'path/to/file'
    processor_from_file = CSVProcessor.from_file(path)

    assert processor_from_file == CSVProcessor(multiple_types_csv)
    # mock_file.assert_called_once_with(path)
