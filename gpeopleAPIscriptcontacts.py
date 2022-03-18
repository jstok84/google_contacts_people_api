import os.path
import pickle
import logging
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from ldap3 import Server, Connection, ALL, MODIFY_ADD, MODIFY_REPLACE, MODIFY_DELETE
import time
start_time = time.time()

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s", level=logging.WARNING
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/contacts.other.readonly",
    "https://www.googleapis.com/auth/contacts",
]


def get_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds

def get_contacts(people_service, pageSize=100):
    request = people_service.connections().list(
        resourceName="people/me", pageSize=pageSize, personFields="relations,names,emailAddresses,phoneNumbers,memberships"
    )
    contacts = []
    while request is not None:
        response = request.execute()
        contacts.extend(response.get("connections", []))
        request = people_service.connections().list_next(request, response)
    return contacts


def get_contacts_with_name_and_phone_number(contacts):
    result = []
    for contact in contacts:
        if contact.get("names") and contact.get("phoneNumbers"):
            result.append(contact)
    return result

def main():
    creds = get_creds()

    people_api = build("people", "v1", credentials=creds)

    people_service = people_api.people()
    contacts = get_contacts(people_service=people_service)
    logger.info(f"Found {len(contacts)} contacts")

    valid_contacts = get_contacts_with_name_and_phone_number(contacts=contacts)
    logger.info(f'Found {len(valid_contacts)} contacts in "Contacts" with name and phone number')
    i=0

    for index, contact in enumerate(valid_contacts):
        memberships= contact.get("memberships")
        groupid=memberships[0].get("contactGroupMembership")["contactGroupId"]
        if(groupid=="4271963ndz335e4d2"):
            resource_name = contact.get("resourceName")
            names = contact.get("names")
            ident=names[0].get("metadata")["source"]["id"];
            title=names[0].get("displayName")
            surname=names[0].get("familyName")
            if not(surname):
                surname="Some generic surname"
            name=names[0].get("givenName")
            phone_numbers = contact.get("phoneNumbers")
            telnum=phone_numbers[0].get("canonicalForm")
            typerel=phone_numbers[0].get("type")
            mailtmp=contact.get("emailAddresses")
            
            if typerel == 'work':
                pager=telnum[-3:]
                if mailtmp is not None:
                    mail=mailtmp[0].get("value")
            if typerel == 'mobile':
                gecos='*#'+telnum[-3:]
                if mailtmp is not None:
                    mail=mailtmp[0].get("value")
            if not (typerel):
                if mailtmp is not None:
                    mail=mailtmp[0].get("value")
                    
            logger.info(f'{i + 1}. Copying {names[0].get("displayName")} (Resource name: {resource_name})')
            i=i+1

if __name__ == "__main__":
    main()
print("--- %s seconds ---" % (time.time() - start_time))
time.sleep(10)
