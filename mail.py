'''
Send-In-Blue: SMTP API
'''

import os
import requests  #tokenZ as tz
import datetime , random

api = os.environ.get('smtp_api')
otp_api = os.environ.get('otp_api')

url = "https://api.brevo.com/v3/smtp/email"
otp_url = "https://www.fast2sms.com/dev/bulkV2"

# Customize the HTML content with an embedded button link

OTP_HTML = """
<td align="center" style="padding: 1rem 2rem; vertical-align: top; width: 100%;">
  <table role="presentation" style="max-width: 600px; border-collapse: collapse; border: 0px; border-spacing: 0px; text-align: left;">
    <tbody>
      <tr>
        <td style="padding: 40px 0px 0px;">
          <div style="text-align: left;">
            <div style="padding-bottom: 20px;"><img src="https://i.ibb.co/Qbnj4mz/logo.png" alt="Company" style="width: 56px;"></div>
          </div>
          <div style="padding: 20px; background-color: rgb(255, 255, 255);">
            <div style="color: #499fb6; text-align: left; font-family: Arial, Helvetica, sans-serif;">
              <h1 style="margin: 1rem 0;">Verification code</h1>
              <p style="padding-bottom: 16px">Please use the verification code below to sign in.</p>
              <p style="padding-bottom: 16px; color: rgb(89, 225, 68)"><strong style="font-size: 130%">
                {}
              </strong></p>
              <p style="padding-bottom: 16px">If you didn’t request this, you can ignore this email.</p>
              <p style="padding-bottom: 16px">Thanks,<br>The Service-app team</p>
            </div>
          </div>
          <div style="padding-top: 20px; color: rgb(153, 153, 153); text-align: center;">
            <p style="padding-bottom: 16px">Made with ♥ in India</p>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</td>
"""

