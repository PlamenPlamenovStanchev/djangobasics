from typing import Optional, List

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class BadWordsValidator:
    def __init__(self, bad_words: Optional[List]=None, message: Optional[str]=None):
        self.bad_words = bad_words
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
#        self.__message = value or 'The text contains bad words or profanity'
        if value is None:
            self.__message = 'The text contains bad words or profanity'
        else:
            self.__message = value


    def __call__(self, value):
        for bad_word in value.split():
            if bad_word.lower() in self.bad_words:
                raise ValidationError(self.message)
