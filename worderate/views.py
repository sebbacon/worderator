import random

from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django import forms

from utils import render
from forms import LoginForm
from worderate.models import Stem
from worderate.models import Word
from worderate.models import WordDB

from profiler import profile

def _worderate(dbmix=None):
    if not dbmix:
        dbmix = {'src/british':1}
    dblist = []
    for k, v in dbmix.items():
        dblist.extend([k]*v)
    whichdb = random.choice(dblist)
    start_stem = Stem.objects.filter(word__worddb__name=whichdb,
                                     is_root=True).order_by('?')[0]
    next_tail = start_stem.pick_next_tail(dbname=whichdb)
    word = start_stem.word.word + next_tail.word.word
    while True:
        next_stem = Stem.objects.filter(
            word=Word.objects.get(
                word=word[-3:]),
                word__worddb__name=whichdb).order_by('?')[0]
        if not next_stem.tails.all():
            # should never happen
            return _worderate(dbmix=dbmix)
        if len(word) > 6:
            next_tail = next_stem.pick_next_tail(dbname=whichdb,
                                                 prefer_end=True)
        else:
            next_tail = next_stem.pick_next_tail(dbname=whichdb)            
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
