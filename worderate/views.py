import random

from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django import forms

from utils import render
from forms import LoginForm
from worderate.models import Stem
from worderate.models import Word
from worderate.models import WordDB
from settings import FALLBACK_DB
from settings import SPLITSIZE
from settings import PREFER_MAXSIZE
from settings import HARD_MAXSIZE
from settings import FALLBACK_DB

from profiler import profile

def _get_next_stem(word, whichdb=None):
    if whichdb:
        try:
            wordob = Word.objects.get(word=word[-SPLITSIZE:],
                                      worddb__name=whichdb)
        except Word.DoesNotExist:
            return _get_next_stem(word)
        next_stem = Stem.objects.filter(
            word=wordob)
        if len(word) > PREFER_MAXSIZE:
            next_stem_with_end = next_stem.filter(tails__in="")
            if next_stem_with_end.count():
                next_stem = next_stem_with_end
    else:
        wordob = Word.objects.filter(
            word=word[-SPLITSIZE:]).order_by('?')[0]
        next_stem = Stem.objects.filter(
            word=wordob)
    result = next_stem.order_by('?')[0]
    print result
    return result

def _worderate(dbmix=None):
    if not dbmix:
        dbmix = {'src/british':1}
    dblist = ['src/british']
    for k, v in dbmix.items():
        dblist.extend([k]*v)
    whichdb = random.choice(dblist)
    start_stem = Stem.objects.filter(word__worddb__name=whichdb,
                                     is_root=True).order_by('?')[0]
    next_tail = start_stem.pick_next_tail()
    word = start_stem.word.word + next_tail.word.word
    while True:
        if len(word) > HARD_MAXSIZE:
            return _worderate(dbmix)
        whichdb = random.choice(dblist)
        next_stem = _get_next_stem(word, whichdb)
        if not next_stem or not next_stem.tails.all():
            next_stem = _get_next_stem(word)
        if len(word) > 5:
            next_tail = next_stem.pick_next_tail(prefer_end=True)
        else:
            next_tail = next_stem.pick_next_tail()
        if not next_tail.word.word.strip():
            break
        word += next_tail.word.word
    return word

@render('home.html')
def home(request):
    databases = WordDB.objects.all()
    dbmix = {}
    if request.GET.has_key("worderate"):
        for database in databases:
            val = request.GET.get("db__%s" % database.name, '')
            if val:
                dbmix[database.name] = int(val)
                database.mix = val
        word = _worderate(dbmix=dbmix)
    else:
        for database in databases:
            if database.name == FALLBACK_DB:
                database.mix = 1
            else:
                database.mix = 0
    return locals()
        

@render('login_form.html')
def login_form(request):
    if request.method == "POST":
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = LoginForm()
    return locals()

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