OTP = """
<body style="background-color: #f9fafb; font-family: 'Inter', sans-serif;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
        <div style="padding: 32px;">
            <div style="text-align: center; margin-bottom: 32px;">
                <img src="https://ai-public.creatie.ai/gen_page/logo_placeholder.png" alt="Service Booking Logo" style="height: 48px; margin: 0 auto 16px;">
                <h1 style="font-size: 24px; font-weight: 600; color: #1f2937;">ServiceBook</h1>
                <p style="color: #4b5563;">Your trusted service booking platform</p>
            </div>

            <div style="margin-bottom: 48px; border-bottom: 1px solid #e5e7eb; padding-bottom: 48px;">
                <h2 style="font-size: 24px; font-weight: 600; color: #1f2937; margin-bottom: 16px;">Verification Code</h2>
                <p style="color: #4b5563; margin-bottom: 24px;">Hi John,</p>
                <p style="color: #4b5563; margin-bottom: 24px;">Please use the following verification code to complete your action:</p>
                <div style="background-color: #f9fafb; border-radius: 8px; padding: 24px; text-align: center; margin-bottom: 24px;">
                    <div style="font-size: 32px; font-weight: 700; color: #000000; letter-spacing: 0.1em;">
                    {}
                    </div>
                </div>
                <p style="color: #6b7280; font-size: 14px;">This code will expire in 10 minutes.</p>
                <p style="color: #6b7280; font-size: 14px; margin-top: 16px;">If you didn't request this code, please ignore this email.</p>
            </div>

            <div style="margin-bottom: 48px; border-bottom: 1px solid #e5e7eb; padding-bottom: 48px;">
                <div style="background-color: rgba(0, 0, 0, 0.05); border-radius: 8px; padding: 24px;">
                    <h2 style="font-size: 24px; font-weight: 600; color: #1f2937; margin-bottom: 16px;">Special Offer!</h2>
                    <p style="font-size: 20px; font-weight: 600; color: #000000; margin-bottom: 16px;">Get 20% OFF on your first booking</p>
                    <p style="color: #4b5563; margin-bottom: 24px;">Book any service before December 31st and enjoy exclusive savings.</p>
                    <a href="#" style="background-color: #000000; color: #ffffff; padding: 12px 32px; border-radius: 8px; font-weight: 500; text-decoration: none; display: inline-block; transition: background-color 0.3s;">Book Now</a>
                </div>
            </div>

            <div style="text-align: center;">
                <div style="margin-bottom: 24px;">
                    <div style="display: flex; justify-content: center; gap: 16px;">
                        <a href="#" style="color: #9ca3af; text-decoration: none;">
                            <svg style="width: 24px; height: 24px;" viewBox="0 0 24 24">
                                <path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.54 2 12.04C2 16.84 5.66 20.74 10.26 21.54V14.89H7.89V12.04H10.26V9.79C10.26 7.42 11.71 6.04 13.82 6.04C14.82 6.04 15.87 6.24 15.87 6.24V8.54H14.68C13.5 8.54 13.26 9.24 13.26 10.04V12.04H15.76L15.36 14.89H13.26V21.54C17.86 20.74 21.52 16.84 21.52 12.04C21.52 6.54 17.02 2.04 12 2.04Z" />
                            </svg>
                        </a>
                        <a href="#" style="color: #9ca3af; text-decoration: none;">
                            <svg style="width: 24px; height: 24px;" viewBox="0 0 24 24">
                                <path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.54 2 12.04C2 16.84 5.66 20.74 10.26 21.54V14.89H7.89V12.04H10.26V9.79C10.26 7.42 11.71 6.04 13.82 6.04C14.82 6.04 15.87 6.24 15.87 6.24V8.54H14.68C13.5 8.54 13.26 9.24 13.26 10.04V12.04H15.76L15.36 14.89H13.26V21.54C17.86 20.74 21.52 16.84 21.52 12.04C21.52 6.54 17.02 2.04 12 2.04Z" />
                            </svg>
                        </a>
                        <a href="#" style="color: #9ca3af; text-decoration: none;">
                            <svg style="width: 24px; height: 24px;" viewBox="0 0 24 24">
                                <path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.54 2 12.04C2 16.84 5.66 20.74 10.26 21.54V14.89H7.89V12.04H10.26V9.79C10.26 7.42 11.71 6.04 13.82 6.04C14.82 6.04 15.87 6.24 15.87 6.24V8.54H14.68C13.5 8.54 13.26 9.24 13.26 10.04V12.04H15.76L15.36 14.89H13.26V21.54C17.86 20.74 21.52 16.84 21.52 12.04C21.52 6.54 17.02 2.04 12 2.04Z" />
                            </svg>
                        </a>
                        <a href="#" style="color: #9ca3af; text-decoration: none;">
                            <svg style="width: 24px; height: 24px;" viewBox="0 0 24 24">
                                <path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.54 2 12.04C2 16.84 5.66 20.74 10.26 21.54V14.89H7.89V12.04H10.26V9.79C10.26 7.42 11.71 6.04 13.82 6.04C14.82 6.04 15.87 6.24 15.87 6.24V8.54H14.68C13.5 8.54 13.26 9.24 13.26 10.04V12.04H15.76L15.36 14.89H13.26V21.54C17.86 20.74 21.52 16.84 21.52 12.04C21.52 6.54 17.02 2.04 12 2.04Z" />
                            </svg>
                        </a>
                    </div>
                </div>
                <div style="color: #6b7280; font-size: 14px; margin-bottom: 24px;">
                    <p style="margin-bottom: 8px;">Contact us: support@servicebook.com</p>
                    <p style="margin-bottom: 8px;">Phone: +1 (555) 123-4567</p>
                    <p>123 Booking Street, Service City, SC 12345</p>
                </div>

                <div style="display: flex; justify-content: center; gap: 16px; margin-bottom: 24px;">
                    <a href="#" style="display: flex; align-items: center; color: #4b5563; text-decoration: none;">
                        <svg style="width: 24px; height: 24px; margin-right: 8px;" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M12 2.04C6.5 2.04 2 6.54 2 12.04C2 16.84 5.66 20.74 10.26 21.54V14.89H7.89V12.04H10.26V9.79C10.26 7.42 11.71 6.04 13.82 6.04C14.82 6.04 15.87 6.24 15.87 6.24V8.54H14.68C13.5 8.54 13.26 9.24 13.26 10.04V12.04H15.76L15.36 14.89H13.26V21.54C17.86 20.74 21.52 16.84 21.52 12.04C21.52 6.54 17.02 2.04 12 2.04Z" />
                        </svg>
                        App Store
                    </a>
                    <a href="#" style="display: flex; align-items: center; color: #4b5563; text-decoration: none;">
                        <svg style="width: 24px; height: 24px; margin-right: 8px;" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M18.258,3.266c-0.693,0.405-1.46,0.698-2.277,0.857c-0.653-0.686-1.586-1.115-2.618-1.115c-1.98,0-3.586,1.581-3.586,3.53c0,0.276,0.031,0.545,0.092,0.805C6.888,7.195,4.245,5.79,2.476,3.654C2.167,4.176,1.99,4.781,1.99,5.429c0,1.224,0.633,2.305,1.596,2.938C2.999,8.349,2.445,8.19,1.961,7.925C1.96,7.94,1.96,7.954,1.96,7.97c0,1.71,1.237,3.138,2.877,3.462c-0.301,0.08-0.617,0.123-0.945,0.123c-0.23,0-0.456-0.021-0.674-0.062c0.456,1.402,1.781,2.422,3.35,2.451c-1.228,0.947-2.773,1.512-4.454,1.512c-0.291,0-0.575-0.016-0.855-0.049c1.588,1,3.473,1.586,5.498,1.586c6.598,0,10.205-5.379,10.205-10.045c0-0.153-0.003-0.305-0.01-0.456c0.7-0.499,1.308-1.12,1.789-1.827c-0.644,0.28-1.334,0.469-2.06,0.555C17.422,4.782,17.99,4.091,18.258,3.266" />
                        </svg>
                        Google Play
                    </a>
                </div>

                <div style="color: #9ca3af; font-size: 14px;">
                    <p style="margin-bottom: 8px;">&copy; 2024 ServiceBook. All rights reserved.</p>
                    <p>
                        <a href="#" style="color: #000000; text-decoration: underline;">Unsubscribe</a> from our emails
                    </p>
                </div>
            </div>
        </div>
    </div>
</body>
"""

