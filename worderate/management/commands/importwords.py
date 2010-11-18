import sys
import codecs
import locale
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction
from django.db.utils import DatabaseError
from django.utils.encoding import smart_unicode
from django.utils.encoding import DjangoUnicodeDecodeError

from worderate.models import Word
from worderate.models import Stem
from worderate.models import Tail
from worderate.models import WordDB

import settings

from profiler import profile

class Command(BaseCommand):
    option_list =  BaseCommand.option_list + (
        make_option('--dry-run', '-n', dest='dry_run',
                    action="store_true",
                    help="Only show what would be done"),
        make_option('--quiet', '-q', dest='quiet',
                    action="store_true",
                    help="Be quiet about it"),
        make_option('--wordlist', '-w', dest='wordlist',
                    action="store",
                    help="Wordlist file, one word per line"),
        )
    help = "Import a word file into the worderator"

    def handle(self, *args, **options):
        # make sure our print statements can handle unicode
        sys.stdout = codecs.getwriter(
            locale.getpreferredencoding())(sys.stdout)
        wordlist = options.get('wordlist', None)

        dry_run = options.get('dry_run', False)
        quiet = options.get('quiet', False)
        infile = open(wordlist, "r")
        worddb, _ = WordDB.objects.get_or_create(name=wordlist)
        splitsize = settings.SPLITSIZE
        count = 0
        for line in infile.readlines():
            try:
                line = smart_unicode(line).lower().strip()
            except DjangoUnicodeDecodeError:
                continue
            if len(line) < splitsize + 1:
                continue
            is_root = True
            for x in range(0, len(line)-splitsize+1):
                try:
                    stemword, _ = Word.objects.get_or_create(
                        word=line[x:x+splitsize])
                    stem, _ = Stem.objects.get_or_create(
                        worddb=worddb,
                        word=stemword,
                        is_root=is_root)
                    tailword, _ = Word.objects.get_or_create(
                        word=line[x+splitsize:x+splitsize+1])
                    tail, _ = Tail.objects.get_or_create(
                        worddb=worddb,
                        word=tailword,
                        stem=stem)
                    is_root = False
                except StandardError:
                    print "!"
                    break
                count +=1
        if not dry_run:
            pass
            #transaction.commit()
        else:
            pass
            #transaction.abort()
        if not quiet:
            print "imported %d words" % count
                
# 15 lloyd square, king x angel
