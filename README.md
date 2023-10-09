# GmailAutomation
Enable Oauth consent in you google cloud account using your gmail account
install all dependency using "pip3 install -r requirement.txt"
add 32 url-safe base64-encoded bytes string in environment variable this  will be use to encrypt data(tokens) so that they can be reused you can also generate this throught Fernet.generate_key()
generate credentials
Update these credentials in enviroment variable


you can script by running main file
if you want to run through flask web server comment first 2 lines in main.py and uncomment last time and then run main.py it wiLL start flask server
