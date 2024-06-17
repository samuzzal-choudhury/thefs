import os
import hashlib
from werkzeug.utils import secure_filename
from thefs.utils.log import logger
from thefs.utils.cache import CacheManager
from collections import Counter


class FileUtils:
    def __init__(self):
        self.dir = os.getenv('FILE_STORAGE_DIR', '/tmp/storage')

    def store_file(self, filename, file):
        if file:
            fname = secure_filename(filename)
            if not os.path.exists(self.dir):
                os.makedirs(self.dir)
            filepath = os.path.join(self.dir, fname)
            try:
                file.save(filepath)
            except Exception as e:
                logger.warning(f'File {filepath} could not be saved.')
                return False
            return True
        return False

    def list_files(self):
        filenames = []
        if os.path.exists(self.dir):
            filenames = os.listdir(self.dir)
        return filenames

    def remove_file(self, fname):
        filepath = os.path.join(self.dir, fname)
        if os.path.isfile(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.warning(f'File {filepath} could not be removed')
                return False
            return True
        return False

    def __generate_file_word_count(self, filename):
        try:
            with open(filename, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"File {filename} not found")
            return Counter()
        wc = Counter(content.strip().split())
        return wc

    def __get_most_common_n(self, word_counter, limit):
        most_common_words = word_counter.most_common(int(limit))
        return [word for word, _ in most_common_words]

    def __get_least_common_n(self, word_counter, limit):
        least_first_agg_counts = sorted(word_counter.items(), key=lambda x: x[1])
        least_common_words = [key for key, count in least_first_agg_counts[1:] if count > 0]
        return least_common_words[:int(limit)]

    def generate_words_frequency(self, limit=-1, order='dsc'):
        # Populate all words with their respective frequencies
        files = self.list_files()
        word_counter = Counter()
        for file in files:
            filepath = os.path.join(self.dir, file)
            file_wc = self.__generate_file_word_count(filepath)
            word_counter.update(file_wc)

        print(word_counter)
        # Generate the list of n frequent words based on the limit
        if limit == -1:
            # limit -1 indicates all words without any limit
            limit = len(word_counter)

        print(limit, order)
        if order == 'dsc':
            return self.__get_most_common_n(word_counter, limit)
        elif order == 'asc':
            return self.__get_least_common_n(word_counter, limit)
        return []

    def count_total_words(self):
        files = self.list_files()
        word_counter = Counter()
        for file in files:
            filepath = os.path.join(self.dir, file)
            file_wc = self.__generate_file_word_count(filepath)
            word_counter.update(file_wc)
        return word_counter.total()
