from django import forms
from .models import Farmer, Student


class FarmerForm(forms.ModelForm):
	"""ModelForm for the existing Farmer model. Useful when you want to
	create/edit Farmer instances from a view.
	"""

	class Meta:
		model = Farmer
		fields = ["name", "farm", "age", "address", "phone_number", "email"]
		widgets = {"address": forms.Textarea(attrs={"rows": 2})}


class StudentModelForm(forms.ModelForm):
	"""ModelForm for the Student model."""

	class Meta:
		model = Student
		fields = ["name", "age", "address", "phone_number", "email", "school", "notes"]
		widgets = {"address": forms.Textarea(attrs={"rows": 2}), "notes": forms.Textarea(attrs={"rows": 3})}

