import cherrypy

from pymocky.models.mapping_request import MappingRequest


def to_mapper_request():
    dic = {
        "method": cherrypy.request.method,
        "url": cherrypy.url(),
        "headers": cherrypy.request.headers,
        "query_string": cherrypy.request.query_string,
    }

    if cherrypy.request.process_request_body:
        dic["body"] = cherrypy.request.body.read()
        dic["form_fields"] = cherrypy.request.body.params

    return MappingRequest(None, "default", dic)


setattr(cherrypy, "to_mapper_request", to_mapper_request)
