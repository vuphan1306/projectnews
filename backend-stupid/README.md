# API application for pika project

# Technical stacks

## DevOps
### Docker

An open platform for distributed applications for developers and sysadmins

[Homepage](https://www.docker.com/)

### Gitlab CI

GitLab CI is a part of GitLab, a web application with an API that stores its state in a database. It manages projects/builds and provides a nice user interface, besides all the features of GitLab.

[Homepage](https://about.gitlab.com/gitlab-ci/)

### Vagrant

Vagrant provides easy to configure, reproducible, and portable work environments built on top of industry-standard technology and controlled by a single consistent workflow to help maximize the productivity and flexibility of you and your team.

[Homepage](http://www.vagrantup.com/)

### VirtualBox

VirtualBox is a general-purpose full virtualizer for x86 hardware, targeted at server, desktop and embedded use.
[Homepage](https://www.virtualbox.org)

### Backend Frameworks

### Django

Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

[Homepage](https://www.djangoproject.com/)

### Django-Extensions

Django Extensions is a collection of custom extensions for the Django Framework.

[Github](https://github.com/django-extensions/django-extensions)

### Tastypie

Tastypie is a web service API framework for Django. It provides a convenient, yet powerful and highly customizable, abstraction for creating REST-style interfaces.

[Homepage](https://django-tastypie.readthedocs.org/en/latest/)

### Celery

Celery is an asynchronous task queue/job queue based on distributed message passing.  It is focused on real-time operation, but supports scheduling as well.

[Homepage](http://www.celeryproject.org/)

## Databases

### PostgreSQL

PostgreSQL is a powerful, open source object-relational database system. It has more than 15 years of active development and a proven architecture that has earned it a strong reputation for reliability, data integrity, and correctness.

[Homepage](http://www.postgresql.org/)

## Backend Libraries

### pip

A tool for installing and managing Python packages.
[Documentation](http://www.pip-installer.org/en/latest/)

### Psycopg

Psycopg is the most popular PostgreSQL adapter for the Python programming language. At its core it fully implements the Python DB API 2.0 specifications. Several extensions allow access to many of the features offered by PostgreSQL.

[Homepage](http://initd.org/psycopg/)

## Web Servers

### nginx

Nginx (pronounced "engine-ex") is an open source reverse proxy server for HTTP, HTTPS, SMTP, POP3, and IMAP protocols, as well as a load balancer, HTTP cache, and a web server (origin server). The nginx project started with a strong focus on high concurrency, high performance and low memory usage. It is licensed under the 2-clause BSD-like license and it runs on Linux, BSD variants, Mac OS X, Solaris, AIX, HP-UX, as well as on other *nix flavors.

[Homepage](http://nginx.org/)

### Gunicorn

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model ported from Ruby's Unicorn project. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.

[Homepage](http://gunicorn.org/)


## Usage

### For devs:

	1.	clone the project, navigate to the project

	2.	run scripts to up the environment as following:
		-	sh scripts/dj-create-dev-env.sh
		-	sudo su
		-	echo 'ln -sfn /mnt/sda1/data /data' >> /var/lib/boot2docker/bootlocal.sh
		-   sh scripts/dj-dev-build.sh
		-   sh scripts/dj-dev-up-bg.sh
		-   sh scripts/dj-dev-mmgr.sh
		-   sh scripts/dj-dev-mgr.sh
		-   sh scripts/dj-dev-createsperuser.sh
	
	3. Your env is ready now, keep calm and review code base in backend folder

## Code Editor

    1. A highly recommended code editor is Sublime Text 2 with Flake8Lint package.
    
    2. If there has no any specially cases, don't break the project structure and code style. 
       It will helps us refer and review your code more easier.

    
Develop on local machine:    
Install virtualenv: 
$ pip install virtualenv
Create virtual enviroment:
$ cd my_project_folder
$ virtualenv venv
$ virtualenv -p /usr/bin/python3 venv
Active enviroment:
$ source venv/bin/activate
Install package:
$ pip install requests
$ pip install -r requirements/local.txt 
Maybe you get error : ValueError: --enable-jpeg requested but jpeg not found, aborting.
=> solve: sudo apt-get install libjpeg-dev
Create DB:
$ sudo su postgres
psql
CREATE DATABASE dbname;
Maybe you need to create new user:
CREATE USER tester WITH PASSWORD 'test_password';



========>DONE 
makemigrations, migrate, createsuperuser and runserver.