from django.shortcuts import render, redirect
from blog.models import post, comment, User
from django.contrib.auth.decorators import login_required

def new_blog(request):
	if request.method == 'POST':
		print (request.POST.get('title'))
		blog = post(title=request.POST.get('title'), 
			body=request.POST.get('body'), 
			user_id=request.session['user_id']
			)
		blog.save()
		return redirect('index')
	else:
		if 'user_id' in request.session:
			first_name = request.session['first_name']
			return render(request, 'new_blog.html', {'first_name': first_name})
		else:
			return redirect('index')


def edit_blog(request, blog_id):
	if request.method == 'POST':
		blog = post.objects.filter(id=blog_id).update(title=request.POST.get('title'),
			body=request.POST.get('body'))
		return redirect('index')
	else:
		if 'user_id' in request.session:
			blog = post.objects.get(id=blog_id)
			first_name = request.session['first_name']
			context = {'first_name':first_name, 'blog': blog}
			return render(request, 'edit_blog.html', context)
		else:
			return redirect('index')

def delete_blog(request, blog_id):
	post.objects.get(id=blog_id).delete()
	return redirect('index')