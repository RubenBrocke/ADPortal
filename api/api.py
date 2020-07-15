from starlette.routing import Route
from starlette.responses import Response
import api.service
import api.flag
import api.exploit

api_routes = [
	Route("/api/services", api.service.Service),
	Route("/api/flags", api.flag.Flag),
	Route("/api/exploits", api.exploit.Exploit)
]