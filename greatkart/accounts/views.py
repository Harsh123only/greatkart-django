from django.shortcuts import render
from  .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# from djnago. import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as account_activation_token


# Create your views here.


def register(request):
    if request.method=="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phon_number = form.cleaned_data['phon_number']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            username = email.split('@')[0]

            user=Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            user.phon_number = phon_number
            user.save()
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_activation_email.html' ,{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, "Thankyou for Registration ! Please check your email to activate your account.")
            return redirect('accounts/login/?command=verification&email='+email)
    else:       
        form = RegistrationForm()
    context={
        'form': form
    }
    return render(request, 'accounts/register.html',context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user=auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            print('eroor')
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You are now logged out")
    return redirect('login')
    return render(request, 'accounts/logout.html')



def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, "Your account has been activated")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('register')
    

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html')
    # else:
    #     messages.error(request, "You are not logged in")
    #     return redirect('login')
    
    # return HttpResponse("This is dashboardashboard'



def forgotPassword(request):
    if request.method == "POST":
        email= request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html' ,{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist! ")
            return redirect('forgotpassword')
        
    return render(request, 'accounts/forgotPassword.html')

def reset_password_validation(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None    
    if user is not None and account_activation_token.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return redirect('resetpassword')
    else:
        messages.error(request, "This link has expired")
        return redirect('login')
    
def resetpassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['Confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetPassword.html')