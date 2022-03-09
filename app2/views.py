from django.db import connection
from django.shortcuts import render


# Create your views here.
def abc(request):
    return render(request, "index.html")


def Register(request):
    email = request.GET['email']
    psw = request.GET['psw']
    cursor = connection.cursor()
    query = '''insert into users(email,password)values(%s, %s) '''
    value = (email, psw)
    cursor.execute(query, value)
    data = {"email": email, "password": psw}
    return render(request, "first.html", data)
