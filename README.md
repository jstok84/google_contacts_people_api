# google_contacts_people_api
Google contacts with People API, my google contacts script edited to work with People API, you can compare this script with my older script which is based on Contacts API (Stopped working on 19th January 2022)

My script uses People API to get all data that I need from proper group

Prerequisites
To run this script you need the following prerequisites:

Python 2.6 or greater.
The pip package management tool
A Google Cloud Platform project with the API enabled. To create a project and enable an API, refer to Create a project and enable the API
Note: For this script, you are enabling the "People API".
https://developers.google.com/workspace/guides/create-project
Authorization credentials for a desktop application. To learn how to create credentials for a desktop application, refer to Create credentials.
https://developers.google.com/workspace/guides/create-credentials
A Google account.

Step 1: Install the Google client library
To install the Google client library for Python, run the following command:


  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
 
Step 2: Create project, you can use test account if you don't want to verify project
 https://developers.google.com/workspace/guides/create-project
 
 
Step 3: Crate credentials file (credentials.json) for desktop app. - When you download file, you need to rename it to: credentials.json in order for this script to work.
 https://developers.google.com/workspace/guides/create-credentials
 
Step 4: Run my script

#Note: If you have TypeError: ‘NoneType’ you essentialy need to check if field is not None: please see how it works with email address field.
