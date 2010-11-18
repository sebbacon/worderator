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


class WordDB(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=120)

    def __unicode__(self):
        return "%s: %s" % (self.name, self.description)

class Word(models.Model):
    worddb = models.ForeignKey(WordDB)
    word = models.CharField(max_length=4)
    
    def __unicode__(self):
        return "%s (%s)" % (self.word.strip() or "END",
                            self.worddb.description or self.worddb.name)


class Stem(models.Model):
    word = models.ForeignKey(Word,
                             related_name='stems')
    is_root = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s: %s" % (self.word, self.tails_str())

    def tails_str(self):
        return ", ".join([x.word.word for x in self.tails.all()])

    def pick_next_tail(self, prefer_end=False):
        tails = self.tails.all()
        if prefer_end:
            tails = tails.filter(word__word="")
            if not tails.count():
                return self.pick_next_tail()
        return tails.order_by('?')[0]


class Tail(models.Model):
    word = models.ForeignKey(Word)
    stem = models.ForeignKey(Stem,
                             related_name='tails',
                             blank=True,
                             null=True)

    def __unicode__(self):
        return unicode(self.word)
