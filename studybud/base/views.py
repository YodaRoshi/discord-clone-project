from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm, MyUserCreationForm

User = get_user_model()


def load(request):
    fh = open('base/data.txt').readlines()

    for line in fh:
        row = line.split(',')
        username, email,password, firstname, lastname,cellphone, is_staff, is_superuser = [i.strip() for i in row]

        if User.objects.filter(email=email).first() is None:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                is_staff=eval(is_staff),
                is_superuser=eval(is_superuser),
            )
            print(f'{email} has beencreated')
        else:
            print(f'{email} already exists')
        
    return HttpResponse('Users Created')


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('base:home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home')

        else:
            messages.error(request, 'Email OR Password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('base:home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # we are not saving data here because we want to clean up a bit
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics,
               'room_messages': room_messages}

    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('base:room', pk=room.id)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, "base/room.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    if user.is_active is False:
        if request.user.is_superuser is False:
            return HttpResponse('You are not allowed here')
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='base:login')
def createRoom(request):

    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('base:home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='base:login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user is not room.host:
        if request.user.is_superuser is False:
            return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('base:home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='base:login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user is not room.host:
        if request.user.is_superuser is False:
            return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        if room.topic is not None:
            topic = Topic.objects.get(pk=room.topic.pk)
            if topic.room_set.count() == 1:
                topic.delete()
        room.delete()
        return redirect('base:home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='base:login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user is not message.user:
        if request.user.is_superuser is False:
            return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        if message.user.message_set.filter(room=message.room).count() == 1:
            room = Room.objects.get(id=message.room.id)
            room.participants.remove(message.user)
        message.delete()
        return redirect('base:home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='base:login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('base:user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html',{'topics':topics})

def activitiesPage(request):
    room_messages = Message.objects.all()
    return render(request,'base/activity.html', {'room_messages':room_messages})


def load(request):
    fh = open('base/data.txt').readlines()

    for line in fh:
        row = line.split(',')
        username, email,password, firstname, lastname,cellphone, is_staff, is_superuser = [i.strip() for i in row]

        if User.objects.filter(email=email).first() is None:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                is_staff=eval(is_staff),
                is_superuser=eval(is_superuser),
            )
            print(f'{email} has beencreated')
        else:
            print(f'{email} already exists')
        
    return HttpResponse('Users Created')