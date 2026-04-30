"""
URL configuration for hospitalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/doctors/', include('doctorsapp.urls')),
    path('api/patients/', include('patientsapp.urls')),
    path('api/appointments/', include('appointmentsapp.urls')),
    path('api/reviews/', include('reviewsapp.urls')),
    path('api/staffs/', include('staffsapp.urls')),
    
    path('rag/', include('Ragapp.urls')),
    
  
    
]



# আপনি যখন প্রথমবার কাজ শুরু করবেন, তখন প্রথমে POST রিকোয়েস্ট পাঠিয়ে /api/rag/rebuild-embeddings/ হিট করবেন। এতে করে ডাটাবেজের ডাক্তারদের ডাটা ভেক্টরে রূপান্তর হবে। এরপর আপনি চ্যাট করার জন্য প্রস্তুত!