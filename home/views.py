from django.shortcuts import render,HttpResponse
import boto3
from boto3.dynamodb.conditions import Key, Attr


# Create your views here.
def explore(request):
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('recipe')
    fe = Attr('Region').contains('Indian')
    names=[]
    imglinks=[]
    rids=[]
    response = dynamoTable.scan(
        FilterExpression=fe,
        )
    for i in response['Items']:
        names+=[i['name']]
        imglinks+=[i['Imglink']]
        rids+=[i['R_id']]
    return render(request, 'home/explore.html',{'data':zip(names,imglinks,rids)})


def recipe(request):
    return render( request, 'home/recipe.html')



def register(request):
    return render(request,'register/login.html')


def registered(request):
    first=request.POST['First']
    last=request.POST['Last']
    email=request.POST['email']
    password=request.POST['password']

    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('Users')
    fe = Attr('email').eq(email)
    response=dynamoTable.scan(FilterExpression=fe)

    if (response['Items']==[]):
        response=dynamoTable.scan()
        if (response['Items']==[]):
            sno=1
        else:
            sno=len(response['Items'])+1
        dynamoTable.put_item(
        Item={
        'uid':str(sno),
        'fname':first,
        'lname':last,
        'email':email,
        'password':password,
        'lat':'80',
        'long':'35',
        }
        )
            # response=dynamoTable.get_item(
            # Key={
            # 'fname':'Yashwanth',
            # 'email':'yashukikkuri@gmail.com'
            # }
            # )

    else:
        # sno=len(response['Items'])+1
        print('email already exists')

    return HttpResponse("hii")


def login(request):
    print("####################")

    email=request.POST['email']
    password=request.POST['password']
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('Users')
    fe = Attr('email').eq(email)
    response=dynamoTable.scan(FilterExpression=fe)
    if (response['Items']==[]):
        print("register first")
    else:
        print(response['Items'][0]['password'])
        if(response['Items'][0]['password']==password):
            print('You are ready to go in')
        else:
            print("Got you bitch")
    return HttpResponse('hellooooo')