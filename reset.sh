dropdb -p 5433 worderator
createdb -p 5433 -O worderate worderator
./manage.py syncdb --noinput
