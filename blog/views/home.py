from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.utils import timezone
from blog.models import post, comment, User, UserProfile
from blog.forms import SignupForm
from django.contrib.auth.decorators import login_required
import hashlib, datetime, random

def main_page(request):
	if 'user_id' in request.session:
		user_obj = User.objects.get(id=request.session['user_id'])
		blog_obj = post.objects.filter(user_id=request.session['user_id'])
		context = {'user':user_obj,'blogs':blog_obj}
		return render(request, 'home.html', context)
	else:
		form = SignupForm()
		return render(request, 'index.html', {'form': form})

def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		print(form.data)
		print(form.is_valid())
		if form.is_valid():
			form.save()

			username = form.data['username']
			email = form.data['email']
			print(username,email)
			salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
			activation_key = hashlib.sha1((salt+email).encode('utf-8')).hexdigest()
			key_expires = datetime.datetime.today() + datetime.timedelta(1)

			# Create and save user profile
			user = User.objects.get(email=email)
			new_profile = UserProfile(user=user, activation_key=activation_key,
				key_expires=key_expires)
			new_profile.save()

			# Send email with activation key
			email_subject = 'Account confirmation'
			email_body = "Hi %s, thanks for signing up. To activate your account, click this link within \
			48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)
			send_mail(email_subject, email_body, 'mytestingapp000@gmail.com',
				[email], fail_silently = False)
			return render(request, 'sign_up_success.html')
		else:
			return render(request, 'confirm_expired.html')
	else:
		return render(request, 'sign_up.html')

def signup_confirm(request, activation_key):
	if 'user_id' in request.session:
		return redirect('index')
	user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
	if user_profile.key_expires < timezone.now():
		return render(request,'confirm_expired.html')
	user = user_profile.user
	user.is_active = True
	user.save()
	request.session['user_id'] = user.id
	return redirect('index')

def login(request):
	if request.method == 'POST':
		user_email = request.POST.get('email')
		user_password = request.POST.get('password')
		user_obj = User.objects.filter(email=user_email, password=user_password)
		if user_obj.count() == 1 and user_obj[0].is_active:
			request.session['user_id'] = user_obj[0].id
			request.session['first_name'] = user_obj[0].first_name
	return redirect('index')

def logout(request):
	if 'user_id' in request.session:
		del request.session['user_id']
		del request.session['first_name']
		request.session.modified=True
	return redirect('index')

def setting(request):
	if request.method == 'POST':
		blog = User.objects.filter(id=request.session['user_id']).update(first_name=request.POST.get('first_name'),
			lname=request.POST.get('last_name'), password=request.POST.get('password'))
		return redirect('index')
	else:
		if 'user_id' in request.session:
			user = User.objects.get(id=request.session['user_id'])
			context = {'user': user}
			return render(request, 'setting.html', context)
		else:
			return redirect('index')