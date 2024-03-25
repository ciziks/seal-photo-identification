import docker

class Docker:
    def __init__(self, container_name: str) -> None:
        self.__client = docker.from_env()

    def is_running(self) -> bool:
        try:
            self.__client.ping()
            return True
        except docker.errors.APIError as e:
            return False

