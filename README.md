## Ride sharer: A Uber-like app
This GitHub repository contains a course project that is a web application built using the Django framework. The purpose of the web application is to allow users to request, join, and drive for rides. The application includes a user authentication system and a user-friendly interface for managing ride requests and joining ride groups. The repository includes the source code for the web application, along with any necessary configuration files and build scripts. The use of Django allows for rapid development of the application, with features such as the ORM, built-in admin interface, and URL routing.

### start

First, you need to enter

```chmod o+x docker-deploy/web-app/initserver.sh```

```chmod o+x docker-deploy/web-app/runserver.sh```

```chmod o+x docker-deploy/web-app/startserver.sh``` in your shell

then enter
```cd docker-delpoy```
```sudo docker-compose up```

### Hierarchy

```docker-deploy
│
├── docker-compose.yml
│
├── web-app/
│   ├── Dockerfile
│   ├── initserver.sh
│   ├── runserver.sh
│   ├── startserver.sh
│   ├── requirements.txt
│   │
│   ├── manage.py
│   ├── naive_uber/
│   │    ├── urls.py
│   │    ├── settings.py
│   │    ├── asgi.py
│   │    ├── wsgi.py
│   │    └── __init__.py
│   │
│   └── basic/
│        ├── migrations/
│        ├── static/
│        ├── templates/
│        │
│        ├── urls.py
│        ├── views.py
│        ├── models.py
│        ├── forms.py
│        ├── apps.py
│        ├── admin.py
│        ├── tests.py
│        └── __init__.py
│   
└── nginx/config/

