# external imports
import tornado.template


class GraphiQLRequestHandler(tornado.web.RequestHandler):

    def initialize(self, schema=None, async=False):
        self._schema = schema

    def get(self):
        # import the template directory
        from nautilus.api.endpoints import template_dir
        # create the template loader
        template_loader = tornado.template.Loader(template_dir)
        # load the template from the file system
        template = template_loader.load('graphiql.html')
        # write the template to the client
        return self.finish(template.generate())
