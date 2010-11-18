from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models import permalink

class CustomUser(User):
    objects = UserManager()

    @property
    def display_name(self):
        if self.first_name:
            name = self.first_name
        else:
            name = self.email
        return name
    
    def __unicode__(self):
        return self.email
    
    @permalink
    def get_absolute_url(self):
        return ("user", (self.id,))


class Word(models.Model):
    word = models.CharField(max_length=4)
    
    def __unicode__(self):
        return self.word.strip() or "END"


class WordDB(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=120)

class Stem(models.Model):
    worddb = models.ForeignKey(WordDB)
    word = models.ForeignKey(Word,
                             related_name='stems')
    is_root = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s" % (self.word,
                           [x for x in self.tails.all()])

    def pick_next_tail(self, dbname=None, prefer_end=False):
        tails = self.tails.all()
        if prefer_end:
            tails = tails.filter(word__word="")
            if not tails.count():
                return self.pick_next_tail(dbname=dbname)
        if dbname:
            specific_tails = tails.filter(worddb__name=dbname)
            if specific_tails.count():
                tails = specific_tails
        if not tails.count():
            return self.pick_next_tail()
        return tails.order_by('?')[0]


class Tail(models.Model):
    worddb = models.ForeignKey(WordDB)
    word = models.ForeignKey(Word)
    stem = models.ForeignKey(Stem,
                             related_name='tails',
                             blank=True,
                             null=True)

    def __unicode__(self):
        return "%s from db %s" % (self.word, self.worddb.name)
