from django.db import models
from django.urls import reverse #Used to generate URLS by reversing the URL patterns
import uuid #Required for unique orphan instances
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	#Model representing an article
	artNum = models.CharField(max_length=8)
	name = models.CharField(max_length=20)
	totBoxes = models.IntegerField()

	def __str__(self):
		#String for representing the Model Object
		return '{0} - {1}'.format(self.artNum, self.name)

class Orphan(models.Model):
	"""
	Model representing an orphan (but not a specific orphan)
	"""
	article = models.ForeignKey('Article', on_delete=models.SET_NULL, null=True)
	#Foreign key used because orphan can only have one article, but a single article can have many orphans
	#Article as a string rather than an object becuase it hasn't been declared yet in the file.
	boxNum = models.IntegerField('Box Number')
	def display_artNum(self):
		return self.article.artNum

	display_artNum.short_description = 'Article Number'


	def display_artName(self):
		return self.article.name

	display_artName.short_description = 'Name'

	def __str__(self):
		#String for representing Model object.
		return 'Box {0}'.format(self.boxNum)

	def get_absolute_url(self):
		#Returns the url to access a detail record for this book.
		return reverse('orphan-detail', args=[str(self.id)])

class OrphanInstance(models.Model):
#Model representing a sepcific orphan (that can be shelved/trashed/ or 450'd)
	id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
	orphan = models.ForeignKey('Orphan', on_delete=models.SET_NULL, null=True)
	date = models.DateField(null=True, blank=True)
	ORPHAN_STATUS = (
		('a', 'Available'),
		('s', 'Spare Parts'),
		('o', 'Open/Damaged'),
		)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=1, choices=ORPHAN_STATUS, blank=True, default='a', help_text= 'Orphan Box Status')

	class Meta:
		ordering = ["date"]

	def display_artNum(self):
		return self.orphan.article.artNum

	display_artNum.short_description = 'Article Number'


	def display_artName(self):
		return self.orphan.article.name

	display_artName.short_description = 'Name'

	def display_boxNum(self):
		return self.orphan.boxNum

	display_boxNum.short_description = 'Box Number'

	def __str__(self):
		#String representing Model Object
		return '{0} ({1})'.format(self.id,self.orphan.boxNum)

	@property
	def is_old(self):
		return self.date < datetime.date.today()-datetime.timedelta(days=14)

	def is_getting_old(self):
		return self.date < datetime.date.today()-datetime.timedelta(days=7)
