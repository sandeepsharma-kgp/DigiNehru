
from students.models import Students
from datetime import datetime
from django.utils.crypto import get_random_string


def send_email(msg, subject):
    from DigiNehruPy.settings import (EMAIL_HOST, EMAIL_HOST_USER,
                                      EMAIL_HOST_PASSWORD)
    from django.core.mail import EmailMultiAlternatives, get_connection

    connection = get_connection(username=EMAIL_HOST_USER,
                                password=EMAIL_HOST_PASSWORD,
                                fail_silently=False)
    from_email = "diginehru@gmail.com"
    to_email = from_email
    to = [to_email]
    email_text = msg
    message_arr = []
    msg = EmailMultiAlternatives(
        subject, email_text, from_email, to)
    message_arr.append(msg)
    try:
        connection.open()
        connection.send_messages(message_arr)
        connection.close()
    except Exception as e:
        print e

st = Students.objects.all()

for s in st:
    s.token = ""
    s.save()

for s in st:
    found = 1
    while found:
        tk = get_random_string(length=4, allowed_chars='1234567890')
        try:
            Students.objects.get(token=tk)
        except Students.DoesNotExist:
            found = 0
            s.token = tk
            s.save()
        except Exception as e:
            import traceback
            error_msg = {}
            error_msg["TRACEBACK"] = traceback.format_exc()
            error_msg["ID"] = s.roll
            error_msg = json.dumps(error_msg)
            send_email(error_msg, "Token-Error")

send_email("Token Distributed Successfully!!", "Token-Success")
