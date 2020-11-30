from django.shortcuts import render

# Create you views here.
def home(request):
    return render(request, 'home.html', {})