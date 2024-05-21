# import requirements

import flask
from PIL import Image
import io
import numpy as np


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
            port=745,
        )

    def __registerRoutes(self) -> None:
        """Register the routes for service."""

        @self.__app.route("/process/estimation", methods=["POST"])
        def callEstimator():
            """Handle the POST request to process image."""

            if "multipart/form-data" in flask.request.headers["Content-Type"]:
                try:
                    hours = int(flask.request.form.get("hours"))
                    minutes = int(flask.request.form.get("minutes"))
                    result = self.__estimator.estimate(
                        image=np.array(Image.open(io.BytesIO(flask.request.files.get('file').read()))),
                        time=(hours, minutes)
                    )

                    return flask.jsonify({"result": result})
                except:
                    return flask.jsonify({"error": "Failed to process image"})
            else:
                return (
                    flask.jsonify(
                        {"error": "Only multipart/form-data can be accepted"},
                    ),
                    400,
                )

        @self.__app.errorhandler(404)
        def notFound(error):
            """Handle the 404 error."""

            return (
                flask.jsonify({"error": "The requested URL was not found on server."}),
            ), 404


if __name__ == "__main__":
    pass
