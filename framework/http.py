import json

from typing import Dict
from urllib.parse import parse_qsl

HTTP_OK = '200 OK'
HTTP_NOT_FOUND = '404 Not Found'
HTTP_CREATED = '201 Created'


class Request:
    """
    Classe responsável por agrupar imnformações pertinentes a requisição (entrada).
    """

    def __init__(self, environ: Dict) -> None:
        body = environ.get('wsgi.input')

        self.method = environ.get('REQUEST_METHOD')
        self.content_type = environ.get('CONTENT_TYPE')
        self.path = environ.get('PATH_INFO')
        self._body = body.read() if body else b''
        self.environ = environ
        self.query = dict(parse_qsl(environ.get('QUERY_STRING')))

    @property
    def data(self):
        if self.content_type == 'application/json':
            return json.loads(self._body.decode())
        elif self.content_type == 'application/x-www-form-urlencoded':
            return dict(parse_qsl(self._body.decode()))
        return self._body.decode()

    @property
    def headers(self) -> Dict:
        """
        Processa o environ enviado pelo WSGI Server e extrai somente os headers.
        """
        return {
            header.lower().replace('http_', ''): value
            for header, value in self.environ.items()
            if header.startswith('HTTP_')
        }


class Response:
    """
    Classe base para classes do tipo Response.
    """
    content_type = None

    def __init__(self, data, status=HTTP_OK, headers=None):
        # não é uma boa prática usar estruturas mutáveis como parametro default
        headers = [] if headers is None else headers
        headers.append(self.content_type)

        self.data = data
        self.status = status
        self.headers = headers

    def make_response(self):
        """Função que irá gerar nosso conteúdo final da response."""
        if isinstance(self.data, str):
            return self.data.encode()

        return self.data


class HTMLResponse(Response):
    """Classe do tipo Response especializada em retornar conteúdos HTML."""
    content_type = ('Content-type', 'text/html')


class JSONResponse(Response):
    """Classe do tipo Response especializada em retornar conteúdos JSON."""
    content_type = ('Content-type', 'application/json')

    def make_response(self):
        if isinstance(self.data, (dict, list)):
            self.data = json.dumps(self.data).encode()

        return super().make_response()
