from framework.http import HTMLResponse, JSONResponse, HTTP_CREATED
from db import db


# view para a url /
def index(request):
    html = '''
    <html>
        <head>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>Olá {}</h1>
            <form action="/users" method="POST">
                <input type="text" name="name" />
                <input type="text" name="age" />
                <button type="submit">Cadastrar</button>
            </form>
        </body>
    </html>
    '''.format(request.user['name'])

    return HTMLResponse(data=html)


# view para a url /users
def users(request):
    if request.method == 'POST':
        user = db.insert('users', request.data)

        return JSONResponse(user, status=HTTP_CREATED)

    data = db.get('users')
    return JSONResponse(data=data)
