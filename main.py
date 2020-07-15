from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.templating import Jinja2Templates
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from api.api import api_routes
from runner import Runner


r = Runner(b'FLAG_[\w]+')

templates = Jinja2Templates(directory='website/templates')
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})
async def flags(request):
    return templates.TemplateResponse('flags.html', {'request': request})


website_routes = [
    Mount('/static', app=StaticFiles(directory='website/static')),
    Route("/", endpoint=homepage),
    Route("/flags", endpoint=flags)
]

app = Starlette(debug=True, routes=api_routes + website_routes)

r.do_round()
