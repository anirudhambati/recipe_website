from django.shortcuts import render
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Create your views here.
def forum(request):
    x=request.session['uid']
    print(x)
    dynamoDB=boto3.resource('dynamodb')
    dynamoTable=dynamoDB.Table('forum')
    # fe = Attr('U_id').eq(x)
    # response=dynamoTable.scan(FilterExpression=fe)
    # print(response['Items'])
    # if(response['Items']==[]):
    #     recipe=[]
    # else:
    #     dynamoDB=boto3.resource('dynamodb')
    #     dynamoTable=dynamoDB.Table('recipe')
    #     recipe=[]
    #     for i in response['Items']:
    #         scan=dynamoTable.get_item(
    #         Key={
    #         'R_id':i['R_id'],
    #         }
    #         )
    #         recipe.append(scan['Item'])
    #     print(recipe)
    # data={'recipe':recipe}
    return render(request, 'forum/forum.html')
