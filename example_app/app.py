from framework import App, Middleware
from db import db

from . import views


# instancia a classe App
app = App()


# define o mapeamento das URLs para as views
urls = [
    ('/', views.index),
    ('/users', views.users)
]

# chama o helper para carregar as urls
app.load_routes(urls)


class SessionMiddleware(Middleware):
    """Middleware para injetar o usuário caso o token seja passado."""

    def on_request(self, request):
        token = request.headers.get('token')
        user = None
        if token:
            try:
                user = db.get('users', int(token))
            except Exception:
                pass

        request.user = user or {
            'name': 'Anonymous'
        }

        return request


class LoggerMiddleware(Middleware):
    """Middleware só para logar as requests."""

    def on_response(self, request, response):
        print('{} {} -> {} ({})'.format(
            request.method, request.path, response.status, request.user['name']
        ))
        return response


# carrega os middlewares
app.load_middlewares([
    SessionMiddleware(),
    LoggerMiddleware()
])
