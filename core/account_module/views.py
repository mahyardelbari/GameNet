from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .models import User
from .forms import RegisterForm
from .utils import helper


def register(request):
    form = RegisterForm
    if request.method == 'POST':
        try:
            if 'mobile' in request.POST:
                mobile = request.POST.get('mobile')
                user = User.objects.get(mobile=mobile)

                # send otp
                otp = helper.get_random()
                # helper.send_otp(mobile, otp)
                print(otp)
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                return redirect('verify')

        except User.DoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # Send otp
                otp = helper.get_random()
                print(otp)
                # helper.send_otp(mobile, otp)
                # save otp
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                messages.success(request, 'ثبت‌نام با موفقیت انجام شد. کد فعالسازی به شماره موبایل شما ارسال شد.')
                return redirect('verify')
    return render(request, "account_module/register.html", {'form': form})

def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        user = User.objects.get(mobile=mobile)
        if request.method == 'POST':
            # Check otp time
            if  helper.check_otp_expiration(user.mobile) == False:
                messages.error(request, 'زمان مجاز ورود کد فعالسازی به پایان رسیده است.')
                return redirect('register')

            if user.otp != int(request.POST.get('otp')):
                messages.error(request, 'کد فعالسازی اشتباه است.')
                return redirect('verify')
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'حساب کاربری شما با موفقیت فعال شد.')
            return redirect('dashboard')
        return render(request, 'account_module/verify.html', {'mobile': mobile})
    except User.DoesNotExist:
        messages.error(request, 'ثبت‌نام انجام نشده است.')
        return redirect('register')

def dashboard(request):
    return render(request, 'account_module/dashboard.html')
