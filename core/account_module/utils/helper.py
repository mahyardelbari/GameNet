from kavenegar import *
from core.settings import KAVENEGAR_API
from random import randint
import datetime
from account_module.models import User
def send_otp(mobile, otp):
	mobile = [mobile]
	try:
		api = KavenegarAPI(KAVENEGAR_API)
		params = {
			'sender': '10004346',
			'receptor': mobile,
			'message': f'کد ورود شما{otp}',
		}
		response = api.sms_send(params)
		print(f'otp : {otp}')

	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)

def get_random():
	return randint(1000, 9999)

def check_otp_expiration(mobile):
	try:
		user = User.objects.get(mobile=mobile)
		now = datetime.datetime.now()
		otp_time = user.otp_create_time
		diff_time = now - otp_time
		print(f'otp time : {diff_time}')
		# if diff_time.seconds > 120:
		# 	return False
		return True

	except User.DoesNotExist:
		return False
