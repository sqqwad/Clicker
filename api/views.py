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
    user = User.objects.filter(id=request.user.id).first()

    if user is None:
        return redirect('login')

    maincycle = models.MainCycle.objects.filter(user=request.user).first()
    boosts = models.Boost.objects.filter(main_cycle=maincycle)

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

            boost = models.Boost(main_cycle=maincycle)
            boost.save()

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

    boosts = None
    is_level_up = maincycle.is_level_up()

    maincycle.save()
    if is_level_up == 1:
        boost = models.Boost(main_cycle=maincycle, power=maincycle.level * 20, price=maincycle.level * 50)
        boost.save()

        boosts = [BoostSerializer(boost).data for boost in maincycle.boost_set.all()]
    elif is_level_up == 2:
        boost = models.Boost(main_cycle=maincycle, power=maincycle.level * 10, price=maincycle.level * 100, boost_type=1)
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


