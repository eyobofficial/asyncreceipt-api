from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView, UserDetailsView
from rest_auth.registration.views import RegisterView
from rest_auth.app_settings import LoginSerializer, PasswordChangeSerializer, \
    PasswordResetSerializer, PasswordResetConfirmSerializer, UserDetailsSerializer
from rest_auth.registration.app_settings import RegisterSerializer

from rest_framework import status


login_view = swagger_auto_schema(
    operation_summary='Login a user',
    operation_description='''
        Check the credentials and return the REST Token if the credentials
        are valid and authenticated. Calls Django Auth login method to register
        User ID in Django session framework.
    ''',
    operation_id='user-login',
    methods=['POST'],
    tags=['User Accounts'],
    security=[],
    responses={
        status.HTTP_200_OK: LoginSerializer,
        status.HTTP_400_BAD_REQUEST: 'Username/Password is required.'
    }
)(LoginView.as_view())


logout_view = swagger_auto_schema(
    operation_summary='Logout authenticated user',
    operation_description='''
        Logout an authenticated user by deleting the Token object assigned to the
        current User object.

        **Note:** It accepts/returns nothing.
    ''',
    operation_id='user-logout',
    methods=['GET', 'POST'],
    tags=['User Accounts'],
    responses={
        status.HTTP_200_OK: 'Successfully logged out.'
    }
)(LogoutView.as_view())


password_change_view = swagger_auto_schema(
    operation_summary='Change user password',
    operation_description='''
        This endpoint changes the password of the current authenticated user.
    ''',
    operation_id='password-change',
    methods=['POST'],
    tags=['User Accounts'],
    responses={
        status.HTTP_200_OK: 'Password changed successfully.',
        status.HTTP_400_BAD_REQUEST: 'Password validation errors.',
        status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
    }
)(PasswordChangeView.as_view())


password_reset_view = swagger_auto_schema(
    operation_summary='Reset user password',
    operation_description='''
        This endpoint sends an email link to reset a password of a user account.
    ''',
    operation_id='password-reset',
    methods=['POST'],
    tags=['User Accounts'],
    security=[],
    responses={
        status.HTTP_200_OK: 'Password reset e-mail sent.',
        status.HTTP_400_BAD_REQUEST: 'Sending Password reset e-mail failed.'
    }
)(PasswordResetView.as_view())


password_reset_cofirm_view = swagger_auto_schema(
    operation_summary='Confirm password reset email',
    operation_description='''
        This endpoint confirms the password reset e-mail link to reset a
        password of a user account.
    ''',
    operation_id='password-reset-confirm',
    methods=['POST'],
    tags=['User Accounts'],
    security=[],
    responses={
        status.HTTP_200_OK: 'New password set.',
        status.HTTP_400_BAD_REQUEST: 'Setting new password failed.'
    }
)(PasswordResetConfirmView.as_view())


registration_view = swagger_auto_schema(
    operation_summary='Register a new user',
    operation_description='''
        This endpoint registers a new user account. It also sends an email that
        contains a verification link to activate the account.
    ''',
    operation_id='user-registration',
    methods=['POST'],
    tags=['User Accounts'],
    security=[],
    responses={
        status.HTTP_200_OK: RegisterSerializer,
        status.HTTP_400_BAD_REQUEST: 'Validation errors.'
    }
)(RegisterView.as_view())


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_id='user-detail',
        operation_summary='Get authenticated user detail',
        operation_description='''
            This endpoint returns all the model fields for the current authenticated
            User object.
        ''',
        tags=['User Accounts'],
        responses={
            status.HTTP_200_OK: UserDetailsSerializer,
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.'
        }
    )
)
@method_decorator(
    name='put',
    decorator=swagger_auto_schema(
        operation_id='user-update',
        operation_summary='Update authenticated user detail',
        operation_description='''
            This endpoint updates the model fields for the current authenticated
            User object.
        ''',
        tags=['User Accounts'],
        responses={
            status.HTTP_200_OK: UserDetailsSerializer,
            status.HTTP_400_BAD_REQUEST: 'Validation errors.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
            status.HTTP_403_FORBIDDEN: 'Permission denied.',
        }
    )
)
@method_decorator(
    name='patch',
    decorator=swagger_auto_schema(
        operation_id='user-edit',
        operation_summary='Edit authenticated user detail',
        operation_description='''
            This endpoint partially edit the model fields for the current authenticated
            User object.
        ''',
        tags=['User Accounts'],
        responses={
            status.HTTP_200_OK: UserDetailsSerializer,
            status.HTTP_400_BAD_REQUEST: 'Validation errors.',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized request.',
            status.HTTP_403_FORBIDDEN: 'Permission denied.',
        }
    )
)
class CustomUserDetailView(UserDetailsView):
    pass
