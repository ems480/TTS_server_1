from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Setup authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # first time only, follow browser login
drive = GoogleDrive(gauth)

def upload_file_to_drive(local_file, title):
    file_drive = drive.CreateFile({'title': title})
    file_drive.SetContentFile(local_file)
    file_drive.Upload()
    
    # Make the file public and get the link
    file_drive.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })

    return file_drive['alternateLink']
