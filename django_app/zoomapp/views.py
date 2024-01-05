from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .helper import create_zoom_meeting
from datetime import datetime
from rest_framework import status
from .helper import create_auth_signature


# /api/meeting/create # to create a meeting
# /api/meeting/authorize # to authorize as Zoom user on the client side



class ScheduleMeetingView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        payload = request.data
        topic = payload['topic']  # Max 100 chars
        agenda = payload['agenda']  # Max 200 chars
        start_time = payload['start_time']  # %Y-%m-%d %H:%M
       
        data = {
            'topic': topic,
            'agenda': agenda,
            'start_time': datetime.strptime(start_time, "%Y-%m-%d %H:%M"),
            'type': 2,
            # The type of meeting.
            #     1 - An instant meeting.
            #     2 - A scheduled meeting. (this)
            #     3 - A recurring meeting with no fixed time.
            #     8 - A recurring meeting with fixed time.
            'user_id': "me"  # For user-level apps, pass the me value.
        }
        response = create_zoom_meeting(data)
        # Store the response in the database for future reference.
        return Response({"message": "Meeting scheduled", 'res': response}, status.HTTP_201_CREATED)
    
class MeetingAuthorizationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        payload = request.data
        meeting_no = payload.get('meeting_no', None)
        role = payload.get('role', None)

        if meeting_no is None or role is None:
            return Response({"error": "Invalid payload"}, status.HTTP_400_BAD_REQUEST)

        # find the meeting details saved in the database
        password = "db.meeting.password"
        response = create_auth_signature(meeting_no, role)
        response['meeting_no'] = meeting_no
        response['password'] = password
        return Response(response, status.HTTP_200_OK)
