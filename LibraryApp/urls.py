

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



from .views import  BorrowBook, MemberAdd, MembersUpdate, ReturnBook, SearchBookList, UserCreate, MemberList, BooksAdd, BookList,BooksUpdate,DeleteMyAccount, BorrowedBooksList

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('user/register/',UserCreate.as_view(), name="register"),
    path('members/',MemberList.as_view(),name='members'),
    path('members/add/',MemberAdd.as_view(),name='add_member'),
    path('member/<str:username>/', MembersUpdate.as_view(),name='update_member'),
    path('delete_my_account/<str:confirm_username>/', DeleteMyAccount.as_view(),name='delete_my_account'),

    path('books/add/',BooksAdd.as_view(),name='add_book'),
    path('books/',BookList.as_view(),name='list_books'),
    path('book/<int:pk>/',BooksUpdate.as_view(),name='update_book'),
    path('books/search/',SearchBookList.as_view(), name='search_book'),
    path('book/<int:pk>/borrow/', BorrowBook.as_view(), name='borrow_book'),
    path('book/<int:pk>/return/', ReturnBook.as_view(), name='return_book'),
    path('books/borrowed/',BorrowedBooksList.as_view(),name='borrowed_books'),

]
