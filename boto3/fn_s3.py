# pylint: disable=E1101
""" Using boto3 methods """
import click
import boto3

@click.command()
def cli():
    """ Understanding click decorator """
    click.echo("Hello World")


def get_session(name):
    try:
        session = boto3.Session(profile_name=name)
    except:
        # botocore.exceptions.ProfileNotFound
        # Use drfualt known user
        name = "analyser"
        session = boto3.Session(profile_name=name)
        print("Using correct userid {0}".format(name))

    s3 = session.resource('s3')
    return s3


@click.group()
def s3_instances():
    """ Commands for s3 instances """


@s3_instances.command('list-buckets')
@click.option('--name', default="analyser", help="Authorised API userid")
def list_buckets(name):
    """ Get the list of all buckets """
    s3 = get_session(name)

    """ list the buckets """
    for bucket in s3.buckets.all():
        print(bucket.name)


@s3_instances.command('list-bucket-objects')
@click.argument('bucket')
@click.option('--name', default="analyser", help="Authorised API userid")
def list_bucket_objects(name, bucket):
    """ Get the list of all objects within a bucket """

    s3 = get_session(name)
    bucket = s3.Bucket(bucket)
    for obj in bucket.objects.all():
        print(obj)


if __name__ == '__main__':
    # cli()
    s3_instances()
