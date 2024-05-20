from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Period)
admin.site.register(Baby)
admin.site.register(BabyPayment)
admin.site.register(Sitter)
admin.site.register(Sitter_on_duty)
admin.site.register(SitterPayment)
admin.site.register(ItemSelling)
admin.site.register(AddItem)