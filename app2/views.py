import string

from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from random import randint, choice
from django.core.mail import send_mail


# Create your views here.


def abc(request):
    return render(request, "home.html")


def Register(request):
    email = request.POST['email']
    psw = request.POST['psw']
    mobile = request.POST['mobile_no']
    city = request.POST['city']
    cursor = connection.cursor()
    query = "Select email from user where email='" + email + "'"
    cursor.execute(query)
    row = cursor.fetchone()
    print(cursor.rowcount)
    if row is None:
        otp = randint(1000, 9999)
        query = '''insert into user(email,password,mobile_no,city,otp)values(%s, %s, %s, %s, %s) '''
        value = (email, psw, mobile, city, otp)
        cursor.execute(query, value)
        body = "Your otp for our portal you signed up with mail " + email + " is " + str(otp) + ""
        send_mail('otp for verification', body, 'xman30462@gmail.com', [email])
        data = {"email": email}
        return render(request, "verify.html", data)
    else:
        data = {"email": email}
        return render(request, "login.html", data)


def login(request):
    email = request.POST['email']
    psw = request.POST['psw']
    cursor = connection.cursor()
    query1 = "select * from user where email  ='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is None:
        data = {"email": "Not SignedUP", "password": ""}
        return render(request, "signed_in.html", data)
    else:
        if data[6] == 0:
            data = {"email": "You are not verified user", "password": ""}
            return render(request, "signed_in.html", data)
        if data[2] == int(psw):
            data = {"email": "Login Success", "password": ""}
            return render(request, "signed_in.html", data)
        else:
            data = {"email": "Password is not correct", "password": ""}
            return render(request, "signed_in.html", data)


def otpVerification(request):
    otp = request.POST['otp']
    email = request.POST['email']
    cursor = connection.cursor()
    query1 = "Select * from user where email='" + email + "'"
    cursor.execute(query1)
    row = cursor.fetchone()
    if row is not None:
        if str(row[5]) == otp:
            query2 = "update user set verify = '1' where email='" + email + "'"
            cursor.execute(query2)
            if cursor.rowcount == 1:
                data = {"email": "otp verified successful"}
                return render(request, "signed_in.html", data)
        else:
            data = {"email": "otp is not correct"}
            return render(request, "signed_in.html", data)


def generateShortURl():
    letters = string.ascii_letters + string.digits
    shortUrl = ''
    for i in range(6):
        shortUrl = shortUrl + ''.join(choice(letters))
    return shortUrl


def urlshortner(request):
    longLink = request.GET['link']
    customUrl = request.GET['customurl']
    if customUrl is None or customUrl == '':
        shortUrl = ''
    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link  ='" + customUrl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {"email": "Already Custom URL exist please try some other url"}
            return render(request, "signed_in.html", data)
        else:
            query2 = "insert into links (long_link, short_link) values (%s, %s)"
            value = (longLink, customUrl)
            cursor.execute(query2, value)
            data = {"email": "Your URl is shortne with nano.co/" + customUrl}
            return render(request, "signed_in.html", data)
    if shortUrl is not None or shortUrl != '':
        while True:
            shortUrl = generateShortURl()
            cursor = connection.cursor()
            query1 = "select * from links where short_link  ='" + shortUrl + "'"
            cursor.execute(query1)
            data = cursor.fetchone()
            if data is None:
                break
        query2 = "insert into links (long_link, short_link) values (%s, %s)"
        value = (longLink, shortUrl)
        cursor.execute(query2, value)
        data = {"email": "Your URl is shortne with nano.co/" + shortUrl}
        return render(request, "signed_in.html", data)


def generateShortURlApi(request):
    letters = string.ascii_letters + string.digits
    shortUrl = ''
    for i in range(6):
        shortUrl = shortUrl + ''.join(choice(letters))
    return JsonResponse({"shortUrl": shortUrl, "success": "success"})
