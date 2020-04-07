import boto3
from threading import Thread
from typing import List
import sys


class ECS:
    def __init__(self, aws_region: str = "us-east-2"):
        try:
            self.client = boto3.client("ecs", region_name=aws_region)
        except Exception as e:
            print(e)
            sys.exit(1)
        pass

    @staticmethod
    def __update_service(client, service, cluster, args: dict):
        print(f"Starting update of service '{cluster}::{service}'...", flush=True)
        try:
            response = client.update_service(cluster=cluster, service=service, **args)
        except Exception as e:
            print(e)
            sys.exit(1)
        try:
            # Wait for service be stable
            waiter = client.get_waiter("services_stable")
            waiter.wait(cluster=cluster, services=[service])
        except:
            print("Failed updating service after 40 checks.", flush=True)
            sys.exit(1)
        print(f"Finished updating {cluster}::{service}", flush=True)

    def __update_services(self, services: List[str], cluster: str, args: dict):
        # create a list of threads
        threads = []
        for service in services:
            process = Thread(
                target=ECS.__update_service, args=[self.client, service, cluster, args],
            )
            process.start()
            threads.append(process)
        print("... Waiting for action to be complete", flush=True)
        # sync
        for process in threads:
            process.join()
            # print(f"result: {process.get()}", flush=True)
        print("syncing done", flush=True)

    def restart_services(self, services: List[str], cluster: str):
        self.__update_services(services, cluster, {"forceNewDeployment": True})

    def scale_services_to(
        self, services: List[str], cluster: str, nr_tasks_per_service: int
    ):
        self.__update_services(
            services,
            cluster,
            {"forceNewDeployment": True, "desiredCount": nr_tasks_per_service},
        )

    def pause_services(self, services: List[str], cluster: str):
        self.__update_services(
            services, cluster, {"forceNewDeployment": True, "desiredCount": 0}
        )
