

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



from .views import  BorrowBook, SearchBookList, UserCreate, MemberList, BooksAdd, BookList,BooksUpdate

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('user/register/',UserCreate.as_view(), name="register"),
    path('members/',MemberList.as_view(),name='users'),

    path('books/add',BooksAdd.as_view(),name='add_book'),
    path('books/',BookList.as_view(),name='list_books'),
    path('books/<int:pk>/',BooksUpdate.as_view(),name='update_book'),
    path('books/search/',SearchBookList.as_view(), name='search_book'),
    path('books/<int:pk>/borrow/', BorrowBook.as_view(), name='borrow_book'),

]
