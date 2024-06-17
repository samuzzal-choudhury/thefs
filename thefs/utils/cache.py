"""Cache manager module."""

from thefs.utils.log import logger


class CacheManager:
    """Manage the file cache."""

    def __init__(self):
        """Create an empty cache."""
        self.file_cache = {}

    def add_file_cache(self, hashval, filename):
        """Add hashval:filename entry to the cache."""
        self.file_cache[hashval] = filename
        logger.info(f'Added {hashval} to the file cache')

    def remove_file_cache(self, filename):
        """Remove hashval:filename entry from the cache."""
        for hashval, fname in self.file_cache.items():
            if fname == filename:
                del self.file_cache[hashval]
                logger.info(f'Deleted {hashval} from the file cache')
                return True
        return False

    def fetch_file_cache(self, hashval):
        """Retrieve entry from the cache based on the hashval."""
        if hashval in self.file_cache:
            return self.file_cache[hashval]
        return None

    def print_cache(self):
        """Print all the entries in the cache."""
        for hashval, fname in self.file_cache.items():
            print(f'{hashval}: {fname}')
