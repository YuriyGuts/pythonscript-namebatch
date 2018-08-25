class NameGenerator(object):
    """
    Generates Benedict Cumberbatch names.
    """

    DIVERSITY_LOW = 0
    DIVERSITY_HIGH = 1

    def __init__(self, morphology_service, diversity_level=DIVERSITY_LOW):
        """
        Create a new name generator.

        Parameters
        ----------
        morphology_service : MorphologyService
        diversity_level : DiversityLevel
        """
        self.morphology_service = morphology_service
        self.diversity_level = diversity_level

    def is_suitable_first_name(self, word):
        """
        Determine whether the specified word is a suitable Benedict.

        Parameters
        ----------
        word : str
            Word to test.

        Returns
        -------
        bool
            True if the word is suitable, False otherwise.
        """
        is_suitable = not (word.endswith("'") or word.endswith("'s"))
        is_suitable &= word not in {'benedict', 'cumberbatch'}

        is_suitable &= len(self.morphology_service.syllabify(word)) == 3
        is_suitable &= self.morphology_service.stressed_syllable_index(word) == 0

        if self.diversity_level < self.DIVERSITY_HIGH:
            is_suitable &= word.startswith('b')

        return is_suitable

    def is_suitable_last_name(self, word):
        """
        Determine whether the specified word is a suitable Cumberbatch.

        Parameters
        ----------
        word : str
            Word to test.

        Returns
        -------
        bool
            True if the word is suitable, False otherwise.
        """
        is_suitable = not (word.endswith("'") or word.endswith("'s"))
        is_suitable &= word not in {'benedict', 'cumberbatch'}

        is_suitable &= len(self.morphology_service.syllabify(word)) == 3

        if self.diversity_level < self.DIVERSITY_HIGH:
            is_suitable &= self.morphology_service.stressed_syllable_index(word) == 0
            is_suitable &= 'AE' in self.morphology_service.last_vowel_sound(word)
            is_suitable &= word.startswith('c')
        else:
            is_suitable &= self.morphology_service.stressed_syllable_index(word) == 2

        return is_suitable

    def random_name(self):
        """
        Generate a random Benedict Cumberbatch name.

        Returns
        -------
        str
            Generated name, ready to summon.
        """
        first_name = next(
            word
            for word in self.morphology_service.sample_words()
            if self.is_suitable_first_name(word)
        )
        last_name = next(
            word
            for word in self.morphology_service.sample_words()
            if self.is_suitable_last_name(word)
        )
        return '{} {}'.format(first_name.capitalize(), last_name.capitalize())
