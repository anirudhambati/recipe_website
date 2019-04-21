from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#import cv2
import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.conf.urls.static import static
import datetime

# Create your views here.

#@login_required
def insert(request):
    if request.method == "POST":

        Rname = request.POST['Rname']
        ingredients = request.POST.getlist('ingredient')
        quantity = request.POST.getlist('quantity')
        option = request.POST.getlist('option')
        Steps = request.POST.getlist('Steps')
        Servings = request.POST['Servings']
        Description = request.POST['Description']
        Maketime = request.POST['Maketime']
        myfile = request.FILES['sentFile']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        f = request.FILES['sentFile']
        f="./media/"+str(myfile)
        s3 = boto3.client('s3')
        bucket = 'dbms2019'
        #print(type(str(f)))
        #print(f)
        #print('aa')
        file_name = str(f)
        key_name = str(myfile)
        #print('a')
        #print(file_name)
        #print(key_name)
        s3.upload_file(file_name, bucket, key_name)

        #ss config.signature_version = botocore.UNSIGNED
        # link=boto3.client('s3').generate_presigned_url('get_object', ExpiresIn=0, Params={'Bucket': bucket, 'Key': key_name})
        # print(link)
        #
        bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
        link = "https://s3-ap-southeast-1.amazonaws.com/{0}/{1}".format(
             bucket,
             key_name)
        dynamoDB = boto3.resource('dynamodb')
        dynamoTable = dynamoDB.Table('recipe')

        scan = dynamoTable.scan()
        count = len(scan['Items'])

        dynamoTable.put_item(
            Item={
                'R_id':int(count + 1),
                'name': Rname,
                'servings': Servings,
                'ingreditents': ingredients,
                'steps': Steps,
                'Region': 'Indian',
                'Maketime': Maketime,
                'Imglink': link,
                'Chefname': 'Anirudh',
                'Description': Description,
                }
        )

        dynamoTable = dynamoDB.Table('forum')
        scan = dynamoTable.scan()
        count2 = len(scan['Items'])
        now = datetime.datetime.now()


        dynamoTable.put_item(
            Item={
                'U_id': int(count2 + 1),
                'R_id':int(count + 1),
                'date': str(now.day + '/' + now.month + '/' + now.year),
                }
        )



    return render(request,'uploadforum/complected.html')

#@login_required
def home(request):
    return render(request,'uploadforum/fo.html')
