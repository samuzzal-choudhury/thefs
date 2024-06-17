"""Module to perform various file storage operations."""

import os
from werkzeug.utils import secure_filename
from thefs.utils.log import logger
from collections import Counter


class FileUtils:
    """Module to perform various file storage operations."""

    def __init__(self):
        """Initiate the storage directory."""
        self.dir = os.getenv('FILE_STORAGE_DIR', '/tmp/storage')

    def store_file(self, filename, file):
        """Add a file in the storage."""
        if file:
            fname = secure_filename(filename)
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            filepath = os.path.join(self.dir, fname)
            try:
                file.save(filepath)
                logger.info(f'File {filepath} stored successfully '
                            f'in {filepath}.')
            except OSError as e:
                logger.error(f'File {filepath} could not '
                             f'be saved. Error {e}')
                return False
            return True
        return False

    def list_files(self):
        """List all files from the storage."""
        filenames = []
        if os.path.exists(self.dir):
            filenames = os.listdir(self.dir)
        logger.info(f'Retrieved files {filenames}')
        return filenames

    def remove_file(self, fname):
        """Remove a file in the storage."""
        filepath = os.path.join(self.dir, fname)
        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
            except OSError as e:
                logger.error(f'File {filepath} could not be '
                             f'removed. Error {e}')
                return False
            return True
        return False

    def __generate_file_word_count(self, filename):
        """Private method to generate word count of a file."""
        try:
            with open(filename, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            logger.warning(f'File {filename} not found')
            return Counter()
        wc = Counter(content.strip().split())
        return wc

    def __get_most_common_n(self, word_counter, limit):
        """Get the first n most common words in the storage."""
        most_common_words = word_counter.most_common(int(limit))
        logger.debug(f'Most common {limit} words are {most_common_words}')
        return [word for word, _ in most_common_words]

    def __get_least_common_n(self, word_counter, limit):
        """Get the first n least common words in the storage."""
        least_first_word_counts = (
            sorted(word_counter.items(), key=lambda x: x[1]))
        least_common_words = \
            [key for key, count in least_first_word_counts[1:] if count > 0]
        logger.debug(f'Least common {limit} words are {least_common_words}')
        return least_common_words[:int(limit)]

    def generate_words_frequency(self, limit=-1, order='dsc'):
        """Initiate the word frequency for first n most/least common words."""
        # Populate all words with their respective frequencies
        files = self.list_files()
        word_counter = Counter()
        for file in files:
            filepath = os.path.join(self.dir, file)
            file_wc = self.__generate_file_word_count(filepath)
            word_counter.update(file_wc)

        # Generate the list of n frequent words based on the limit
        if limit == -1:
            # limit -1 indicates all words without any limit
            limit = len(word_counter)
        logger.debug(f'Generated word counter {word_counter}')

        if order == 'dsc':
            return self.__get_most_common_n(word_counter, limit)
        elif order == 'asc':
            return self.__get_least_common_n(word_counter, limit)
        return []

    def count_total_words(self):
        """Generate the total word count in the storage."""
        files = self.list_files()
        word_counter = Counter()
        for file in files:
            filepath = os.path.join(self.dir, file)
            file_wc = self.__generate_file_word_count(filepath)
            word_counter.update(file_wc)
        logger.debug(f'Total word count is {word_counter.total()}')
        return word_counter.total()
