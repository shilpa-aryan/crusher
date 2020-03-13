from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# local Django
from crusher_app.views import *

urlpatterns = [
    path("vehicle/registration/", VehicleCreateListAPIView.as_view()),
    path("vehicle/list/", VehicleCreateListAPIView.as_view(), name="vehicle-list"),
    path("vehicle/retrieve/<int:pk>/", VehicleRetrieveUpdateDestroyAPIView.as_view()),
    path("vehicle/edit/<int:pk>/", VehicleRetrieveUpdateDestroyAPIView.as_view()),
    path("vehicle/delete/<int:pk>/", VehicleRetrieveUpdateDestroyAPIView.as_view()),
    path("vehicle/search/", VehicleSearchAPIView.as_view()),
    path("driver/add/", AddDriver.as_view()),
    path("driver/list/", AddDriver.as_view()),
    path("driver/retrieve/<int:pk>/", RetrieveUpdateDeleteDriver.as_view()),
    path("driver/edit/<int:pk>/", RetrieveUpdateDeleteDriver.as_view()),
    path("driver/delete/<int:pk>/", RetrieveUpdateDeleteDriver.as_view()),
    path("driver/search/", SearchDriver.as_view(), name="search-driver"),
    path("hours/add/", HoursTrackingCreateListAPIView.as_view()),
    path("hours/list/", HoursTrackingCreateListAPIView.as_view()),
    path(
        "hours/retrieve/<int:pk>/",
        HoursTrackingRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("hours/edit/<int:pk>/", HoursTrackingRetrieveUpdateDestroyAPIView.as_view(),),
    path(
        "hours/delete/<int:pk>/", HoursTrackingRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path(
        "hours/retrieve/previous_reading/",
        HoursTrackingListOfPrevDataAPIView.as_view(),
    ),
    path("trip/add/", AddTrip.as_view()),
    path("trip/list/", AddTrip.as_view()),
    path("trip/retrieve/<int:pk>/", RetrieveUpdateDeleteTrip.as_view()),
    path("trip/edit/<int:pk>/", RetrieveUpdateDeleteTrip.as_view()),
    path("trip/delete/<int:pk>/", RetrieveUpdateDeleteTrip.as_view()),
    path("trip/drafts/", TripDraft.as_view()),
    path("production/add/", ProductionCreateList.as_view()),
    path("production/list/", ProductionCreateList.as_view()),
    path("production/retrieve/<int:pk>/", ProductionRetrieveUpdateDestroy.as_view()),
    path("production/edit/<int:pk>/", ProductionRetrieveUpdateDestroy.as_view()),
    path("production/delete/<int:pk>/", ProductionRetrieveUpdateDestroy.as_view()),
    path("dayin/", DayIn.as_view()),
    path("check_user_type/", CheckUserType.as_view()),
    path('email-exist/', EmailCheckView.as_view()),
    path('assigned-driver/', VehicleAssigned.as_view()),




]


urlpatterns += staticfiles_urlpatterns()
