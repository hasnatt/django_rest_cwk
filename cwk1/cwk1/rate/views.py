# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from _decimal import ROUND_HALF_UP, Decimal
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
import json


# Create your views here.

# list
def getAllModules(request):
    """
    for the 'list' function shown in option 1, this function retrieves all data from
    querying the existing modules instances and returns a JSON for the client.
    """
    x = []
    body = ModuleState.objects.all()
    for i in body:
        professors = []
        for j in i.professors.all():
            professors.append(j.code + " " + j.name)
        mod = i.module

        d = {
            "module id": mod.code,
            "module": mod.name,
            "year": i.year,
            "semester": i.semester,
            "professors": professors,
            # "profcode":
        }
        x.append(d)
    return JsonResponse(x, safe=False)

# view
f


def profaverage(request):
    """
    the 'average' function for option 3 requires an input of a professor and a module, this is done my taking
    an get request from the user. this is then queried to the Module and professor model where we can find the ratings
    for a given professor. This returns a JSON string for the client

    """
    professor = request.GET.get('professor')
    module = request.GET.get('module')

    check = check_user([professor, module])

    if check == False:
        return HttpResponse("missing data", status=400)
    try:
        professor = Professor.objects.get(code=professor)
        module = Module.objects.get(code=module)
    except:
        return HttpResponse("Data doesnt exist", status=500)

    ratings = ProfessorRating.objects.all().filter(professor=professor)

    ratinglist = []

    for rate in ratings:
        if rate.module_state.module.code == module.code:
            ratinglist.append(rate.rating)

    if len(ratinglist) == 0:
        return HttpResponse("No ratings found, incomplete information", status=206)

    avg = sum(ratinglist) / len(ratinglist)
    average = float(Decimal(avg).quantize(0, ROUND_HALF_UP))

    dict = {

        'professor': professor.name,
        'professorcode': professor.code,
        'module': module.name,
        'code': module.code,
        'rating': average,
    }

    return JsonResponse(dict, safe=False)


@csrf_exempt
def rateprofessor(request):
    """
    for the 'rate' function we take in 5 arguemtns form the client and store that in to the ProffesorRating
    database.
    """
    professor_id = request.POST.get('professor_id', None)
    module_code = request.POST.get('module_code', None)
    year = request.POST.get('year', None)
    semester = request.POST.get('semester', None)
    rating = request.POST.get('rating', None)

    # professor_id = "JE1"
    # module_code = "CD1"
    # year = 2017
    # semester = 1
    # rating = 3

    check = check_user([professor_id, module_code, year, semester, rating])

    if request.user.is_authenticated:

        if check == False:
            return HttpResponse("Empty parameters have been provided", status=400)

        try:
            module = Module.objects.get(code=module_code)
            professor = Professor.objects.get(code=professor_id)
            modulestate = ModuleState.objects.get(professors=professor, module=module, semester=semester, year=year)

            print(module.code)
            print(professor)
            print(modulestate)

            newrating = ProfessorRating(professor=professor, rating=rating, module_state=modulestate,
                                        user=request.user)
            newrating.save()
        except:
            return HttpResponse("Rating Failed", status=400)
        return HttpResponse("Rating successful", status=200)

    else:
        return HttpResponse("User isnt logged in", status=400)


@csrf_exempt
def register(request):
    """
    for the 'register' function the function gets 3 values from the client which are username, password
    and email. this functions uses djangos built in user system

    """
    username = request.POST.get('username', None)
    email = request.POST.get('password', None)
    password = request.POST.get('email', None)

    check = check_user([username, email, password])
    if check == False:
        return HttpResponse("Please provide parameters", status=400)
    try:
        newuser = User.objects.create_user(username=username,
                                           email=email,
                                           password=password)
        newuser.save()
    except:
        return HttpResponse("Registration Failed", status=500)

    return HttpResponse("Registering successful", status=200)


@csrf_exempt
def loginuser(request):
    """
    Thos function is for the  'login' function which takes a username and password and checks
    it exists in the database
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    checkuser = check_user([username, password])
    if not checkuser:
        return HttpResponse("Try Again", status=400)
    x = authenticate(username=username, password=password)
    if x is not None:
        login(request, x)
        return HttpResponse("You are now logged in", status=200)
    else:
        return HttpResponse("Log in attempt unsuccessful", status=401)


def check_user(params):
    """
    A simple function to check if the parameters passed are valid. if theyre empty we return a false boolean
    """
    for param in params:
        if (len(param) == 0):
            return False
        return True


def logoutuser(request):
    """
    for the 'logout' function we are utilising djangos logout() function to log a user out

    """
    try:
        logout(request)
    except:
        return HttpResponse("Logout Unsuccesfull", status=401)
    return HttpResponse("Logout Succesfull", status=200)
