from django.urls import path, include
# from api.internal.transport.rest.equipment.handlers import EquipmentListByEmployeeView

urlpatterns = [
    path('auth/', include('api.auth.urls')),
    # path('admin/', include('api.admin_api.urls')),
    # path('employee/', include('api.employee_api.urls')),
    # path('employee/', include('api.internal.router.toggl')),
    #
    # path('equipment/', include('api.internal.router.equipment')),
    # path('equipment', EquipmentListByEmployeeView.as_view(), name='equipment by employee'),
    #
    # path('skills', include('api.internal.router.skills')),
    # path('', include('api.internal.router.employee')),
    # path('projects/', include('api.internal.router.project')),
]
