from django.forms import ModelForm, ValidationError
from blog.models import User

class SignupForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

	# Clean used email
	# def clean_email(self):
	# 	email = self.data['email']
	# 	try:
	# 		User._default_manager.get(email=email)
	# 	except User.DoesNotExist:
	# 		return email
	# 	raise ValidationError('Email is already been used.')
	# 

	# Save user with inactive status
	def save(self):
		user = super(ModelForm, self).save(commit=False)
		user.is_active = False
		user.save()
		return user