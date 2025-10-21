from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .forms import StudentModelForm, FarmerForm


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


def farmer_update_view(request, pk):
    """Render and process a Farmer ModelForm to update Farmer instances."""
    from .forms import FarmerForm
    from .models import Farmer

    farmer = get_object_or_404(Farmer, pk=pk)

    if request.method == "POST":
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            return redirect(reverse("attendance:farmer_list"))
    else:
        form = FarmerForm(instance=farmer)

    return render(request, "attendance/farmer_form.html", {"form": form, "update": True})


def mark_attendance_view(request):
	"""Handle attendance marking for farmers."""
	from .models import Farmer, Attendance
	from django.utils import timezone
	from django.contrib import messages
	
	if request.method == "POST":
		# Get today's date
		today = timezone.now().date()
		
		# Get the list of farmer IDs who are present
		present_farmer_ids = request.POST.getlist('attendance')
		
		# Get all farmers
		all_farmers = Farmer.objects.all()
		
		# Mark attendance for all farmers
		for farmer in all_farmers:
			is_present = str(farmer.id) in present_farmer_ids
			
			# Get or create attendance record for today
			attendance, created = Attendance.objects.get_or_create(
				farmer=farmer,
				date=today,
				defaults={'is_present': is_present}
			)
			
			# Update if already exists
			if not created:
				attendance.is_present = is_present
				attendance.save()
		
		# Add success message
		messages.success(request, f"Attendance saved successfully for {today}")
		return redirect(reverse("attendance:farmer_list"))
	
	return redirect(reverse("attendance:farmer_list"))


def attendance_list_view(request):
	"""Display attendance records."""
	from .models import Attendance
	from django.utils import timezone
	from datetime import timedelta
	
	# Get date filter from query params (default to last 30 days)
	days_back = int(request.GET.get('days', 30))
	start_date = timezone.now().date() - timedelta(days=days_back)
	
	# Get attendance records ordered by date (newest first)
	attendances = Attendance.objects.filter(
		date__gte=start_date
	).select_related('farmer').order_by('-date', 'farmer__name')
	
	# Group by date for better display
	attendance_by_date = {}
	for attendance in attendances:
		date_str = attendance.date
		if date_str not in attendance_by_date:
			attendance_by_date[date_str] = []
		attendance_by_date[date_str].append(attendance)
	
	context = {
		'attendance_by_date': attendance_by_date,
		'days_back': days_back,
		'start_date': start_date,
	}
	
	return render(request, "attendance/attendance_list.html", context)


def farmers_json_api(request):
	"""Return farmers data as JSON."""
	from .models import Farmer
	
	farmers = Farmer.objects.all().order_by("name")
	
	farmers_data = []
	for farmer in farmers:
		farmer_dict = {
			'id': farmer.id,
			'name': farmer.name,
			'farm': farmer.farm,
			'age': farmer.age,
			'address': farmer.address,
			'phone_number': farmer.phone_number,
			'email': farmer.email,
			'gender': farmer.get_gender_display(),  # Gets the human-readable version
			'gender_code': farmer.gender,  # Gets the code (M, F, O)
			'worker_type': farmer.get_worker_type_display(),  # Gets the human-readable version
			'worker_type_code': farmer.worker_type,  # Gets the code (casual, contract)
		}
		farmers_data.append(farmer_dict)
	
	return JsonResponse({
		'farmers': farmers_data,
		'count': len(farmers_data),
		'status': 'success'
	})