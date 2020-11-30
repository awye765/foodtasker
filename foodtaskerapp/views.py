from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from foodtaskerapp.forms import UserForm, RestaurantForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create you views here.
def home(request):
    return redirect(restaurant_home)

@login_required(login_url='/restaurant/sign-in/')
def restaurant_home(request):
    return render(request, 'restaurant/home.html', {})

def restaurant_sign_up(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()

    # When user hits Sign Up button, run below code
    if request.method == "POST":
        # Get data from the forms for each new user and restaurant
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        # If data valid
        if user_form.is_valid() and restaurant_form.is_valid():
            # Create new user object for restaurant owner
            new_user = User.objects.create_user(**user_form.cleaned_data)
            # Create new restaurant, but don't commit to db. Hold in mem only
            new_restaurant = restaurant_form.save(commit=False)
            # Set user of that restaurant to the new user
            new_restaurant.user = new_user
            # Now save restaurant to db
            new_restaurant.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(restaurant_home)

    return render(request, 'restaurant/sign_up.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })