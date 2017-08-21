from DigiNehruPy.settings import (EMAIL_HOST, EMAIL_HOST_USER,
                                  EMAIL_HOST_PASSWORD)
from students.models import Students
import hashlib
from django.core.mail import EmailMultiAlternatives, get_connection
from datetime import datetime
connection = get_connection(username=EMAIL_HOST_USER,
                            password=EMAIL_HOST_PASSWORD,
                            fail_silently=False)


def send_email(email, token):
    from_email = EMAIL_HOST_USER
    subject = "Your Token"
    to_email = email
    to = [to_email]
    email_text = token
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
    i = 0
    while True:
        tks = s.roll + str(datetime.now())
        tk = int(hashlib.sha1(tks).hexdigest(), 16) % (10 ** 6)
        try:
            Students.objects.get(token=tk)
        except Students.DoesNotExist:
            s.token = tk
            s.save()
            send_email(s.email, s.token)
            break
        except Exception as e:
            # send_email()
            print e
print "Done"
