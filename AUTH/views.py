
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

User = get_user_model()


@login_required
def landing_page(request):
    print("called")
    user = request.user
    if user.is_authenticated:
        username = user.username
    else:
        username = 'Guest'
    return render(request, 'authTemplates/index.html', {
        "username": username
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'authTemplates/signup.html', {
                'message': "passwords do not match!!"
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'authTemplates/signup.html', {
                'message': "email already exists"
            })

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
        )

        return HttpResponse('Check your email to verify your account.')

    return render(request, 'authTemplates/signup.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('home')
            else:
                return redirect('home')
        return HttpResponse('Invalid credentials.')
    return render(request, 'authTemplates/signin.html')


def password_reset_link(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = request.build_absolute_uri(
                f'/auth/reset-password/{uid}/{token}/')

            send_mail(
                'Reset your password',
                f'Click the link to reset your password: {verification_link}',
                'noreply@myproject.com',
                [email],
                fail_silently=False,
            )

            return render(request, 'authTemplates/reset_password.html', {
                'message': "Password reset link sent to your email"
            })
        except User.DoesNotExist:
            return render(request, 'authTemplates/reset_password.html', {
                'message': "User with this email does not exist"
            })
    else:
        return render(request, 'authTemplates/reset_password.html', {
            'message': "Something went wrong, try again..."
        })


def password_reset_link_check(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')

        if not email or not new_password:
            return render(request, 'authTemplates/set_new_password.html', {
                'message': "Email and password are required.",
                'email': email
            })

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return render(request, 'authTemplates/set_new_password.html', {
                'message': "Password reset successful! Please sign in."
            })
        except User.DoesNotExist:
            return render(request, 'authTemplates/set_new_password.html', {
                'message': "User with this email does not exist.",
                'email': email
            })
    else:
        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'authTemplates/set_new_password.html', {
                'email': user.email
            })
        else:
            return render(request, 'authTemplates/set_new_password.html', {
                'message': "Something went wrong, try again..."
            })


def logout_view(request):
    logout(request)
    return redirect('signin')


def root_url(request):
    return redirect('signin')
