# import requirements
import flask


class RestAPIService:
    """_summary_"""

    def __init__(self, estimator: any) -> None:
        self.__app = flask.Flask("mse1h2024-clock-ml-processing")
        self.__estimator = estimator

        self.__registerRoutes()

    def run(self) -> None:
        self.__app.run(
            host="0.0.0.0",
            port=22869,
        )

    def __registerRoutes(self) -> None:
        @self.__app.route("/process/estimation", methods=["POST"])
        def callEstimator():
            try:
                data = flask.request.json
                print(data)

                # result = self.__estimator.estimate(someParsedData) line will be implemented in the future

                return flask.jsonify({"result": "Estimation processed successfully."})
            except Exception as e:
                return flask.jsonify(
                    {"error": f"Internal server error: {str(e)}"},
                    500,
                )

        @self.__app.errorhandler(404)
        def notFound(error):
            return (
                flask.jsonify({"error": "The requested URL was not found on server."}),
                404,
            )


if __name__ == "__main__":
    pass
