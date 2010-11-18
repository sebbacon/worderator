from django.contrib import admin
import models

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'email')

class WordDBAdmin(admin.ModelAdmin):
    list_display = ('name','description')

class TailInline(admin.TabularInline):
    model = models.Tail
    raw_id_fields = ("word",)
    
class StemAdmin(admin.ModelAdmin):
    list_display = ('word','is_root', 'tails_str',)
    inlines = [TailInline,]
    
admin.site.register(models.CustomUser, UserAdmin)
admin.site.register(models.WordDB, WordDBAdmin)
admin.site.register(models.Stem, StemAdmin)
