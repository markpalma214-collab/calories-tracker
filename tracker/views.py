from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .forms import CaloriesForm
from .models import CaloriesTracker, Category
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    foods = CaloriesTracker.objects.filter(
        Q(food__icontains=q)|
        Q(category__category__icontains=q)
    )
    category = Category.objects.all()

    context = {
        'Category':category,
        'foods':  foods,

    }

    return render(request, 'website/home.html', context)

@login_required(login_url='authentication')
def tracker(request):
    form = CaloriesForm()

    if request.method == "POST":
        form = CaloriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("view")

    context = {
        "form": form,
    }

    return render(request, "website/caloriestracker.html", context)

@login_required(login_url='authentication')
def trackerview(request):
    q = request.GET.get("q", "")

    calories = CaloriesTracker.objects.filter(
        food__icontains=q
    )

    context = {
        "calories": calories,
    }

    return render(request, "website/caloriesview.html", context)

@login_required(login_url='authentication')
def summary_hard(request):
    foods = CaloriesTracker.objects.all()
    category = Category.objects.all()
    total_calories = 0
    total_protein = 0
    total_fiber = 0
    total_carb = 0
    total_quantity = 0
    for food in foods:
        total_calories += food.calories * food.quantity
        total_protein += food.protein * food.quantity
        total_fiber += food.fiber * food.quantity
        total_carb += food.carb * food.quantity
        total_quantity += food.quantity
    goal = 1700
    reached_goal = total_calories>=goal


    context = {
        "foods":foods,
        "calories":total_calories,
        "protein":total_protein,
        "carb":total_carb,
        "quantity":total_quantity,
        "fiber":total_fiber,
        "category":category,
        "reached_goal":reached_goal,

    }
    
    
    # quantity means each nutrition labels should be doubled given its amount.

    return render(request, "website/summary.html", context)


@login_required(login_url='authentication')
def history(request):
    # check the history for yesterday, the other day,
    calendar_date = request.GET.get("calendar")
    if calendar_date:
        foods = CaloriesTracker.objects.filter(date=calendar_date)
        history = calendar_date
    else:
        history = timezone.localdate()
        foods = CaloriesTracker.objects.filter(date=history)
    context = {
        "history":history,
        "foods":foods,
    }
    return render(request, "website/history.html", context)


    

@login_required(login_url='authentication')
def summary_easy(request):
    today = timezone.localdate()
    days = CaloriesTracker.objects.filter(date = today)


    summary = days.aggregate(
        calories = Sum("calories"),
        protein = Sum("protein"),
        fiber = Sum("fiber"),
        carb = Sum("carb"),
        quantity = Sum("quantity"),
    )

    goal = 1700
    reached_goal = summary["calories"] >= goal
    context = {
        "foods":summary,
        "goal":goal,
        "reached_goal": reached_goal,
    }
    
    return render(request, 'website/summary.html', context)

def update_form(request, pk):
    calories = get_object_or_404(CaloriesTracker, id=pk)
    form = CaloriesForm(instance=calories)
    if request.method == "POST":
        form = CaloriesForm(request.POST, instance=calories)
        if form.is_valid():
            form.save()
            return redirect('view')
    context = {
        "form":form
    }
    return render(request, 'website/caloriestracker.html', context)

@login_required(login_url='authentication')
def delete(request, pk):
    calories = CaloriesTracker.objects.get(id=pk)
    if request.method == "POST":
        calories.delete()
        return redirect("view")
    return render(request,
                'website/delete.html',
                  {'obj':calories},
                  )

def authentication(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'username or password does not exist.')


        

        

    return render(request, "website/authentication.html")

def logoutuser(request):
    logout(request)
    return redirect('home')
