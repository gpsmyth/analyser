# pylint: disable=E1101
""" Using boto3 methods """
import click
import boto3

def filter_instances(project, name):
    """ If Project Tag is provided, then filtering is applied """
    # session = boto3.Session(profile_name="analyser")
    try:
        session = boto3.Session(profile_name=name)
    except:
        # botocore.exceptions.ProfileNotFound
        # Use drfualt known user
        name = "analyser"
        session = boto3.Session(profile_name=name)
        print("Using correct userid {0}".format(name))

    ec2 = session.resource('ec2')

    """ list the instances """
    instances = []

    print (project)
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
        print("Filtering")
    else:
        instances = ec2.instances.all()

    return instances


@click.command()
def cli():
    """ Understanding click decorator """
    click.echo("Hello World")

@click.group()
def instances():
    """ Commands for instances """

@instances.command('list')
@click.option('--project', default=None, help="Only Instances for project (tag Project:<name>")
@click.option('--name', default="analyser", help="Authorised API userid")
def InstanceToGet(project, name):
    """ Info about Instances using Project tag like --project=<name>"""
    
    instances = filter_instances(project, name)

    for i in instances:
        tags = { t['Key'] : t['Value'] for t in i.tags or [] }
        try:
            # i.id is the same as i.instance_id so no need to duplicate
            print(', '.join((i.id,
                                i.instance_type,
                                i.placement['AvailabilityZone'],
                                i.state['Name'],
                                i.public_ip_address,
                                tags.get('Project', '<No Project>'))))
        except TypeError:
            # how handle i.public_ip_address when None as in stopped
            print(', '.join((i.id,
                                i.instance_type,
                                i.placement['AvailabilityZone'],
                                i.state['Name'],
                                tags.get('Project', '<No Project>'))))

    return


@instances.command('stop')
@click.option('--project', default=None, help="Only Instances for project (tag Project:<name>")
@click.option('--name', default="analyser", help="Authorised API userid")
def stop_instances(project, name):
    """ Stop EC2 Instances using Project Tag """
    instances = filter_instances(project, name)

    for i in instances:
        print("Stopping instance {0}".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None, help="Only Instances for project (tag Project:<name>")
@click.option('--name', default="analyser", help="Authorised API userid")
def start_instances(project, name):
    """ Start EC2 Instances using Project Tag """
    instances = filter_instances(project, name)

    for i in instances:
        print("Starting instance {0}".format(i.id))
        i.start()

    return


if __name__ == '__main__':
    # cli()
    instances()
