from django.shortcuts import render, redirect, HttpResponse
from .models import User, ConfirmString
from .forms import UserForm, RegisterForm
import hashlib
from mysite import send_mail
import datetime
from django.conf import settings

# Create your views here.


def index(request):
    """首页"""
    return render(request, 'login/index.html')


def login(request):
    """登录页面"""
    if request.session.get('is_login', None):
        print(request.seesion.get('is_login'))
        return redirect('index')

    if request.method == 'POST':
        message = '所有字段都必须填写'
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if not user.has_confirmed:
                    message = '该用户还未通关邮件确认'
                    return render(request, 'login/login.html', locals())

                # if user.password == password:
                if user.password == hash_code(password):    # 哈希值和数据库内值进行对比

                    # 往 session 字典内写入用户状态和数据
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name

                    # 验证通过重定向到首页
                    return redirect('index')
                else:
                    message = '密码错误'
                    return render(request, 'login/login.html', locals())
            except:
                message = '用户名不存在'
                return render(request, 'login/login.html', locals())
        return render(request, 'login/login.html', locals())

    # 为 get 方法时，login_form 为空
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    """
    注册页面
    检查用户名、邮箱是否存在
    """
    if request.session.get('is_login', None):
        # 登录状态不许注册
        return redirect('index')
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'login/register.html', {'register_form': register_form})
    else:
        register_form = RegisterForm(request.POST)
        message = '请检查填写内容'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']

            if password1 != password2:
                message = '两次密码输入不同'
                return render(request, 'login/register.html', locals())
            else:
                # 检查用户名是否存在
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经被注册'
                    return render(request, 'login/register.html', locals())

                # 检查邮箱是否存在
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已被注册'
                    return render(request, 'login/register.html', locals())

                # password = hash_code(password2)     # 对密码进行哈希加密
                # User.objects.create(
                #     name=username,
                #     password=password,
                #     email=email,
                #     sex=sex
                # )

                # 另一种方式进行添加
                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password2)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                # 生成注册码 code，发送邮件，进行邮件注册确认
                code = make_confirm_string(new_user)
                send_mail.send_email(email, code)
                message = '请前往注册邮箱，进行邮箱确认'

                return render(request, 'login/confirm.html', locals())

        return render(request, 'login/register.html', locals())


def logout(request):
    """登出，重定向到首页"""
    if not request.session.get('is_login', None):
        # 如果没有登录，也就没有登出一说
        return redirect('index')

    request.session.flush()     # 删除当前的会话数据和会话cookie。经常用在用户退出后，删除会话。
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']

    return redirect('index')


def hash_code(s, salt='mysite'):        # 加盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())        # update 只接收 bytes 类型
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # '2019-02-24 15:05:03'
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def user_confirm(request):
    """当用户点击邮件确认邮件时，处理那个链接中的 code"""
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'login/confirm.html', locals())

    created_time = confirm.created_time
    now = datetime.datetime.now()
    if now > created_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '你的邮件已过期，请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.user.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())


def test(request):
    """处理 Ajax 请求"""
    return render(request, 'login/test.html')


def ajax(request):
    print(request.GET)      # <QueryDict: {'username': ['a']}>
    import json
    ret = {'message': None}
    username = request.GET.get('username')
    print(username)
    new_user = User.objects.filter(name=username)
    if new_user:
        ret['message'] = '用户名已存在'
        return HttpResponse(json.dumps(ret))

