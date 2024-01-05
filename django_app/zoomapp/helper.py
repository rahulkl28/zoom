from zoomus import ZoomClient
import os
import jwt
import time

CLIENT_ID = os.environ.get("ZOOM_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("ZOOM_CLIENT_SECRET", "")
ACCOUNT_ID = os.environ.get("ZOOM_ACCOUNT_ID", "")

def create_zoom_meeting(payload):
    client = ZoomClient(CLIENT_ID, CLIENT_SECRET,   api_account_id=ACCOUNT_ID)
    response = client.meeting.create(**payload)
    return response.json()

def create_auth_signature(meeting_no, role):
    ZOOM_SDK_CLIENT_ID = os.environ.get("ZOOM_SDK_ACC_ID", "")
    ZOOM_SDK_CLIENT_SECRET = os.environ.get("ZOOM_SDK_ACC_SECRET", "")
    
    iat = int(time())
    exp = iat + 60 * 60 * 1  # expire after 1 hour
    oHeader = {"alg": 'HS256', "typ": 'JWT'}
    oPayload = {
        "sdkKey": ZOOM_SDK_CLIENT_ID,
        "mn": int(meeting_no),
        "role": role,
        "iat": iat,
        "exp": exp,
        "tokenExp": exp
    }

    jwtEncode = jwt.encode(
        oPayload,
        ZOOM_SDK_CLIENT_SECRET,
        algorithm="HS256",
        headers=oHeader,
    )
    return {'token': jwtEncode, 'sdkKey': ZOOM_SDK_CLIENT_ID}