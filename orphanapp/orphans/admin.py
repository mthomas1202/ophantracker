from django.contrib import admin
from .models import Orphan, Article, OrphanInstance
# Register your models here.

#admin.site.register(Orphan)
#admin.site.register(Article)
#admin.site.register(OrphanInstance)


class OrphanInline(admin.TabularInline):
	model = Orphan

#Define the admin class
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('artNum', 'name', 'totBoxes')
	fields = ['artNum', 'name', 'totBoxes']
	inlines = [OrphanInline]
#Register the admin class with the associated model
admin.site.register(Article, ArticleAdmin)

class OrphanInstanceInline(admin.TabularInline):
	model = OrphanInstance
#Register the Admin classes for Orphan using the decorator
@admin.register(Orphan)
class OrphanAdmin(admin.ModelAdmin):
	list_display = ('display_artNum', 'display_artName', 'boxNum')
	inlines = [OrphanInstanceInline]

#Register the Admin class for OrphanInstance using the decorator
@admin.register(OrphanInstance)
class OrphanInstanceAdmin(admin.ModelAdmin):
	list_display = ('display_artNum', 'display_artName', 'display_boxNum','created_by', 'date')
	list_filter = ('status', 'date',)

	fieldsets = (
		(None, {
			'fields': ('orphan', 'id')
			}),
		('Status', {
			'fields': ('status', 'user', 'date')
			}),
		)