import pytest
from unittest.mock import MagicMock, patch, mock_open
from collections import Counter
from thefs.utils.files import FileUtils


@pytest.fixture
def file_utils():
    return FileUtils()


def test_store_file_success(file_utils):
    with patch('thefs.utils.files.secure_filename', return_value='test.txt'):
        with patch('builtins.open', mock_open()):
            file = MagicMock()
            file.save = MagicMock()
            result = file_utils.store_file('test.txt', file)
            assert result is True
            file.save.assert_called_once()


def test_store_file_failure(file_utils):
    with patch('thefs.utils.files.secure_filename', return_value='test.txt'):
        with patch('builtins.open', mock_open()) as mocked_file:
            mocked_file.side_effect = Exception('File save error')
            file = MagicMock()
            file.save = MagicMock(side_effect=Exception('File save error'))
            result = file_utils.store_file('test.txt', file)
            assert result is False
            file.save.assert_called_once()


def test_list_files(file_utils):
    with patch('os.path.exists', return_value=True):
        with patch('os.listdir', return_value=['file1.txt', 'file2.txt']):
            files = file_utils.list_files()
            assert files == ['file1.txt', 'file2.txt']


def test_list_files_empty(file_utils):
    with patch('os.path.exists', return_value=False):
        files = file_utils.list_files()
        assert files == []


def test_remove_file_success(file_utils):
    with patch('os.path.isfile', return_value=True):
        with patch('os.remove', return_value=None):
            result = file_utils.remove_file('test.txt')
            assert result is True


def test_remove_file_failure(file_utils):
    with patch('os.path.isfile', return_value=True):
        with patch('os.remove', side_effect=Exception('Remove error')):
            result = file_utils.remove_file('test.txt')
            assert result is False


def test_generate_words_frequency(file_utils):
    with patch('thefs.utils.files.FileUtils.list_files', return_value=['file1.txt']):
        with patch('builtins.open', mock_open(read_data='word1 word2 word2')):
            result = file_utils.generate_words_frequency(limit=2, order='dsc')
            assert result == ['word2', 'word1']


def test_count_total_words(file_utils):
    with patch('thefs.utils.files.FileUtils.list_files', return_value=['file1.txt']):
        with patch('builtins.open', mock_open(read_data='word1 word2 word2')):
            result = file_utils.count_total_words()
            assert result == 3
