from typing import Callable, Dict, List, Tuple
from framework.http import HTMLResponse, HTTP_NOT_FOUND, Request, Response


class Middleware:
    """Classe base para a criação de middlewares."""

    def on_request(self, request: Request) -> Request:
        """
        Recebe, processa e retorna uma request, podendo ser a mesma ou criar
        uma nova.
        """
        return request

    def on_response(self, request: Request, response: Response) -> Response:
        """
        Recebe uma request e uma response, processa e retorna uma response,
        podendo ser a mesma ou criar uma nova.
        """
        return response


# declara classe principal da aplicação
class App:
    """Classe responsável pela aplicação.

    Ela contem as rotas e middlewares e lidará com as requisições vindas do
    servidor WSGI.
    """

    def __init__(self):
        """ Função que inicializa o objeto, ou seja, carrega todos os atributos."""
        self._routes = {}       # será nossa tabela de rotas/urls
        self._middlewares = []  # será nossa lista de moddlewares que serão executados

    def load_middlewares(self, middlewares: List[Middleware]) -> None:
        """
        Função para carregar os middlewares customizados do nosso app.

        Recebe uma lista de middlewares e salva no atributo _middlewares
        """
        self._middlewares.extend(middlewares)

    def add_route(self, route: str, view: Callable) -> None:
        """
        Função auxiliar para adicionar as rotas. (parecido com flask)

        Recebe uma rota (str) e uma view (função) e adiciona no mapeamento.
        """
        self._routes[route] = view

    # (parecido com Django)
    def load_routes(self, urls: List[Tuple[str, Callable]]) -> None:
        """
        Função auxiliar para adicionar as rotas por lista de rotas.

        Recebe uma lista de listas/tuplas contendo o mapeamento das rotas:
            [('/url', função),]
        """
        for route, view in urls:
            self.add_route(route, view)

    def call_all_request_middlewares(self, request: Request) -> Request:
        """
        Função que processa todos os middlewares para a request.

        Recebe uma request e retorna uma request.
        """
        for middleware in self._middlewares:
            request = middleware.on_request(request)

        return request

    def call_all_response_middlewares(
        self,
        request: Request,
        response: Response
    ) -> Response:
        """
        Função que processa todos os middlewares para a response.

        Recebe uma request e uma response e retorna uma response.
        """
        for middleware in self._middlewares:
            response = middleware.on_response(request, response)

        return response

    # __call__ permite que um objeto seja chamado como função
    def __call__(self, environ: Dict, start_response: Callable) -> List[bytes]:
        """__call__ permite um objeto ser executado como função.

        Será usada para permitir que um WSGI Server execute nosso objeto app
        como entrada de uma request.
        """

        # instancia o objeto de Request
        request = Request(environ)

        # processa as middewares (somente request)
        request = self.call_all_request_middlewares(request)

        # pega a view(função) mapeada para URL requisitada
        view = self._routes.get(request.path)

        if view:
            # executa a view e espera receber uma Response
            response = view(request)
        else:
            # não encontrou a url no mapeamento
            response = HTMLResponse(
                data='<h1>Not Found</h1>',
                status=HTTP_NOT_FOUND,
            )

        # processa as middewares (somente response)
        request = self.call_all_response_middlewares(request, response)

        # executa o callback do WSGI Server
        start_response(response.status, response.headers)

        # processa o resultado da response e retorna para WSGI Server
        return [response.make_response()]
