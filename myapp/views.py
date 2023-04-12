import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.core.mail import send_mail, BadHeaderError
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

from django.core import serializers


from .forms import CustomRegistrationForm, ArcticleForm, CommentForm, ProfileForm
from . import models


def index(request):
	return render(request, 'main/index.html')


class CustomRegistrationView(CreateView):
	form_class = CustomRegistrationForm
	success_url = reverse_lazy('index')
	template_name = 'main/registration.html'

class CustomLoginView(LoginView):
	template_name = 'main/login.html'
	success_url = reverse_lazy('index')

	def get_success_url(self):
		return self.success_url


class CustomLogoutView(LoginRequiredMixin, LogoutView):
	template_name = 'main/logout.html'
	next_page = reverse_lazy('index')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})


class HomeListView(ListView):
	model = models.Arcticle
	template_name = 'main/arcticles.html'
	context_object_name = 'list_arcticles'


class CustomSuccessMessageMixin:
	@property
	def success_msg(self):
		return False
		
	def form_valid(self,form):
		messages.success(self.request, self.success_msg)
		return super().form_valid(form)
	def get_success_url(self):
		return '%s?id=%s' % (self.success_url, self.object.id)


class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
	model = models.Arcticle
	template_name = 'main/detail.html'
	context_object_name = 'arcticle'
	form_class = CommentForm
	success_msg = 'Комментарий успешно создан, ожидайте модерации'
	
	
	def get_success_url(self):
		return reverse_lazy('detail', kwargs={'pk':self.get_object().id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['likes'] = models.Like.objects.filter(arcticle = self.object.pk )#user=self.request.user
		
		return context

	def post(self,request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)
	
	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.arcticle = self.get_object()
		self.object.author = self.request.user
		self.object.save()
		return super().form_valid(form)




class ArcticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
	model = models.Arcticle
	template_name = 'main/edit_page.html'
	form_class = ArcticleForm
	success_url = reverse_lazy('edit')
	success_msg = 'Запись создана'
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	
	def get_context_data(self, **kwargs):
		kwargs['list_arcticles'] = models.Arcticle.objects.all().order_by('id') 
		return super().get_context_data(**kwargs)
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.author = self.request.user
		self.object.save()
		return super().form_valid(form)



class ArcticleCreatePage(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
	model = models.Arcticle
	template_name = 'main/create_arcticle.html'
	form_class = ArcticleForm
	success_url = reverse_lazy('edit')
	success_msg = 'Запись создана'
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	
	def get_context_data(self, **kwargs):
		kwargs['list_arcticles'] = models.Arcticle.objects.all().order_by('id') 
		return super().get_context_data(**kwargs)
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.author = self.request.user
		self.object.save()
		return super().form_valid(form)





	
class ArcticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin,UpdateView):
	model = models.Arcticle
	template_name = 'main/edit_page.html'
	form_class = ArcticleForm
	success_url = reverse_lazy('edit')
	success_msg = 'Запись обновлена'
	def get_context_data(self, **kwargs):
		kwargs['update_text'] = True
		return super().get_context_data(**kwargs)
	
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		if self.request.user != kwargs['instance'].author:
			return self.handle_no_permission()

		return kwargs
	



class ArcticleDeleteView(LoginRequiredMixin, DeleteView):
	model = models.Arcticle
	template_name = 'main/edit_page.html'
	success_url = reverse_lazy('edit')
	success_msg = 'Запись удалена'
	
	def post(self,request,*args,**kwargs):
		messages.success(self.request, self.success_msg)
		return super().post(request)
	
	
	def form_valid(self, form):
		self.object = self.get_object()
		print(self.object.author)
		if self.request.user != self.object.author:
			return self.handle_no_permission()
		success_url = self.get_success_url()
		self.object.delete()
		return HttpResponseRedirect(success_url)

		response = super().form_valid(form)

		return response
	


class ShowProfilePageView(LoginRequiredMixin,DetailView):
	model = models.Profile
	template_name = 'main/user_profile.html'
	login_url = '/login/'

	
	def get_object(self):
		queryset = super().get_queryset()
		return queryset.get(user_id=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page_user = self.object.user
		user = self.object.user_id
		arcticles_len = models.Arcticle.objects.filter(author_id=user)
		user_likes = models.Like.objects.filter(user_id=user)
		arcticles_user = models.Arcticle.objects.filter(author_id=user)

		context['page_user'] = page_user
		context['arcticle_count'] = arcticles_len.count() # sdnfhbsdfbsdhfbsd
		context['user_likes'] = user_likes.count()
		context['arcticle_list'] = arcticles_user
		return context
	

	# def get(self, request, *args, **kwargs):
	# 	user = request.user
	# 	if not models.Profile.objects.filter(user=user):
	# 		return redirect('create_user_profile')
	# 	return super().get(request, *args, **kwargs)


	# def get_context_data(self, *args, **kwargs):
	# 	context = super().get_context_data(*args, **kwargs)
	# 	page_user = get_object_or_404(models.Profile, id=self.kwargs['pk'])
	# 	user = self.object.id
	# 	arcticles_len = models.Arcticle.objects.filter(author_id=user)
	# 	user_likes = models.Like.objects.filter(user_id = user)
	# 	arcticles_user = models.Arcticle.objects.filter(author_id = user)

	# 	context['page_user'] = page_user	
	# 	context['arcticle_count'] = arcticles_len.count()
	# 	context['user_likes'] = user_likes.count()
	# 	context['arcticle_list'] = arcticles_user
	# 	return context



class CreateProfilePageView(CreateView):
	model = models.Profile
	
	template_name = 'main/create_profile.html'
	fields = ['profile_pic', 'bio', 'facebook', 'twitter', 'instagram']
	def form_valid(self, form):
		status = models.Profile.objects.values_list('status')
		status = True
		form.instance.user = self.request.user
		return super().form_valid(form)

	success_url = reverse_lazy('index')


class EditProfilePageView(UpdateView):
	model = models.Profile
	template_name = 'main/edit_profile_page.html'
	form_class=ProfileForm
	
	success_url = reverse_lazy('index')
	


@login_required
def like_arcticle(request):
	print('aaaaaaaaaaaaaaaa')
	if request.method == 'POST':
		print('fffffffffff')
		if request.POST.get("operation") == "like_submit":
			print('ggggggggggggggg')
			arcticle_id = request.POST.get('arcticle_id')
			print('ID', arcticle_id)
			arcticle = get_object_or_404(models.Arcticle, id=arcticle_id)
			user = request.user
			likes = models.Like.objects.filter(user_id=user, arcticle_id=arcticle_id) #get_object_or_404(models.Like, pk=arcticle_id)
			print('query',likes)
			if likes.filter(user_id=request.user.id).exists():
				print('DISLIKE')
				likes.delete()
				like_status = False
			else:
				print('LIKED')
				models.Like.objects.create(user=user, arcticle=arcticle)
				like_status = True
			

			user_likes = models.Like.objects.filter(arcticle_id = arcticle_id).count()
			print("DDDDDDDD", type(user_likes))

			context = {'status': like_status, 'arcticle_id': arcticle_id, 'user_likes': user_likes}
			print('CONTEXT', type(context['status']))
			return JsonResponse(json.dumps(context), content_type='application/json', safe=False)
	
	print('CHECK')
	contents = models.Like.objects.all()
	already_liked = []
	id = request.user.id
	for content in contents:
		if(content.user.filter(user_id=id).exists()):
			already_liked.append(content.user_id)
	print('4444444444444444444444',already_liked)
	ctx = {'contents':contents, 'already_liked':already_liked}
	print('CHEKC@@@@@@')
	return render(request, 'like_arcticle', ctx)





		# if request.user.is_authenticated:
		# 	arcticle.likes.add(request.user)
		# 	arcticle.save()
		# 	return JsonResponse({'status': 'ok', 'likes_count': arcticle.likes.count()})
		# else:
		# 	return JsonResponse({'status': 'error', 'message': 'User not authenticated.'})


def unlike_arcticle(request):
	if request.method == 'POST':
		arcticle_id = request.POST.get('arcticle_id')
		arcticle = get_object_or_404(models.Arcticle, id=arcticle_id)
		if request.user.is_authenticated:
			arcticle.likes.remove(request.user)
			arcticle.save()
			return JsonResponse({'status': 'ok', 'likes_count': arcticle.likes.count()})
		else:
			return JsonResponse({'status': 'error', 'message': 'User not authenticated.'})




# def like_arcticle(request):
#     print('sdfkogjiosdfgioshdefgsdfgsdfgdsfgsgfd')
#     arcticle_id = request.POST.get('arcticle_id')
#     arcticle = get_object_or_404(models.Arcticle, id=arcticle_id)
#     user = request.user
#     like = models.Like.objects.filter(user=user, arcticle=arcticle)
#     if like.exists():
#         like.delete()
#         liked = False
#     else:
#         models.Like.objects.create(user=user, arcticle=arcticle)
#         liked = True
#     context = {'liked': liked, 'count': arcticle.likes.count()}
#     return JsonResponse(context)
