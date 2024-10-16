'''
Send-In-Blue: SMTP API
'''

import os
import requests  #tokenZ as tz
import datetime , random

api = os.environ.get('smtp_api')

url = "https://api.brevo.com/v3/smtp/email"

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
    html_ = OTP_HTML.format(link)
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


# payload_('r@125','roy')
# print(payload)
# html-content:

# print(send_mail(name='LambdaX',email="rsnehasish125@gmail.com",open_link=otp_value))
# print(OTP_HTML.format('123456'))
# print(generate_otp())