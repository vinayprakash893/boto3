import boto3

ec2 = boto3.resource('ec2', region_name='ap-south-1')
client = boto3.client('ec2','ap-south-1')

instances = ec2.instances.filter(InstanceIds=['i-0067eeaab6c8188fd'])

image_ids = []

for instance in instances:
    image = instance.create_image(Name='Demo Boto - '+instance.id, Description='Demo Boto'+instance.id)
    image_ids.append(image.id)

print("Images to be copied {} ".format(image_ids))

# Get waiter for image_available
waiter = client.get_waiter('image_available')

# Wait for Images to be ready
waiter.wait(Filters=[{
    'Name': 'image-id',
    'Values': image_ids
}])

# Copy Images to the region, us-east-1
client = boto3.client('ec2', region_name='us-east-1')
for image_id in image_ids:
    client.copy_image(Name='Boto3 Copy'+image_id, SourceImageId=image_id, SourceRegion='ap-south-1')



