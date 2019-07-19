# Copyright 2017 The BEGAN-tensorflow Authors(Taehoon Kim). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import requests
import zipfile
import os
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    path = './assets' 
    if not os.path.exists(path):
        os.makedirs(path)
    
    print('Download classification models ...')
    file_id = '1dlJ9SwmQTwyaVfEEEi6bf0AqaGrktkb0'
    destination = './assets/weight.zip'
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination) as zf:
        zip_dir = zf.namelist()[0]
        zf.extractall('./assets')
    os.remove(destination)

    file_id = '1jXyobZjOn8_2XD6mlLJvMG0nyLVFPhHf'
    destination = './assets/weight.zip'
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination) as zf:
        zip_dir = zf.namelist()[0]
        zf.extractall('./assets')
    os.remove(destination)


    file_id = '1hMf83Fs6j2T4wmSXqPIy4hXBpOdpAri8'
    destination = './assets/weight.zip'
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination) as zf:
        zip_dir = zf.namelist()[0]
        zf.extractall('./assets')
    os.remove(destination)


    file_id = '1yBOFkjy0wua7xtua4rSn4fz6aDvNSeeQ'
    destination = './assets/weight.zip'
    download_file_from_google_drive(file_id, destination)
    with zipfile.ZipFile(destination) as zf:
        zip_dir = zf.namelist()[0]
        zf.extractall('./assets')
    os.remove(destination)


    