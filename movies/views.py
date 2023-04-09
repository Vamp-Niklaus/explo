from django.shortcuts import render, redirect
from datetime import datetime
from movies.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models.signals import pre_save,post_save
import math
# Create your views here.

def index(request):
    context={
        'movie':Movie.objects.all().order_by("-m_id"),
        'cat':Cat_list.objects.all(),
        'lan':Lang_list.objects.all(),
        'year':range(2000,2023),
        'sort':['by rating','A-Z','Z-A','Newly Uploaded','Old Uploaded']
    }
    return render(request,'index.html',context)
    # return HttpResponse("this is homepage")

def contact(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name=request.user.first_name
            last_name=request.user.last_name
            email = request.user.email
            reason = request.POST['reason']
            at=datetime.today()
            number = request.POST['number']
            if Contact.objects.filter(customer=request.user.username).first() is None:
                if len(reason)<1:
                    messages.error(request, "Sorry you can't send empty message!!")
                    return redirect('home')
                elif len(number)<10:
                    messages.error(request, "Please Fill Complete Numbers!!")
                    return redirect('home')
                else:
                    Contact(c_id=request.user.id,customer=request.user.username,first_name=first_name,last_name=last_name,email=email,reason=reason,at=at,number=number).save()
                    messages.success(request, "Your message sent successfully!!")
                    return redirect('home')
            else:
                messages.error(request, "Sorry you can't send message again!!")
                return redirect('home')

        else:
            return render(request,'contact.html')
    else:
        messages.error(request, "You must be logged in for Contact Us!!")
        return redirect('home')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['dob']
        gender = request.POST['gender']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')

        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        Users(id=User.objects.get(username=username).id,birthday=dob,gender=gender,user_id=User.objects.get(username=username).id).save()
        messages.success(request, "Your Account has been created succesfully!!")
        messages.success(request, "Logged In Sucessfully!!")
        user = authenticate(username=username, password=pass1)
        login(request, user)
        return redirect('home')

    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out sucessfully!")
    return redirect('home')

def movie(request,m_id):
    actor_ids=Actor.objects.filter(m_id=m_id).values_list('actor_id',flat=True)
    actress_ids=Actress.objects.filter(m_id=m_id).values_list('actress_id',flat=True)
    director_ids=Director.objects.filter(m_id=m_id).values_list('director_id',flat=True)
    context={
             'movie':Movie.objects.get(m_id=m_id),
            'run':str(Movie.objects.get(m_id=m_id).run_time),
             'actor':Catalog.objects.filter(id__in =actor_ids),
             'actress':Catalog.objects.filter(id__in =actress_ids),
             'director':Catalog.objects.filter(id__in =director_ids),
             'users':Users.objects.all(),
             'cat':Cat_list.objects.all(),
            'lan':Lang_list.objects.all(),
            'year':range(2000,2023),
            'sort':['by rating','A-Z','Z-A','Newly Uploaded','Old Uploaded']
            }
    return render(request,'movie.html',context)
    # return HttpResponse("this is homepage")

def ratings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            rby=User.objects.get(username=request.user).id
            rby=Users.objects.get(user_id=rby).user_id
            ron= int(request.POST['ron'])
            rating= int(request.POST['star'])
            os=Views.objects.get(m_id=ron).sum
            oc=Views.objects.get(m_id=ron).count
            entries=Ratings.objects.values_list('rby','ron')
            
            if (rby,ron) in entries:
                old=Ratings.objects.get(ron=ron,rby=rby).rating
                Ratings.objects.filter(ron=ron,rby=rby).update(rating=rating)
                Views.objects.filter(m_id=ron).update(sum=(os+rating-old))
                messages.success(request, f"Your rating updated from  {str(old)}  to   {str(rating)}.")
            else:
                Ratings(ron,rby,rating=rating).save()
                Views.objects.filter(m_id=ron).update(sum=(os+rating))
                Views.objects.filter(m_id=ron).update(count=(oc+1))
                messages.success(request, f"Your rating {str(rating)} is saved.")

            ns=Views.objects.get(m_id=ron).sum
            nc=Views.objects.get(m_id=ron).count
            Movie.objects.filter(m_id=ron).update(rating=round((ns/nc),1))
            return redirect("movie",ron)
    else:
        messages.error(request, "You must be logged in for rating!!")
        return redirect('home',)

def search(request):
    target=request.GET['search']
    rm=Movie.objects.filter(m_name__icontains=target).first()
    if rm is None:
        messages.error(request,"Sorry! No Matches Found!")
        return redirect('home')
    else:
        context={
        'movie':Movie.objects.filter(m_name__icontains=target),
        'cat':Cat_list.objects.all(),
        'lan':Lang_list.objects.all(),
        'year':range(2000,2023),
        'sort':['by rating','A-Z','Z-A','Newly Uploaded','Old Uploaded']
        }
        return render(request,'index.html',context)

def category(request,rcat):
    rm=Categories.objects.filter(category=rcat).first()
    if rm is None:
        messages.error(request,"Sorry! No Matches Found!")
        return redirect('home')
    else:
        rid=Categories.objects.filter(category=rcat).values_list('m_id',flat=True)
        context={
        'movie':Movie.objects.filter(m_id__in =rid),
        'cat':Cat_list.objects.all(),
        'lan':Lang_list.objects.all(),
        'year':range(2000,2023),
        'sort':['by rating','A-Z','Z-A','Newly Uploaded','Old Uploaded']
        }
        return render(request,'index.html',context)

def language(request,rlang):
    rm=Languages.objects.filter(language=rlang).first()
    if rm is None:
        messages.error(request,"Sorry! No Matches Found!")
        return redirect('home')
    else:
        rid=Languages.objects.filter(language=rlang).values_list('m_id',flat=True)
        context={
        'movie':Movie.objects.filter(m_id__in =rid),
        'cat':Cat_list.objects.all(),
        'lan':Lang_list.objects.all(),
        'year':range(2000,2023),
        'sort':['by rating','A-Z','Z-A','Newly Uploaded','Old Uploaded']
        }
        return render(request,'index.html',context)

def year(request,year):
    rm=Movie.objects.filter(release_year=year).first()
    if rm is None:
        messages.error(request,"Sorry! No Matches Found!")
        return redirect('home')
    else:
        context={
        'movie':Movie.objects.filter(release_year=year),
        'cat':Cat_list.objects.all(),
        'lan':Lang_list.objects.all(),
        'year':range(2000,2023),
        'sort':['by rating','A-Z','Z-A','Newly Uploaded','Old Uploaded']
        }
        return render(request,'index.html',context)

def sort(request,sort):
    context={
        'cat':Cat_list.objects.all(),
        'lan':Lang_list.objects.all(),
        'year':range(2000,2023),
        'sort':['by rating','A-Z','Z-A','Newly Uploaded','Old Uploaded']
    }
    if sort=='by rating':
        context['movie']= Movie.objects.all().order_by("-rating")
    elif sort=='A-Z':
        context['movie']= Movie.objects.all().order_by("m_name")
    elif sort=='Z-A':
        context['movie']= Movie.objects.all().order_by("-m_name")
    elif sort=='Newly Uploaded':
        context['movie']= Movie.objects.all().order_by("-m_id")
    elif sort=='Old Uploaded':
        context['movie']= Movie.objects.all().order_by("m_id")

    return render(request,'index.html',context)


def movie_post_save(instance, **kwargs):
    view =Views(m_id=instance.m_id,sum=0,count=0)
    view.save()
pre_save.connect(movie_post_save,sender=Movie)