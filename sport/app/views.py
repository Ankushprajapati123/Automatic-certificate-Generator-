from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
import os
from django.core.files.storage import FileSystemStorage
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import FileResponse

def base(request):
    return render(request,'base.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    if request.method == "POST":
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request, username=un, password=pw)
        if user is not None:
            auth_login(request, user)
            return redirect('/profile')  # Redirect to profile after successful login
        else:
            msg = 'Invalid Username/Password'
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Redirect to the login page after successful signup
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def generate_certificate(name, game, today_date, template_path, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)

    # Draw the template image to fit A4 size
    c.drawImage(template_path, 0, 0, width=595.27, height=841.89)

    # Add text to the PDF
    c.setFont("Helvetica", 20)
    c.drawString(200, 507, f"{name}")

    c.setFont("Helvetica", 15)
    c.drawString(210, 377, f"Game: {game}")
    c.drawString(230, 227, f"{today_date}")

    # Save the generated PDF
    c.save()

def profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        game = request.POST.get('game')
        today_date = date.today().strftime("%d %B %Y")

        template_path = "static/images/certificate_Template.png" 
        output_path = f"generated/{name}_certificate.pdf"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        generate_certificate(name, game, today_date, template_path, output_path)

        return FileResponse(open(output_path, 'rb'), as_attachment=True, filename=f"{name}_certificate.pdf")

    return render(request, 'profile.html')
