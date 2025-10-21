from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import StudentModelForm


def student_create_view(request):
	"""Render and process the StudentModelForm to create Student instances."""
	if request.method == "POST":
		form = StudentModelForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse("attendance:student_success"))
	else:
		form = StudentModelForm()

	return render(request, "attendance/student_form.html", {"form": form})


def student_success_view(request):
	return render(request, "attendance/student_success.html")


def student_list_view(request):
	"""Display a list of students."""
	from .models import Student

	students = Student.objects.all().order_by("name")
	return render(request, "attendance/student_list.html", {"students": students})


def farmer_create_view(request):
	"""Render and process a Farmer ModelForm to create Farmer instances."""
	from .forms import FarmerForm

	if request.method == "POST":
		form = FarmerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse("attendance:farmer_success"))
	else:
		form = FarmerForm()

	return render(request, "attendance/farmer_form.html", {"form": form})


def farmer_success_view(request):
	return render(request, "attendance/farmer_success.html")


def farmer_list_view(request):
	from .models import Farmer

	farmers = Farmer.objects.all().order_by("name")
	return render(request, "attendance/farmer_list.html", {"farmers": farmers})
