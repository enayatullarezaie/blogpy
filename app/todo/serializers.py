from rest_framework import serializers
from .models import Todo
from django.contrib.auth import get_user_model



class TodoSerializer(serializers.ModelSerializer):

   def validate_priority(self, priority):
      if priority > 20 or priority < 1 :
         raise serializers.ValidationError('priority is not ok')
      return priority
   
   # def validate(self, attrs):
   #    print(attrs)
   #    return super().validate(attrs)

   class Meta:
      model= Todo
      fields = '__all__'



User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model= User
      fields = '__all__'

   todos = TodoSerializer(read_only=True, many= True)


