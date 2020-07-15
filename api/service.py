from database import database
import sqlite3
from starlette.responses import PlainTextResponse
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request

# Api and Data for a service

class Service(HTTPEndpoint):
    async def get(self, request):
        # Get data from database
        res = database.get_services()

        # Create JSON list
        services = []
        for r in res:
            services.append({"id":r[0], "name":r[1], "port":r[2]})

        # Return json response
        return JSONResponse(services)

    async def put(self, request):
        # Get relevant data
        name = str(request.query_params['name'])
        port = int(request.query_params['port'])

        # Commit to database
        try:
            database.insert_service(name, port)
        except sqlite3.IntegrityError:
            return JSONResponse({"error":"service already in database"})

        # Return service
        return JSONResponse({"name":name, "port":port})