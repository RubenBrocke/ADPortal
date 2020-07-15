from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from database import database
import sqlite3

class Flag(HTTPEndpoint):
    async def get(self, request):
        # Get possible filter data
        _filter = None
        if 'filter' in request.query_params:
            _filter = request.query_params['filter']

        # Get data from database
        res = database.get_flags(_filter)
        print(res)
        # Create JSON list
        flags = []
        for r in res:
            flags.append({"flag":r[1], "service":r[4]})
        return JSONResponse(flags)

    async def put(self, request):
        # Get relevant data
        try:
            flag = str(request.query_params['flag'])
            service_id = int(request.query_params['service_id'])
        except:
            return JSONResponse({"error":"invalid parameters"})

        # Commit to database
        try:
            database.insert_flag(flag, service_id)
        except sqlite3.IntegrityError as e:
            return JSONResponse({"error":str(e)})
        
        # Return flag
        ret = database.get_flags(flag)[0] # Get first (and hopefully only) result
        print(ret)
        return JSONResponse({"flag":ret[1],"service":ret[4]})
