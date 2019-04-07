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

# Create your views here.

#@login_required
def insert(request):
    if request.method == "POST":
        Rname = request.POST['Rname']
        print("\nRname:",Rname)
        ingredients = request.POST.getlist('ingredient')
        print("\ningredients:",ingredients)
        quantity = request.POST.getlist('quantity')
        print("\nquantity:",quantity)
        option = request.POST.getlist('option')
        print("\noption:",option)
        Steps = request.POST.getlist('Steps')
        print("\nSteps:",Steps)
        Servings = request.POST['Servings']
        print("\nServings:",Servings)
        Description = request.POST['Description']
        print("\nDescription:",Description)
        Maketime = request.POST['Maketime']
        print("\nMaketime:",Maketime)
        myfile = request.FILES['sentFile']
        print("\nmyfile:",myfile)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        f = request.FILES['sentFile']
        f="./media/"+str(myfile)
        s3 = boto3.client('s3')
        bucket = 'dbms2k19'
        #print(type(str(f)))
        #print(f)
        #print('aa')
        file_name = str(f)
        key_name = str(myfile)
        #print('a')
        #print(file_name)
        #print(key_name)
        #s3.upload_file(file_name, bucket, key_name)

        # config.signature_version = botocore.UNSIGNED
        # link=boto3.client('s3').generate_presigned_url('get_object', ExpiresIn=0, Params={'Bucket': bucket, 'Key': key_name})
        # print(link)
        #
        # bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
        # object_url = "https://s3-ap-southeast-1.amazonaws.com/{0}/{1}".format(
        #     bucket,
        #     key_name)
    return render(request,'uploadforum/complected.html')

#@login_required
def home(request):
    return render(request,'uploadforum/fo.html')
