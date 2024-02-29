# import requirements
import flask
import requests


class RestAPIService:
    """_summary_"""

    def __init__(self) -> None:
        self.__app = flask.Flask("mse1h2024-clock-ml-processing")
        self.__registerRoutes()

    def run(self) -> None:
        self.__app.run(host="0.0.0.0", port=22869)

    def __registerRoutes(self) -> None:
        @self.__app.route("/process/estimation", methods=["POST"])
        def callEstimator():
            if flask.request.method == "POST":
                data = flask.request.json
                print(data)

                return flask.jsonify({"message": "Estimation processed successfully."})


if __name__ == "__main__":
    service = RestAPIService()
    service.run()

    # # Отправка ping запроса
    # url = "http://localhost:22869/ping"
    # response = requests.get(url)
    # print(response.text)  # Ожидаемый результат - 'pong'
