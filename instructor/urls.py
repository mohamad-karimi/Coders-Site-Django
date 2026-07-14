from django.urls import path, re_path
from instructor.views import IN_list, IN_single, instructor_search, dashboard, create_course, delete_account, edit_profile, add_lesson, add_section

app_name = "instructor"
urlpatterns = [
    path("list/", IN_list, name="instructor_list"),
    path("search/", instructor_search, name="instructor_search"),
    path("create-course/", create_course, name="create_course"),
    path("dashboard/", dashboard, name="dashboard"),
    path("delete-account/", delete_account, name="delete_account"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path('course/<int:course_id>/add-section/', add_section, name='add_section'),
    path('section/<int:section_id>/add-lesson/', add_lesson, name='add_lesson'),

    re_path(
        r"^(?P<slug>[-\w\u0600-\u06FF]+)/$",
        IN_single,
        name="instructor_single",
    ),
]