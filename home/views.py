from django.shortcuts import render,HttpResponse,redirect
import boto3
from boto3.dynamodb.conditions import Key, Attr
import random

# Create your views here.
def explore(request):
    uid=request.session['uid']
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('recipe')
    names=[]
    imglinks=[]
    rids=[]
    response = dynamoTable.scan()
    for i in response['Items']:
        names+=[i['name']]
        imglinks+=[i['Imglink']]
        rids+=[i['R_id']]
    name=[]
    imglink=[]
    rid=[]
    for x in range(0,4):
        rand=random.randint(1,100)
        name.append(names[rand])
        imglink.append(imglinks[rand])
        rid.append(rids[rand])

    return render(request, 'home/explore.html',{'data':zip(name,imglink,rid),'uid':uid})


def tryout(request):
    uid=request.session['uid']
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('recipe')
    names=[]
    imglinks=[]
    rids=[]
    response = dynamoTable.scan()
    for i in response['Items']:
        names+=[i['name']]
        imglinks+=[i['Imglink']]
        rids+=[i['R_id']]
    name=[]
    imglink=[]
    rid=[]
    for x in range(0,4):
        rand=random.randint(1,100)
        name.append(names[rand])
        imglink.append(imglinks[rand])
        rid.append(rids[rand])


    #### RECOMMENDOR SYSTEMS ####

    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('Users')
    scan=dynamoTable.scan()
    count=len(scan['Items'])
    u=[]

    for i in range(1,count+1):
        u.append(i)

    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('Recommend')
    scan=dynamoTable.scan()

    rvu=[]
    r=[]

    for i in scan['Items']:
        rvu.append(i['U_id'])
        r.append(i['R_id'])

    rvu_t = [list(i) for i in zip(*rvu)]

    ### FAMOUS ###
    top_recipes = [sum(i) for i in zip(*rvu_t)]

    n = len(top_recipes)
    temp_r = r

    for a in range(0, n):
        for j in range(0, n-a-1):
            if top_recipes[j] > top_recipes[j+1]:
                top_recipes[j], top_recipes[j+1] = top_recipes[j+1], top_recipes[j]
                temp_r[j], temp_r[j+1] = temp_r[j+1], temp_r[j]


    most_famous = []
    trending = []

    for i in range(0, 8):
        most_famous.append(temp_r[i])

    for i in range(6, 10):
        trending.append(temp_r[i])
    ################

    uid = request.session['uid']
    sim = []
    i = u.index(uid)
    user_table = rvu_t[i-1]
    for user in rvu_t:
        sim.append(sum(user or user_table))

    temp_r = u

    for a in range(0, n):
        for j in range(0, n-a-1):
            if sim[j] > sim[j+1]:
                sim[j], sim[j+1] = sim[j+1], sim[j]
                temp_r[j], temp_r[j+1] = temp_r[j+1], temp_r[j]



    #############################

    return render(request, 'home/tryout.html',{'data':zip(name,imglink,rid)})


def recipe(request, id):
    print(id)
    print(type(id))
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('recipe')
    response = dynamoTable.scan(
        FilterExpression=Attr('R_id').eq(int(id))
    )
    #data extraction
    servings    =response['Items'][0]['servings']
    ingredients =response['Items'][0]['ingreditents']
    chefname    =response['Items'][0]['Chefname']
    img         =response['Items'][0]['Imglink']
    maketime    =response['Items'][0]['Maketime']
    region      =response['Items'][0]['Region']
    steps       =response['Items'][0]['steps']
    name        =response['Items'][0]['name']
    description = response['Items'][0]['Description']

    print(description)
    x = [x.strip() for x in eval(steps)]
    del x[-1]

    n = len(x)

    x1 = [x1.strip() for x1 in eval(ingredients)]
    del x1[-1]

    n1 = len(x1)


    data = {'servings':servings,
            'ingredients':zip([x1+1 for x1 in list(range(n1))], x1),
            'chefname':chefname,
            'img':img,
            'maketime':maketime,
            'region':region,
            'steps':zip([x+1 for x in list(range(n))], x),
            'name':name,
            'n':n,
            'description':description[1:-1],
            'l':[x+1 for x in list(range(n))]}

    return render( request, 'home/recipe.html', data)

