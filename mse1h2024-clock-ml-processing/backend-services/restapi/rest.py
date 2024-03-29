# import requirements
import flask

class RestAPIService:
    """Class for handing with backend data using REST-API."""

    def __init__(self, estimator: any) -> None:
        """
        Initialization the REST-API Service.

        Parameters
        ----------
        estimator : any
            Estimator class object for processing data and return result

        """

        self.__app = flask.Flask("mse1h2024-clock-ml-processing")
        self.__estimator = estimator

        self.__registerRoutes()

    def run(self) -> None:
        """Start the Flask application to serve incoming requests."""

        self.__app.run(
            host="0.0.0.0",
            port=22869,
        )

    def __registerRoutes(self) -> None:
        """Register the routes for service."""

        @self.__app.route("/process/estimation", methods=["POST"])
        def callEstimator():
            """Handle the POST request to process image."""
            
            if flask.request.headers['Content-Type'] == 'image/png':
                data = flask.request.data

                return flask.jsonify({"result": 5})
            else:
                return flask.jsonify(
                    {"error": "Only image/png can be accepted"},
                ), 400

        @self.__app.errorhandler(404)
        def notFound(error):
            """Handle the 404 error."""

            return (
                flask.jsonify({"error": "The requested URL was not found on server."}),
            ), 404


if __name__ == "__main__":
    pass
