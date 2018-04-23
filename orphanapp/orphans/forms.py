from django import forms
from .models import Orphan, OrphanInstance, Article
import datetime #for checking renewal date range.
from extra_views import InlineFormSet

class AddOrphanForm(forms.ModelForm):
	class Meta:
		model=OrphanInstance
		fields=['date','status']
		initial = {'date': datetime.datetime.strftime(datetime.datetime.today(),"%m/%d/%Y")}


class InstanceInline(InlineFormSet):
	model = OrphanInstance
	fields = ['date','status']
	form_class = AddOrphanForm

	


