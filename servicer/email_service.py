from __future__ import print_function

import base64
import os.path
import traceback

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from servicer.constants import EMAIL_SCOPE, Action
import config
from servicer.struct import EmailData
from utils import convert_datetime, read_and_decrypt, encrypt_and_save


class EmailService:
    def __init__(self):
        self.creds = self.generate_token()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def generate_token(self):
        creds = None
        if os.path.exists('token.json'):
            tokens = read_and_decrypt("token.json")
            creds = Credentials.from_authorized_user_info(tokens, EMAIL_SCOPE)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                account_credentials = self.get_account_credentials()
                flow = InstalledAppFlow.from_client_config(account_credentials, EMAIL_SCOPE)
                creds = flow.run_local_server(port=0)
            encrypt_and_save(creds.to_json(), 'token.json')
        return creds

    @staticmethod
    def get_account_credentials():
        return {
            "installed": {
                "client_id": config.CLIENT_ID,
                "project_id": config.PROJECT_ID,
                "auth_uri": config.AUTH_URI,
                "token_uri": config.TOKEN_URI,
                "auth_provider_x509_cert_url": config.AUTH_PROVIDER_X509_CERT_URL,
                "client_secret": config.CLIENT_SECRET,
                "redirect_uris": [config.REDIRECT_URIS]
            }
        }

    # we are run this function using asyncio/multithreading as this is a IO bound process
    def fetch_emails(self, limit=1000):
        result = self.service.users().messages().list(userId='me').execute()
        messages = result.get('messages')
        parsed_email_count = 0
        for msg in messages:
            txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            try:
                payload = txt['payload']
                headers = payload['headers']
                body = subject = from_address = to_address = ""
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        from_address = d['value']
                    if d['name'] == 'Delivered-To':
                        to_address = d['value']
                    if d['name'] == 'Date':
                        received_date = convert_datetime(d['value'])

                try:
                    if payload.get('parts') is not None:
                        parts = payload.get('parts')[0]
                        data = parts['body']['data']
                        data = data.replace("-", "+").replace("_", "/")
                        body = base64.b64decode(data)
                except Exception:
                    print("failed to parse body")

                yield EmailData(
                    message_id=msg['id'],
                    email_body=body,
                    received_date=received_date,
                    subject=subject,
                    to_address=to_address,
                    from_address=from_address,

                )
                parsed_email_count += 1
                if parsed_email_count > limit:
                    return
            except Exception as ex:
                traceback.print_exc()
                print("failed to parse email Error:", ex)
            else:
                print("email is parsed")

    def execute_action(self, action: Action, message_ids: list[str]):
        if action in [Action.MARK_READ, Action.MARK_UNREAD]:
            self._action_update_read_status(action, message_ids)
        elif action in [Action.MOVE_SPAM, Action.MOVE_TRASH]:
            self._move_emails(action, message_ids)

    def _action_update_read_status(self, action: Action, message_ids: list[str]):
        # Todo: handle scenario where email is already marked
        if action == Action.MARK_READ:
            status_body = {'removeLabelIds': ['UNREAD']}
        else:
            status_body = {'removeLabelIds': ['READ']}
        for message_id in message_ids:
            self.service.users().messages().modify(userId='me', id=message_id, body=status_body).execute()

    def _move_emails(self, action: Action, message_ids: list[str]):
        # Todo: handle scenario where email is not in Inbox
        for message_id in message_ids:
            self.service.users().messages().modify(
                userId='me', id=message_id, body={'addLabelIds': [action.value]}
            ).execute()
