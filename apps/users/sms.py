import math, random
import ghasedakpack


def generateOTP() :
   # Declare a digits variable  
   # which stores all digits 
   digits = "123456789"
   OTP = ""
   
   # length of password can be changed
   # by changing value in range
   for i in range(4) :
      OTP += digits[math.floor(random.random() * 10)]
   return OTP


def sendSmsToPhone(phone):
   API_KEY= "076eed4b42336572ed5a9547f380308ab2e9b00741c37faee95f2db899667e96"

   verif_code = generateOTP()
   
   sms = ghasedakpack.Ghasedak(apikey = API_KEY)
   sms.verification({
      'receptor': phone, 
      'type': '1',
      'template': 'blogotp',
      'param1': verif_code 
   })
   
   



