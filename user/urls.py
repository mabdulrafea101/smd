from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from . import views
# from django.contrib.auth.forms import AuthenticationForm
from .forms import MyLoginForm

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="user/login.html",
            authentication_form=MyLoginForm,
        ),
        name="login_url",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            template_name="user/logout.html", next_page=reverse_lazy("login_url")
        ),
        name="logout_url",
    ),
    path("signup/admin/", views.signup_admin, name="signup-admin"),
    path("signup/manager/", views.signup_manager, name="signup-manager"),
    path(
        "signup/inventory-manager/",
        views.signup_inventory_manager,
        name="signup-inventory-manager",
    ),
    path("signup/staff/", views.signup_staff, name="signup-staff"),
    path("list/", views.get_user_list, name="user-list"),
    path("<int:pk>/edit/", views.get_user_list, name="user-edit"),
    path("<int:pk>/activate/", views.activate_user, name="user-activate"),
    path("<int:pk>/deactivate/", views.deactivate_user, name="user-deactivate"),
    path("active/list", views.user_active_list, name="user-active-list"),
    path("blocked/list", views.user_blocked_list, name="user-deactive-list"),
    path("distributor/", views.PurchaserList.as_view(), name="purchaser-list"),
    path("distributor/add/", views.PurchaserAddView.as_view(), name="purchaser-add"),
    path("distributor/edit/<int:pk>", views.PurchaserUpdate.as_view(), name="purchaser-edit"),
    path("distributor/delete/<int:pk>", views.PurchaserDelete.as_view(), name="purchaser-delete"),
    path("customer/", views.CustomerList.as_view(), name="customer-list"),
    path("customer/add/", views.CustomerAddView.as_view(), name="customer-add"),
    path("customer/edit/<int:pk>", views.CustomerUpdate.as_view(), name="customer-edit"),
    path("customer/delete/<int:pk>", views.CustomerDelete.as_view(), name="customer-delete"),

]
