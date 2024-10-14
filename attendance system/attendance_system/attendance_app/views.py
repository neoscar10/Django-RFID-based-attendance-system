# 

# # Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Attendance
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('attendance')
    return render(request, 'login.html')

@login_required
def attendance_list_view(request):
    attendances = Attendance.objects.all()
    print(attendances)
    return render(request, 'attendance_list.html', {'attendances': attendances})

class RegisterCardView(APIView):
    def post(self, request, format=None):
        card_uid = request.data.get('card_uid')
        timestamp = request.data.get('timestamp')
        
        try:
            user = User.objects.get(card_uid=card_uid)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        attendance, created = Attendance.objects.get_or_create(user=user, timestamp=timestamp)
        if created:
            attendance.time_in = timezone.now()
            attendance.save()
            
        return Response({'message': 'Card UID registered successfully'}, status=status.HTTP_200_OK)


# class RegisterCardView(APIView):
#     def post(self, request, format=None):
#         card_uid = request.data.get('card_uid')
        
#         try:
#             user = User.objects.get(card_uid=card_uid)
#         except User.DoesNotExist:
#             return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         return Response({'message': 'Card UID registered successfully'}, status=status.HTTP_200_OK)



class AttendanceListView(APIView):
    def get(self, request, format=None):
        attendances = Attendance.objects.all()
        data = [{'user': attendance.user.name, 'timestamp': attendance.timestamp, 'time_in': attendance.time_in, 'time_out': attendance.time_out} for attendance in attendances]
        return JsonResponse(data, safe=False)
    



# class AttendanceListView(APIView):
#     def get(self, request, format=None):
#         attendances = Attendance.objects.all()
#         data = [{'user': attendance.user.name, 'timestamp': attendance.timestamp} for attendance in attendances]
#         return Response(data, status=status.HTTP_200_OK)

