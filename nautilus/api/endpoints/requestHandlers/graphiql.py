# external imports
import aiohttp_jinja2
# local imports
from nautilus.network.http import RequestHandler


class GraphiQLRequestHandler(RequestHandler):

    @aiohttp_jinja2.template('graphiql.html')
    async def get(self):
        # write the template to the client
        return {}