# Example OTP value
global otp_value
otp_value = ''

# generate an 6-digit OTP value
# also get current utc time so that the otp gets expired after 5 minutes
def generate_otp():
    global otp_value
    otp_value = random.randint(100000, 999999)
    # get current utc time
    utc = datetime.datetime.now(datetime.UTC)
    return otp_value , utc

# Replace the placeholder with the actual OTP value
# formatted_otp_html = OTP_HTML.format(otp_value)

# print(formatted_otp_html)
payload_schema = {
    "sender": {
        "name": "Web2app-Support",
        "email": "no-reply@myshop.com"
    },
    "to": [
        {
            "email": 'some0ne@az.com',
            "name": "Recipient's Name"
        }
    ],
    "subject": "Greetings!",
    "htmlContent": OTP_HTML
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": api
}

def verify_Token(token):...

def content(link: str) -> str:
    # html_=html_content
    # dynamic_link = link
    html_ = OTP.format(link)
    # print(html_)
    return html_

def send_mail(open_link :str,name :str,email :str) ->int:
    '''Sends ```OTP``` to the user's email address'''
    # prepare link:
    ## get with JWT ....

    global otp_value

    payload = payload_schema.copy()
    payload["htmlContent"] = content(open_link)
    # name-email:
    payload_ = lambda email,name: payload["to"][0].update({"email":email,'name':name})
    payload_(name=name,email=email)

    response = requests.post(url, json=payload, headers=headers)

    try:
        if response.status_code == 201:
            print("Greetings message sent successfully to:",email)
            return response.status_code
        else:
            print("Failed to send greetings message. Status code:", response.status_code)
            print(response.text)
            return response.status_code
    except Exception as e:
        print(e)
        return response.status_code
    finally:
        otp_value = None

def send_otp_mob(number:str,otp:int) ->int:
    '''Sends ```OTP``` to the user's mobile number'''
    # as api accepts only 6-digit otp and number in int
    # send otp to the user's mobile number
    _ = requests.get(url=otp_url+f"?authorization={otp_api}&route=otp&variables_values={otp}&flash=0&numbers={int(number)}&schedule_time=")
    print(_.text)
    return _.status_code


# payload_('r@125','roy')
# print(payload)
# html-content:

# print(send_mail(name='LambdaX',email="rsnehasish125@gmail.com",open_link=otp_value))
# print(OTP_HTML.format('123456'))
# print(generate_otp())