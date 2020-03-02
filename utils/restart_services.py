import argparse
import sys
import boto3


class AWSService:
    pass

    @classmethod
    def __restart_service(cls, service: str, cluster: str):
        print("Starting restart " + service + " " + cluster)
        # Force new deployment
        if (self.updateService(service, cluster) == False):
            sys.exit(1)
        # Wait for service be stable
        try:
            waiter = self.client.get_waiter('services_stable')
            waiter.wait(
                cluster=cluster,
                services=[service]
            )
        except:
            print("Failed restart service after 40 checks.")
            sys.exit(1)
        print("Finished restart " + service + " " + cluster)

    @classmethod
    def setup_client(cls, aws_region: str):
        client = None
        try:
            client = boto3.client('ecs',region_name=aws_region)
        except Exception as e:
            print(e)
            sys.exit(1)
        return client

    @classmethod
    def restart_services(cls, services: str, cluster: str, aws_region: str = 'us-east-2'):

        services = services.split(' ')

        # TODO: execute in parallel
        for service in services:
            cls.__restart_service(service, cluster)


def parse_args():
    parser = argparse.ArgumentParser(description='Videos to images')
    parser.add_argument('indir', type=str, help='Input dir for videos')
    parser.add_argument('outdir', type=str, help='Output dir for image')
    return parser.parse_args()



if __name__ == '__main__':
    args = parse_args()
