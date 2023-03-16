from django.contrib import admin
from .models import Ad, MpesaCalls, MpesaCallBacks, MpesaPayment
# Register your models here.
admin.site.register(Ad)
admin.site.register(MpesaCalls)
admin.site.register(MpesaCallBacks)
admin.site.register(MpesaPayment)



