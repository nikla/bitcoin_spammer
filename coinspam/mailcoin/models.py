from django.db import models
from django.forms import ModelForm

class WalletApi (models.Model) :
	walletId = models.CharField(max_length=22)
	walletAddress = models.CharField(max_length=34)
	walletBalance = models.DecimalField(max_digits=16, decimal_places=8)
	
class WalletForm (ModelForm) :
	class Meta :
		model = WalletApi
		fields = ('walletId',)

class sendModel (models.Model):
	email = models.EmailField()
	amountToSend = models.DecimalField(max_digits=16, decimal_places=8)

class EmailForm (ModelForm):
	class Meta :
		model = sendModel
		fields = ('email','amountToSend',)
