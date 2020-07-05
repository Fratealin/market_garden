#TODO: this allows for if there is no config file
try:
    from market_garden import config
except:
    pass
import smtplib

def send_email(message, email, subject =""):
    myAddress = config.email_address
    #recipient = email
    receiverAddress = (myAddress, config.yahoo_address)
    # create smtp object. This creates a connection to the smtp mail server. Use this to call methods to login and send emails
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    # must call this to establish connection to server. First item in tuple is 250. Success.
    smtpObj.ehlo()
    # You are connecting to port 587. Using standard TLS encryption. So need to enable encryption. 220 = success:
    smtpObj.starttls()
    # log in
    smtpObj.login(config.email_address, config.password)

    # send email
    smtpObj.sendmail(myAddress, receiverAddress,
                     f"Subject: {subject}.\n{message}\nThanks from all at Picked")
    # logout
    smtpObj.quit()


def order_received_message(current_user):

    message = f"Hi {current_user.username}\n\tPlease take note of your pickup time\n{current_user.box_size}\n{current_user.pickup_time} Thursday \n{current_user.address}"
    return message

def new_order_message(current_user, vegbox_orders):
    message = f"Hi Picked\n\tNew veg box order received from: {current_user.username}\n{current_user.box_size}\n{current_user.pickup_time} Thursday\n{current_user.address}\nHere is a list of all your current orders.\n{vegbox_orders}"
    return message