def base(request):
    return render(request, 'home/base.html')

def register(request):
    return render(request, 'register/login.html')

def findchefs(request):

    dynamoDB = boto3.resource('dynamodb')
    dynamoTable = dynamoDB.Table('Users')


    fe = Attr('email').contains('yashukikkuri@gmail.com')

    response = dynamoTable.scan(
         FilterExpression = fe,
         )

    following = response['Items'][0]['following']

    scan = dynamoTable.scan()
    top5 = []
    followers5=[]
    count = 0

    for i in scan['Items']:
        if(i['U_id'] in following):
            continue
        else:
            count+=1
            if(count>5):

                if(i['followers']>min(followers5)):
                    index=followers5.index(min(followers5))

                    a = []
                    response2 = dynamoTable.scan(
                        FilterExpression = Attr('U_id').eq(int(i['U_id']))
                    )
                    fname = response2['Items'][0]['fname']
                    uname = response2['Items'][0]['uname']
                    lname = response2['Items'][0]['lname']
                    followers = response2['Items'][0]['followers']

                    a.append(i['U_id'])
                    a.append(fname)
                    a.append(lname)
                    a.append(uname)
                    a.append(followers)

                    top5[index] = a

                    print(followers5)
                    print("\n\n")
                    print(top5)
                    print("\n\n")

            else:
                a = []
                response2 = dynamoTable.scan(
                    FilterExpression = Attr('U_id').eq(int(i['U_id']))
                )
                fname = response2['Items'][0]['fname']
                uname = response2['Items'][0]['uname']
                lname = response2['Items'][0]['lname']
                followers = response2['Items'][0]['followers']

                a.append(i['U_id'])
                a.append(fname)
                a.append(lname)
                a.append(uname)
                a.append(followers)

                top5.append(a)
                followers5.append(i['followers'])


    user_details = {'data': top5}

    return render(request, 'home/findchefs.html', user_details)


def registered(request):
    first = request.POST['First']
    last = request.POST['Last']
    email = request.POST['email']
    password = request.POST['password']
    uname=last+first
    dynamoDB = boto3.resource('dynamodb')
    dynamoTable = dynamoDB.Table('Users')
    fe = Attr('email').eq(email)
    response = dynamoTable.scan(FilterExpression = fe)

    if (response['Items']==[]):
        response=dynamoTable.scan()
        if (response['Items']==[]):
            sno = 1
        else:
            sno = len(response['Items'])+1
        dynamoTable.put_item(
        Item={
        'U_id':sno,
        'fname':first,
        'lname':last,
        'uname':uname,
        'email':email,
        'password':password,
        'lat':'80',
        'long':'35',
        'followers':0,
        'following':[],
        'D_id':0
        }
        )

    else:
        # sno=len(response['Items'])+1
        print('email already exists')

    return render(request, 'home/index.html')

def home(request):
    request.session['uid']=0
    return render(request, 'home/index.html')

def login(request):
    flag = 0
    email=request.POST['email']
    password=request.POST['password']
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('Users')
    fe = Attr('email').eq(email)
    response=dynamoTable.scan(FilterExpression=fe)
    if (response['Items']==[]):
        res = 'You have not registered yet. Please register first to continue'
        flag = 1
        print("register first")
    else:
        print(response['Items'][0]['password'])
        id = int(response['Items'][0]['U_id'])
        request.session['uid']=id
        if(response['Items'][0]['password'] == password):
            return redirect('home:tryout')
        else:
            res = 'The password you have entered is wrong'
            flag = 1
    return render(request, 'register/login.html', {'res':res, 'flag':flag})


def search(request):
    return render(request,'search/search.html')
