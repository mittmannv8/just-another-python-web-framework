
## This project is not another web framework. It was made for learning purposes only.


### The Framework
This web framework was created to run under WSGI specifications, so you can use any WSGI server to run it, just instantiate the App object, make the views and set the URLs:
```
from framework import App, JSONResponse

app = App()

def index(request):
    return JSONResponse({'status': 'OK'})

app.load_routes([
    '/', index,
])
```

## To run example app using gunicorn
```
gunicorn app.app:app -b 127.0.0.1:8080 --reload --chdir .
```
