# import requirements
import importlib
import asyncio

# import project modules
# restAPIModule = importlib.import_module("backend-services.restapi.rest")
rabbitModule = importlib.import_module("backend-services.rabbitmq.rabbit")
# here will be import RabbitMQService class in the future


class Core:
    """Class for init ML-processing modules and REST-API/message broker services.

    This class serves as the core component of the system, responsible for initializing and coordinating
    machine learning processing modules, REST-API and message broker services.

    """

    def __init__(self) -> None:
        """Initialization the core for ML-processing."""
        # self.__estimator = estimationModule.Estimator()
        # self.__restAPIService = restAPIModule.RestAPIService(
         #   estimator=self.__estimator,
        # )
        self.__rabbitMQService = rabbitModule.RabbitmMQService()

    async def start(self) -> None:
        """Run the REST-API service"""

        # self.__restAPIService.run()

        await self.__rabbitMQService.run()


if __name__ == "__main__":
    core = Core()
    asyncio.run(core.start())
