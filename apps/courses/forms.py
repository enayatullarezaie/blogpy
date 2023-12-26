from .models import *
from django import forms




class CourseForm(forms.ModelForm):
   class Meta:
      model = Course
      fields = ("title", "description", "cover")