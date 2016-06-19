# local imports
from nautilus.network.http import RequestHandler


class GraphiQLRequestHandler(RequestHandler):
    @aiohttp_jinja2('graphiql.jinja2')
    async def get(self):
        # write the template to the client
        return {}
