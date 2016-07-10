Gets radio show's logo and title and serves them in a webserver. Also album cover, and music name too

How to run? 
Just set up 2 upstart scripts, one for each process

```
setuid user
setgid user

start on runlevel [2345]

stop on runlevel [016]
chdir /PATH/
exec python /PATH/screenshooter.py
```
and 
```
setuid user
setgid user

start on runlevel [2345]

stop on runlevel [016]
chdir /path/
exec python /path/server.py
```
