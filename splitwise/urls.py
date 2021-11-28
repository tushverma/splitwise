from django.urls import path, include
from rest_framework.routers import DefaultRouter
from splitwise import views

urlpatterns = [
    path('createGroup', views.CreateGroupApiView.as_view()),
    path('createExpense', views.CreateExpenseApiView.as_view()),
    path('createUser', views.UserProfileApiView.as_view()),
    path('addUserToGroup', views.AddUserToGroupApiView.as_view()),
    path('showGroupMembers', views.ShowGroupMembersApiView.as_view()),
    path('userDetails', views.ShowUserDetailsApiView.as_view()),
    path('addExpense', views.CreateExpenseApiView.as_view()),
    path('groupDetails', views.ShowGroupDetailsApiView.as_view()),
    path('deleteUser', views.DeleteUserApiView.as_view()),
    path('deleteGroup', views.DeleteGroupApiView.as_view()),
    path('recordPayment', views.RecordPaymentApiView.as_view()),
]
