# supondo que o nome do arquivo seja site.py
# para executar pelo gunicorn:
# gunicorn site:app --reload

# - return html page
# - Response
# - POST
# - Request
# - middlewares
# - auth decorator


# declara classe principal da aplicação
class App:

    # função que inicializa o objeto
    def __init__(self):
        self._routes = {}  # será nossa tabela de rotas/urls

    # função auxiliar para adicionar as rotas
    # (parecido com flask)
    def add_route(self, route, view):
        # adiciona a url como chave e a função como valor
        self._routes[route] = view

    # função auxiliar para adicionar as rotas por lista de rotas
    # (parecido com Django)
    def load_routes(self, urls):
        for route, view in urls:
            self.add_route(route, view)

    # __call__ permite que um objeto seja chamado como função
    def __call__(self, environ, start_response):

        route = environ['PATH_INFO']

        view = self._routes.get(route)

        if view:
            response_headers = [('Content-type', 'application/json')]
            start_response("200 OK", response_headers)
            return [view()]
        else:
            response_headers = [('Content-type', 'text/html')]
            start_response('404 Not Found', response_headers)
            return ['burro, não tem nada aqui'.encode()]


# instancia a classe App
app = App()


# view para a url /
def index():
    return b'{"page": "/"}'


# view para a url /users
def users():
    return b'{"page": "/users"}'


# define o roteamento das URLs para as views
urls = [
    ('/', index),
    ('/users', users)
]

# chama o helper para carregar as urls
app.load_routes(urls)
