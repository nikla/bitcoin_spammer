# Create your views here.
from mailcoin.models import WalletApi, WalletForm, sendModel, EmailForm
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import httplib
from django.http import HttpResponse
import json
from decimal import *
import urllib
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

@csrf_exempt
def index(request):
	form = WalletForm()
	eForm = EmailForm()
	if request.method == 'POST':
		try:
			walletId = request.POST['walletid']
			Balance = UseOldWallet (walletId)
			hinta = str(Balance) + " BC"
			address = getAddress(walletId)
			addressqr = qrcode(address)
			return HttpResponse(json.dumps({"walletid":walletId,"balance": float(Balance)}))
			#~ return HttpResponse(json.dumps(response_data), 
				#~ mimetype="application/json")
			#~ return render_to_response('coinspam/index.html', {
				#~ 'form': form,
				#~ 'walletId': walletId,
				#~ 'balance': Balance,
				#~ 'address': address,
				#~ 'qrcode': addressqr,
				#~ 'emailform': eForm,
			#~ })
			
		except (KeyError):
			walletId = CreateNewWallet()
			Balance = UseOldWallet (walletId)
			address = getAddress(walletId)
			addressqr = qrcode(address)
			return HttpResponse(json.dumps({"walletid":walletId,"balance": float(Balance)}))
		return render_to_response('coinspam/index.html')
	return render_to_response('coinspam/index.html', {
		'form': form,
		'emailform': eForm,
	})

@csrf_exempt
def sendcoins(request):
	if request.method == 'POST':
		try:
			email = request.POST['email']
			amount = request.POST['amount']
			walletid = request.POST['walletid']
			vastaus = SendPaymentToMail(email, walletid, amount)
			return HttpResponse(json.dumps(vastaus))
		except (KeyError):
			return HttpResponse(json.dumps({"successful" : False}))
	else:
		return HttpResponse(json.dumps({"successful" : False}))
		
		
#~ def parse
def SendPaymentToMail(email, walletid, amount):
	parameters = urllib.urlencode({'address': email,'amount': amount })
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	paymentRequest = httplib.HTTPSConnection("easywallet.org")
	paymentRequest.request("POST", "/api/v1/w/"+ walletid + "/payment", parameters, headers)
	response = paymentRequest.getresponse().read()
	paymentRequest.close()
	return json.loads(response)
	

def CreateNewWallet():
	newWalletRequest = httplib.HTTPSConnection("easywallet.org")
	newWalletRequest.request("POST", "/api/v1/new_wallet")
	response = newWalletRequest.getresponse().read()
	newWalletRequest.close()
	return json.loads(response)['wallet_id']
	
def UseOldWallet(_walletID):
	if _walletID == "":
		return "Wrong wallet id!"
	getWallet = httplib.HTTPSConnection("easywallet.org")
	getWallet.request("GET", "/api/v1/w/" + _walletID + "/balance")
	response = getWallet.getresponse().read()
	getWallet.close()
	if json.loads(response)['successful']:
		return Decimal(json.loads(response)['balance'])
	else :
		return "Wrong wallet id!"
		
def getAddress (_walletID):
	if _walletID == "":
		return ""
	getWallet = httplib.HTTPSConnection("easywallet.org")
	getWallet.request("GET", "/api/v1/w/" + _walletID + "/address")
	response = getWallet.getresponse().read()
	getWallet.close()
	if json.loads(response)['successful']:
		return json.loads(response)['address']
	else :
		return ""
	
register = template.Library()
@register.filter
@stringfilter
def qrcode(value, alt=None):
    """
    Generate QR Code image from a string with the Google charts API
    
    http://code.google.com/intl/fr-FR/apis/chart/types.html#qrcodes
    
    Exemple usage --
    {{ my_string|qrcode:"my alt" }}
    
    <img src="http://chart.apis.google.com/chart?chs=150x150&amp;cht=qr&amp;chl=my_string&amp;choe=UTF-8" alt="my alt" />
    """
    
    url = conditional_escape("http://chart.apis.google.com/chart?%s" % \
            urllib.urlencode({'chs':'150x150', 'cht':'qr', 'chl':value, 'choe':'UTF-8'}))
    alt = conditional_escape(alt or value)
    
    return mark_safe(u"""<img class="qrcode" src="%s" width="150" height="150" alt="%s" />""" % (url, alt))
