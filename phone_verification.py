#!/usr/bin/env python3
"""Phone verification logic"""
import os
import typing
import math
import random
from twilio.rest import Client

"""Twilio Credientials"""

# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC10f506b95409c6b7be812dafa3f2e581"
auth_token = "21b9eed775257c8f4ddf6fcf396f368a"
verify_sid = "VA9f46457c5fe40e28010dce7f19d2d95b"
verified_number = "+2347066041638"

client = Client(account_sid, auth_token)

verification = client.verify.v2.services(
        verify_sid
        ).verifications.create(to='+2347010744571', channel="sms")
print(verification.status)

otp_code = input("Please enter the OTP:")

verification_check = client.verify.v2.services(verify_sid) \
  .verification_checks \
  .create(to='+2347010744571', code=otp_code)
print(verification_check.status)


# def generate_pass():
#     return str(random.randint(10000, 99999))
# def send_otp(number, otp):
#     try:
#         if number is None:
#             return
#         client = Client(account_sid, auth_token)
#         message = client.messages.create(
#             body=f'Your OTP is: {otp}',
#             from_=verified_number,
#             to=number
#         )

#         print(f'OTP sent successfully. SID: {message.sid}')
#     except Exception as e:
#         print(f'An error occurred: {str(e)}')


# def main():
#     receiver = input('Enter a phone number: \n')
#     otp = generate_pass()

#     send_otp(receiver, otp)
# if __name__ == '__main__':
#     main()
