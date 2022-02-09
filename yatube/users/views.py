from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from .forms import CreationForm
from django.contrib import messages



# class SignUp(CreateView):
#     form_class = CreationForm
#
#     success_url = reverse_lazy("login")
#     template_name = "signup.html"

def register(request):
    if request.method == "POST":
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегестрировались")
            return redirect("index")
        else:
            messages.error(request, "Ошибка регистрации")
    else:
        form = CreationForm()
    return render(request, "signup.html", {"form": form})


