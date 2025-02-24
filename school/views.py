from django.shortcuts import render, redirect # type: ignore
from django.core.mail import send_mail # type: ignore
from django.conf import settings # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import logout as auth_logout  # type: ignore
from .models import Course, Home, Instructors

def index(request):
    home_data = Home.objects.all() 
    return render(request, 'index.html', {'Home_data': home_data})


def instructors(request):
    instructors = Instructors.objects.all()
    return render(request, 'instructors.html', {'instructors': instructors})

def courses(request):
    courses = Course.objects.all()    
    return render(request, 'courses.html', {'courses': courses})




def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Prepare the email content
        email_subject = f"Message from {name} - {subject}"
        email_body = f"Name: {name}\nPhone number: {phone}\n\nMessage:\n{message}"

        # Send the email
        try:
            send_mail(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,  # Your email address (sender)
                ['newandajmotordrivingschool@gmail.com'],  # The email address where you want to receive the message
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully! Our team will contact you soon.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")

        return redirect('contact')
    
    return render(request, 'contact.html')


from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from django.contrib import messages # type: ignore
from accounts.models import Registration  # Import your Registration model
from django.contrib.auth.hashers import check_password  # type: ignore # Import for checking password
from django.contrib.auth.models import User # type: ignore

def portal(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the email exists in the Registration table
        try:
            user = Registration.objects.get(email=email)
        except Registration.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return redirect('portal')  # Redirect to login if email is not found
        
        # Check if the password matches the stored (hashed) password
        if check_password(password, user.password):
            # Store user info in session
            request.session['user_id'] = user.id
            request.session['email'] = user.email
            request.session['first_name'] = user.first_name
            request.session['course'] = user.course
            request.session['start_date'] = user.start_date.strftime('%Y-%m-%d')  # Convert date to string
            request.session['time_slot'] = user.time_slot
            
            messages.success(request, 'Login successful!')
            return redirect('portal')  # Redirect to portal after login
        else:
            messages.error(request, 'Invalid email or password.')

    # Check if the user is logged in by checking the session
    user_id = request.session.get('user_id')  # Fetch user from session
    if user_id:
        try:
            user = Registration.objects.get(id=user_id)
            context = {
                'user': user,
                'start_date': user.start_date,
                'course': user.course,
                'time_slot': user.time_slot
            }
            return render(request, 'portal.html', context)  # Render student details if logged in
        except Registration.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('portal')
    
    # If not logged in, show the login form
    return render(request, 'portal.html')

def logout(request):
    # Log the user out
    auth_logout(request)
    request.session.flush()  # Ensure session data is cleared
    
    # Redirect to the portal page after logout
    return redirect('portal')
    
from django.shortcuts import render # type: ignore
from .models import FaqItem

def faq(request):
    faq_items = FaqItem.objects.all()  
    return render(request, 'faq.html', {'faq_items': faq_items})




