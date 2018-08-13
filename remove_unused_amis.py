import boto3
client = boto3.client('ec2')

ec2 = boto3.resource('ec2')

instances = ec2.instances.all()
used_amis = []
for instance in instances:
    used_amis.append(instance.image_id)

print(used_amis)

# Remove duplicate amis
def remove_duplicates(amis):
    unique_amis = []
    for ami in amis:
        if ami not in unique_amis:
            unique_amis.append(ami)
    return unique_amis
unique_amis = remove_duplicates(used_amis)
print(unique_amis)

# get custom amis from the account

custom_images = ec2.instances.describe_images(
    Filters=[
            {
                'Name': 'state',
                'Values': [
                    'available'
                ]
            },
        ],
    Owners= ['self']
)

custom_amis_list = []
for image in custom_images['Images']:
    custom_amis_list.append(image['ImageId'])


for custom_ami in custom_amis_list:
    if custom_ami not in used_amis:
        print("deregistering ami {}".format(custom_ami))
        client.deregister_image(ImageId=image['ImageId'])