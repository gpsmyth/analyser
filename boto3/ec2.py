# pylint: disable=E1101
""" Using boto3 methods """
import boto3

class InstanceToGet:
    """ Class about Instances """
    def __init__(self, name):
        # pylint complained here
        session = boto3.Session(profile_name=name)
        self._ec2 = session.resource('ec2')

    def list_instances(self):
        """ list the instances """
        for i in self._ec2.instances.all():
            print(i)

if __name__ == '__main__':
    MYINSTANCES = InstanceToGet("analyser")
    MYINSTANCES.list_instances()
    