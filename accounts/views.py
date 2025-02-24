import random
from django.core.mail import send_mail # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from .models import Registration
from django.contrib.auth.hashers import make_password # type: ignore
from .utils import send_otp
from django.conf import settings # type: ignore
from django.contrib.auth.hashers import check_password # type: ignore

# Register View (remains unchanged)
def register(request):
    # Get course from the URL query parameters, default to None if not provided
    course = request.GET.get('course', None)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm-password')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        course = request.POST.get('course', course)  # Use the course from the form, or the one from the URL
        start_date = request.POST.get('start_date')
        time_slot = request.POST.get('time_slot')
        experience = request.POST.get('experience')
        notes = request.POST.get('notes', '')

        if password1 == password2:
            if Registration.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return redirect('register')
            else:
                otp = send_otp(email, purpose='registration')
                request.session['otp'] = otp
                request.session['email'] = email
                request.session['password'] = make_password(password1)
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['phone'] = phone
                request.session['location'] = location
                request.session['course'] = course
                request.session['start_date'] = start_date
                request.session['time_slot'] = time_slot
                request.session['experience'] = experience
                request.session['notes'] = notes

                messages.success(request, 'OTP sent to your email!')
                return redirect('validate_otp')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

    return render(request, 'register.html', {'selected_course': course})


# Validate OTP View (with confirmation email)
def validate_otp(request):
    if request.method == 'POST':
        otp = ''.join([request.POST.get(f'otp{i}', '').strip() for i in range(1, 7)])
        stored_otp = str(request.session.get('otp', '')).strip()

        print("Entered OTP:", otp)
        print("Stored OTP:", stored_otp)

        if otp == stored_otp:
            # Retrieve user details from session
            email = request.session.get('email')
            password = request.session.get('password')
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            phone = request.session.get('phone')
            location = request.session.get('location', 'Not provided')
            course = request.session.get('course')
            start_date = request.session.get('start_date')
            time_slot = request.session.get('time_slot')
            experience = request.session.get('experience')
            notes = request.session.get('notes')

            # Save user registration
            registration = Registration.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                phone=phone,
                location=location,
                course=course,
                start_date=start_date,
                time_slot=time_slot,
                experience=experience,
                notes=notes
            )
            registration.save()

            # Send registration details email to admin
            subject_admin = f"New Registration: {first_name} {last_name}"
            message_admin = f"""
                A new student has successfully registered:

                Name: {first_name} {last_name}
                Email: {email}
                Phone: {phone}
                Address: {location}
                Course: {course}
                Start Date: {start_date}
                Time Slot: {time_slot}
                Experience: {experience}
                Notes: {notes}
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.ADMIN_EMAIL]
            send_mail(subject_admin, message_admin, from_email, recipient_list)

            # Send confirmation email to user
            subject_user = "Thank you for your registration!"
            message_user = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <p>Hello {first_name} {last_name},</p>

                <p>Thank you for registering for the <strong>{course}</strong> course with us. We have received your registration,
                and our team will contact you soon to finalize the details.</p>

                <h3>Your Registration Details:</h3>
                <ul>
                    <li><strong>Course:</strong> {course}</li>
                    <li><strong>Start Date:</strong> {start_date}</li>
                    <li><strong>Time Slot:</strong> {time_slot}</li>
                </ul>

                <p>If you have any questions or need further assistance, feel free to contact us.</p>
                <p>Phone: 8696555563</P>

                <p>Best regards,</p>
                <p><strong>New Andaj Motor Driving School</strong></p>
            </body>
        </html>
    """
            send_mail(subject_user, message_user, from_email, [email], html_message=message_user)


            # Clear session data
            for key in ['otp', 'email', 'password', 'first_name', 'last_name', 'phone', 'location', 'course', 'start_date', 'time_slot', 'experience', 'notes']:
                request.session.pop(key, None)

            messages.success(request, "Registration successful. A confirmation email has been sent.")
            return redirect('register')  # Redirect to register page

        else:
            messages.error(request, "Invalid OTP.")
            return redirect('validate_otp')

    return render(request, 'validate_otp.html')


# Resend OTP View
def resend_otp(request):
    email = request.session.get('email')
    if email:
        otp = send_otp(email)
        request.session['otp'] = otp
        messages.success(request, "A new OTP has been sent to your email.")
    else:
        messages.error(request, "Unable to resend OTP. Please try again.")
    return redirect('validate_otp')




from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore
from .models import Registration  # Importing the custom Registration model
from .utils import send_otp  # Ensure send_otp function is implemented correctly

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        # Check if the email exists in the Registration model
        if Registration.objects.filter(email=email).exists():
            otp = send_otp(email, purpose='reset_password')  # Sending OTP to the user’s email
            request.session['otp'] = otp
            request.session['email'] = email

            messages.success(request, "OTP sent to your email.")
            return redirect('validate_otp2')
        else:
            messages.error(request, "Email not found. Please register first.")
            return redirect('forget_password')

    return render(request, 'forget_password.html')

def reset_password(request):
    if request.method == 'POST':
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']

        if password1 == password2:
            email = request.session.get('reset_email')
            try:
                user = Registration.objects.get(email=email)  # Get user by email
                user.password = make_password(password1)  # Hash the password before saving
                user.save()
                del request.session['reset_email']
                messages.success(request, "Password reset successful! Please log in.")
                return redirect('portal')  # Redirecting to login after reset
            except Registration.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('forget_password')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

    return render(request, 'reset_password.html')

def validate_otp2(request):
    if request.method == 'POST':
        # Concatenating the OTP digits
        otp = ''.join([
            request.POST.get(f'otp{i}', '') for i in range(1, 7)
        ])
        user_otp = otp

        if int(user_otp) == request.session.get('otp'):
            email = request.session.get('email')

            try:
                user = Registration.objects.get(email=email)  # Get user by email
                # Store email for password reset
                request.session['reset_email'] = email
                # Clear OTP after successful verification
                del request.session['otp']
                messages.success(
                    request, "OTP verified! Set your new password.")
                # Redirect to reset password page
                return redirect('reset_password')
            except Registration.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('forget_password')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('validate_otp2')

    return render(request, 'validate_otp.html')





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