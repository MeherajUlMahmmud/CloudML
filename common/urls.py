from django.urls import path

from common.views import IndexView, ContactUsModelAPIView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/', IndexView.as_view()),

    path('api/contact-us/create/', ContactUsModelAPIView.as_view(), name='contact_us'),
]
