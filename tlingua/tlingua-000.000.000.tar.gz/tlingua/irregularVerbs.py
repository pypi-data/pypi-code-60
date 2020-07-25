from .global_vars import *

from .token_types import Verb_Token


class IrregularVerb:
    root = ""
    third_person = ""
    present = ""
    past_simple = ""
    past_simple_plural = ""
    past_participle = ""
    past_participle_third_person = ""

    def __init__(self, lingua):
        temp_token = Verb_Token("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")

        self.root = self.__class__.root
        self.third_person = self.__class__.third_person
        self.present = self.__class__.present
        self.past_simple = self.__class__.past_simple
        self.past_simple_plural = self.__class__.past_simple_plural
        self.past_participle = self.__class__.past_participle
        self.past_participle_third_person = self.__class__.past_participle_third_person

        if self.third_person == "":
            self.third_person = temp_token.verb_form(self.root, lingua, VERB_THIRD_PERSON, check_irregulars=False)
        if self.present == "":
            self.present = temp_token.verb_form(self.root, lingua, VERB_PRESENT, check_irregulars=False)
        if self.past_simple == "":
            self.past_simple = temp_token.verb_form(self.root, lingua, VERB_PAST_SIMPLE, check_irregulars=False)
        if self.past_simple_plural == "":
            self.past_simple_plural = self.past_simple
        if self.past_participle == "":
            self.past_participle = temp_token.verb_form(self.root, lingua, VERB_PAST_PARTICIPLE, check_irregulars=False)
        if self.past_participle_third_person == "":
            self.past_participle_third_person = temp_token.verb_form(self.root, lingua, VERB_PAST_PARTICIPLE, PERSON_THIRD, check_irregulars=False)

    def form(self, form, person=PERSON_FIRST):
        if form == VERB_ROOT:
            return self.root
        if form == VERB_THIRD_PERSON:
            return self.third_person
        if form == VERB_PRESENT:
            return self.present
        if form == VERB_PAST_SIMPLE:
            if person == PERSON_PLURAL:
                return self.past_simple_plural
            return self.past_simple
        if form == VERB_PAST_PARTICIPLE:
            if person == PERSON_THIRD:
                return self.past_participle_third_person
            return self.past_participle


class AriseVerb(IrregularVerb):
    root = "arise"
    past_simple = "arose"
    past_participle = "arisen"

class AwakeVerb(IrregularVerb):
    root = "awake"
    past_simple = "awoke"
    past_participle = "awoken"

class BackslideVerb(IrregularVerb):
    root = "backslide"
    past_simple = "backslid"
    past_participle = "backslid"

class BeVerb(IrregularVerb):
    root = "be"
    third_person = "is"
    present = "being"
    past_simple = "was"
    past_simple_plural = "were"
    past_participle = "been"

class BearVerb(IrregularVerb):
    root = "bear"
    past_simple = "bore"
    past_participle = "borne"
