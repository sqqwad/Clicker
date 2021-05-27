from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from .serializers import MainCycleSerializer, BoostSerializer
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.forms import UserCreationForm
from logging import getLogger


# Create your views here.
def index(request):
    user = request.user

    if isinstance(user, AnonymousUser) or user is None:
        return redirect('login')

    maincycle = models.MainCycle.objects.filter(user=user).first()
    boosts = maincycle.boost_set.all()

    return render(request, 'index.html', {
        'maincycle': maincycle,
        'boosts': boosts
    })


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


def boosts(args):
    pass


@api_view(['GET'])
def call_click(request):
    maincycle = models.MainCycle.objects.filter(user=request.user).first()
    maincycle.click()

    boosts = None
    is_level_up = maincycle.is_level_up()

    maincycle.save()
    if is_level_up:
        boost = models.Boost(
            maicycle=maincycle,
            level=maincycle.level,
            power=maincycle.level*20,
            price=maincycle.level*50,
        )
        boost.save()

        boosts = [BoostSerializer(boost).data for boost in maincycle.boost_set.all()]

    return Response({
        'maincycle': MainCycleSerializer(maincycle).data,
        'boosts': boosts,
    })

    
@api_view(['POST'])
def buy_boost(request):
    boost_id = request.data['boost_id']

    boost = models.Boost.objects.get(id=boost_id)
    maincycle = boost.update()
    boost.save()

    boosts = [BoostSerializer(boost).data for boost in maincycle.boost_set.all()]

    return Response({
        'maincycle': MainCycleSerializer(maincycle).data,
        'boosts': boosts,
    })


