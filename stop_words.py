import os

class StopWords:
    def __init__(self, file_name='stop_hinglish.txt'):
        self.file_name = file_name
        self.stop_words = self.load_stop_words()

    def load_stop_words(self):
        """Load stop words from a file."""
        stop_words_file = os.path.join(os.path.dirname(__file__), self.file_name)
        try:
            with open(stop_words_file, 'r') as f:
                return f.read().splitlines()  # Return a list of stop words
        except FileNotFoundError:
            print(f"Error: {stop_words_file} not found.")
            return []

    def get_stop_words(self):
        """Return the loaded stop words."""
        return self.stop_words
