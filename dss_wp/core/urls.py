from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('input-nilai/<int:stakeholder_id>', views.input_nilai_view, name='input-nilai'),
    path('hasil-wp/<int:stakeholder_id>', views.hasil_wp_view, name='hasil-wp'),
    path('hasil-borda/', views.hasil_borda_view, name='hasil-borda'),
]