from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {"id": 1, "name": "Let's learn python"},
#     {"id": 2, "name": "Design with me"},
#     {"id": 3, "name": "Frontend Developers"},
# ]


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            # Flash message
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username OR password does not exist")

    context = {}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def home(request):
    # expression_if_true if condition else expression_if_false
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    # topic__name, to query upwards to the parent
    # topic__name__icontains - contains means it will check if it contains letters in query string. i.e. Py for Python. i stands for case insensitive
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "base/home.html", context)


def room(request, id):
    room = Room.objects.get(id=id)

    context = {"room": room}
    return render(request, "base/room.html", context)


# @login_url will redirect the user to the login page if the user is not authenticated
@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    # if I don't know the room id then I should not be able to edit the room
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "base/delete.html", {"obj": room})
