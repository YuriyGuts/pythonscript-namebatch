import abc
import random

import nltk


class MorphologyService(object):
    @abc.abstractmethod
    def bootstrap(self):
        """
        Initialize the necessary internal resources before serving requests.
        """
        pass

    @abc.abstractmethod
    def sample_words(self):
        """
        Sample random words from the dictionary as an infinite generator.

        Yields
        ------
        str
            Random word from the dictionary
        """
        pass

    @abc.abstractmethod
    def syllabify(self, word):
        """
        Break the word into syllables.

        Parameters
        ----------
        word : str
            The word to syllabify.

        Returns
        -------
        list(list(str))
            A list of syllables, each item is a nested list containing the phonemes in the syllable.
        """
        pass

    @abc.abstractmethod
    def last_vowel_sound(self, word):
        """
        Extract the last vowel sound of the word.

        Parameters
        ----------
        word : str
            The word to check

        Returns
        -------
        str
            Last vowel sound (in the dictionary notation).
        """
        pass

    @abc.abstractmethod
    def stressed_syllable_index(self, word):
        """
        Get the index of the stressed syllable in the word.

        Parameters
        ----------
        word : str
            The word to check

        Returns
        -------
        int
            Index of the stressed syllable (can be used together with the `syllabify` method).
        """
        pass


class CMUDictMorphologyService(MorphologyService):
    """
    Morphology service backed by CMU Pronunciation Dictionary data
    (http://www.speech.cs.cmu.edu/cgi-bin/cmudict).
    """
    def __init__(self):
        self.transcriptions = {}
        self.syllables = {}
        self.words = []

    def bootstrap(self):
        """
        Initialize the necessary internal resources before serving requests.
        """
        nltk.download('cmudict', quiet=True)
        self.transcriptions = {
            word.lower(): transcription[0]
            for word, transcription in nltk.corpus.cmudict.dict().items()
        }
        self.syllables = {
            word: self._syllabify(word)
            for word in self.transcriptions.keys()
        }
        self.words = sorted(self.transcriptions.keys())

    def sample_words(self):
        """
        Sample random words from the dictionary as an infinite generator.

        Yields
        ------
        str
            Random word from the dictionary
        """
        while True:
            yield random.choice(self.words)

    def _syllabify(self, word):
        vowel_sounds = {'A', 'O', 'E', 'I', 'U'}
        result = []
        current_syllable = []

        # For simplicity, assume each vowel sound breaks the syllable.
        for phoneme in self.transcriptions[word]:
            current_syllable.append(phoneme)
            if set(phoneme) & vowel_sounds:
                result.append(current_syllable)
                current_syllable = []

        # Append any remaining consonants.
        if current_syllable and result:
            result[-1].extend(current_syllable)

        return result

    def syllabify(self, word):
        """
        Break the word into syllables.

        Parameters
        ----------
        word : str
            The word to syllabify.

        Returns
        -------
        list(list(str))
            A list of syllables, each item is a nested list containing the phonemes in the syllable.
        """
        return self.syllables[word]

    def last_vowel_sound(self, word):
        """
        Extract the last vowel sound of the word.

        Parameters
        ----------
        word : str
            The word to check

        Returns
        -------
        str
            Last vowel sound (in the dictionary notation).
        """
        phoneme = next((ph for ph in reversed(self.transcriptions[word]) if ph[-1].isdigit()), '')
        return ''.join(c for c in phoneme if not c.isdigit())

    def stressed_syllable_index(self, word):
        """
        Get the index of the stressed syllable in the word.

        Parameters
        ----------
        word : str
            The word to check

        Returns
        -------
        int
            Index of the stressed syllable (can be used together with the `syllabify` method).
        """
        for i, syllable in enumerate(self.syllables[word]):
            # Primary stress is marked with a 1, e.g. 'AE1'.
            if any(phoneme for phoneme in syllable if phoneme[-1] == '1'):
                return i
        return None
