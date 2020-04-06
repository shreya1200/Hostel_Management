# from msilib.schema import ListView
from django.http import HttpResponseBadRequest
from django.shortcuts import render, Http404, redirect, reverse
import django.http
from .models import Banner, SignUp, Leave, Complaint
from django.contrib.auth.models import User, auth, AnonymousUser
from django.contrib import messages
from django.urls import NoReverseMatch
from django.views.generic import ListView


# Create your views here.

def homepage(request):
    try:
        if not request.user.is_anonymous:
            profile = SignUp.objects.get(user=request.user)
            return render(request, 'index.html', {'home': homepage, 'profile': profile})  # used in .html  as jinja
        else:
            return render(request, 'index.html', {'home': homepage})
    except SignUp.DoesNotExist:  # used in .html  as jinja
        return render(request, 'index.html', {'home': homepage})


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        prn = request.POST['prn']
        st_number = request.POST['st_number']
        parent_number = request.POST['parent_number']
        branch = request.POST['branch']
        username = request.POST['username']
        password = request.POST['password']

        # su.student_name = student_name
        # su.email = email
        # su.prn = prn
        # su.st_number = st_number
        # su.parent_number = parent_number
        # su.branch = branch
        # su.username = username
        # su.password = password
        user = User.objects.create_user(username=username, password=password, first_name=name,
                                        email=email)
        user.save()
        su = SignUp(name=name, email=email, prn=prn, st_number=st_number, parent_number=parent_number,
                    branch=branch, user=user, username=username, password=password)
        su.page = 'hostel:home'
        su.save()

        print('user created')
        return redirect('hostel:home')
    else:
        return render(request, 'Signup.html', {'signup': signup})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:

            # correct username and password login the user
            if user.is_staff:
                auth.login(request,user)
                return redirect('/')
            elif not user.is_staff:
                auth.login(request, user)
                # to segragate users using foreignkey
                profile = SignUp.objects.get(user=request.user)
                profile.save()
                print(request.user)
            # for i in User.objects.all():
            #     print(i.pk)
                return redirect('/')
        else:
            messages.error(request, 'Invalid username/password')  # specified in jinja {{message}}
            return redirect('/login')
    else:
        return render(request, 'indexlogin.html', {'login': login})


def logout(request):
    auth.logout(request)
    return redirect('/')
    # if request.method != 'POST':
    #     raise Http404('Only POSTs are allowed')
    # try:
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = auth.authenticate(username=username, password=password)
    #     if user is not None:
    #         request.session['user_id'] = user.id
    #         return HttpResponseRedirect('/you-are-logged-in/')
    # except user.DoesNotExist:
    #     return HttpResponse("Your username and password didn't match.")
    # global s
    # # ban = Banner()
    # # ban.status = "Login"
    # # return render(request,'indexlogin.html',{'login' :login})
    # # print({{ban.status}})
    # if s == "Login":
    #     # return render(request,'indexlogin.html',{'login' :login})
    #     if request.method == 'POST':
    #         username = request.POST['username']
    #         password = request.POST['password']
    #         print(username, password, "Outsdoe IF")
    #         user = auth.authenticate(username=username, password=password)
    #         print(username, password, "Outside IF")
    #         # auth.login(request,user)
    #         # messages.info(request,'congo..!!')
    #         # return HttpResponse("Hello {{username}}")
    #         if user is not None:
    #             print(username, password, "In")
    #             auth.login(request, user)
    #             s = "Logout"
    #             # status = ban.status
    #             # messages.info(request,'congo..!!')
    #             return render(request, 'index.html', {'s': s})
    #         else:
    #             messages.error(request, 'Invalid Credentials')
    #             return redirect('hostel:login')
    #     else:
    #         return render(request, 'indexlogin.html', {'login': login})
    # elif s == "Logout":
    #     auth.logout(request)
    #     s = "Login"
    #     return render(request, 'index.html', {'s': s})


# def homepage(request):
# return render(request,'index.html',{'name' : 'HOME'})
# def logout(request):
#     auth.logout()
#     return redirect('/')
# return render(request, 'logout.html', {'logout': logout})
# try:
#     del request.session['user_id']
# except KeyError:
#     pass
# return HttpResponse("You're logged out.")


def facility(request):
    return render(request, 'facility.html', {'facility': facility})


def leave(request):
    profile = SignUp.objects.get(user=request.user)
    if request.method == 'POST':

        name = request.POST['name']
        reason = request.POST['reason']
        text = request.POST['text']  # parent consent type (letter/email/fax)
        depdate = request.POST['depdate']
        deptime = request.POST['deptime']
        arrdate = request.POST['arrdate']
        arrtime = request.POST['arrtime']
        parent_number = request.POST['parent_number']

        # context = {
        #     # "Name": name,
        #     "Reason": reason,
        #     "Parent_consent_type": text,
        #     "Departure_date": depdate,
        #     "Departure_time":deptime,
        #     "Arrival_date":arrdate,
        #     "Arrival_time":arrtime,
        #     "Parent_contact":parent_number,
        # }

        lea = Leave(profile=profile, name=name, reason=reason, text=text, depdate=depdate, deptime=deptime,
                    arrdate=arrdate, arrtime=arrtime,
                    parent_number=parent_number)
        # lea.profile = SignUp.objects.get(user=request.user)
        lea.save()
        return redirect(reverse('/'))

        # template_name = "leavedetails.html"
        # return render(request, template_name, context)


    else:
        profile.page = 'leave'
        profile.save()
        return render(request, 'leave.html', {'leave': leave})


def complaint(request):
    profile = SignUp.objects.get(user=request.user)
    if request.method == 'POST':

        name = request.POST['name']
        st_number = request.POST['number']
        category = request.POST['complaint']
        problem = request.POST['problem']
        room = request.POST['room']
        user_type = request.POST['user_type']

        comp = Complaint(profile=profile, name=name, st_number=st_number, category=category, problem=problem, room=room,
                         user_type=user_type)
        comp.save()
        return redirect('/')
    else:
        profile.page = 'complaint'
        profile.save()
        return render(request, 'complaint.html', {'complaint': complaint})



def ApproveLeave(request):
    user = request.user
    if user.is_staff:
        leaves = Leave.objects.all()
        profile = SignUp.objects.get(user=user)

        # return HttpResponseBadRequest("Bad Request")
        return render(request, 'approveleave.html', {'profile': profile})
        # return render(request, 'approveleave.html', {'approveleave': ApproveLeave})
    # model = Leave #model is a necessary parameter which needs to be included to specify which class are we working on
    # template_name = 'approveleave.html' #
    #
    # def get_queryset(self):  #self is same as 'this' keyword
    #     return Leave.objects.all()


def leavedetails(request, pk):
    leave = Leave.objects.get(pk=pk)
    if request.method == 'POST':
        approve = request.POST['approved']
        if approve == "1":
            user_profile = SignUp.objects.get(id=leave.profile_id)
            return redirect('hostel:home')
        else:
            return render(request, 'leavedetails.html', {'leave': leave})
    # for i in SignUp.objects.all():
    #     print(i.pk)
    # student_info = Leave.objects.get(pk=pk)
    # context = {'student_info': student_info}
    # return render(request, 'leavedetails.html', context)
