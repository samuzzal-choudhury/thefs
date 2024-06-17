from thefs.utils.log import logger


class CacheManager:
    def __init__(self):
        self.file_cache = {}

    def add_file_cache(self, hashval, filename):
        self.file_cache[hashval] = filename
        logger.info(f'Added {hashval} to the file cache')

    def remove_file_cache(self, filename):
        for hashval, fname in self.file_cache.items():
            if fname == filename:
                del self.file_cache[hashval]
                logger.info(f'Deleted {hashval} from the file cache')
                return True
        return False

    def fetch_file_cache(self, hashval):
        if hashval in self.file_cache:
            return self.file_cache[hashval]
        return None

    def print_cache(self):
        for hashval, fname in self.file_cache.items():
            print(f'{hashval}: {fname}')