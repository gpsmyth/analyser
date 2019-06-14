# pylint: disable=E1101
""" Using boto3 methods """
import click
import boto3

@click.command()
def cli():
    """ Understanding click decorator """
    click.echo("Hello World")


class InstanceToGet:
    """ Class about Instances """
    def __init__(self, name):
        # pylint complained here
        session = boto3.Session(profile_name=name)
        self._ec2 = session.resource('ec2')

    def list_instances(self):
        """ list the instances """
        for i in self._ec2.instances.all():
            try:
                # i.id is the same as i.instance_id so no need to duplicate
                print(', '.join((i.id,
                                 i.instance_type,
                                 i.placement['AvailabilityZone'],
                                 i.state['Name'],
                                 i.public_ip_address)))
            except TypeError:
                # how handle i.public_ip_address when None as in stopped
                print(', '.join((i.id,
                                 i.instance_type,
                                 i.placement['AvailabilityZone'],
                                 i.state['Name'])))


if __name__ == '__main__':
    MYINSTANCES = InstanceToGet("analyser")
    MYINSTANCES.list_instances()
    cli()
