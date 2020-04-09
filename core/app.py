import falcon
import json


from .runner import main_runner, health_check_runner
from .constants import ROUTER


class Filter(object):
    def validate_route(self, route):
        """ Check if route is valid """

        for router in ROUTER:
            if router.value == route:
                return True
        return False

    @staticmethod
    def handleServerError(response, message="Unknown error occurred"):
        """ Error message handler """
        # TODO logger
        response.media = {"message": message}
        response.status = falcon.HTTP_500

    def on_post(self, req, res, route):
        valid_route = self.validate_route(route)
        if not valid_route:
            self.handleServerError(res, "Invalid route")
            return False

        try:
            body = json.loads(req.stream.read())
        except Exception:
            self.handleServerError(res, "Invalid request body")
            return False

        new_body = main_runner(body, route)
        res.media = new_body
        res.status = falcon.HTTP_200

        return True


class HealthCheck(object):
    """ Health check endpoint to make sure server has been started properly """

    def on_get(self, req, res):
        res.status = falcon.HTTP_200


api = falcon.API()
api.add_route("/filter/{route}", Filter())
api.add_route("/health", HealthCheck())
