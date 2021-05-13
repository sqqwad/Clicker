from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):
    user = User.objects.filter(id=request.user.id).first()
    if user == None:
        return redirect('login')

    maincycle = models.MainCycle.objects.filter(user=request.user).first()
    return render(request, 'index.html', {'maincycle': maincycle})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            maincycle = models.MainCycle()
            maincycle.user = user
            maincycle.save()

            # authenticate
            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})

    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@api_view(['GET'])
def call_click(request):
    maincycle = models.MainCycle.objects.filter(user=request.user).first()
    maincycle.click()
    maincycle.save()

    return Response(maincycle.click_count)
