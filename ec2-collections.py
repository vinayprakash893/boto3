import boto3
ec2 = boto3.resource('ec2')
ec2.instances.filter(Filters=[
    {
        'Name': 'instance-state-name',
        'Values': ['running']
    }
]).stop()
