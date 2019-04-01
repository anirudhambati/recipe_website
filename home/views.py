from django.shortcuts import render

# Create your views here.
def explore(request):
    return render(request, 'home/explore.html')

def recipe(request):
    return render( request, 'home/recipe.html')
