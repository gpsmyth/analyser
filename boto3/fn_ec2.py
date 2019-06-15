# pylint: disable=E1101
""" Using boto3 methods """
import click
import boto3

@click.command()
def cli():
    """ Understanding click decorator """
    click.echo("Hello World")

@click.command()
@click.option('--project', default=None, help="Only Instances for project (tag Project:<name>")
@click.option('--name', default="analyser", help="Authorised API userid")
def InstanceToGet(project, name):
    """ Info about Instances """
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


if __name__ == '__main__':
    # cli()
    InstanceToGet()
