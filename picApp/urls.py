from django.urls import path
from .views import  who, remove_verified,feedback, delete_complaint, verify_found_persons, search_missing_person, submit_child, admin_dashboard, home, case_cart, verify_case, found_person, found_person_cart, verified_profile

urlpatterns = [
    path('submit/', submit_child, name="submit_child"),
    path('search/', search_missing_person, name="search_child"),
    path('', home, name="home"),
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),
    path('case_cart/', case_cart, name="cart"),
    path('verify_case/<int:case_id>/', verify_case, name="verify_case"),
    path('found_person/', found_person, name="found_person"),
    path('found_person_cart/', found_person_cart, name="found_person_cart"),
    path('verified_profile/', verified_profile, name="verified_profile"),
    path('verify_found_persons/<int:case_id>/', verify_found_persons, name="verify_found_persons"),
    path('delete/<int:copm_id>', delete_complaint, name="delete"),
    path('remove/<int:person_id>', remove_verified, name="remove"),
    path('feedback', feedback, name="feedback"),
    path('who', who, name="who"),
]
