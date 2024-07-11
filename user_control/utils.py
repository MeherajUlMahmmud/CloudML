from django.core.mail import EmailMessage
from ip2geotools.databases.noncommercial import DbIpCity


class Util:

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_country_from_ip(ip):
        print(ip)
        response = DbIpCity.get(ip, api_key='free')
        print(response)
        return response.country

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
        )
        email.send()
