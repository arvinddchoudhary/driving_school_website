import random
from django.core.mail import send_mail # type: ignore


def generate_otp():
    return random.randint(100000, 999999)  # 6-digit OTP


def send_otp(email, purpose='registration'):
    otp = generate_otp()
    
    if purpose == 'registration':
        subject = "Your OTP for Registration"
        message = f"Your OTP is {otp}. Please use this to complete your registration."
    elif purpose == 'reset_password':
        subject = "Your OTP for Password Reset"
        message = f"Your OTP is {otp}. Please use this to reset your password."

    from_email = 'your_email@gmail.com'
    send_mail(subject, message, from_email, [email])
    return otp



