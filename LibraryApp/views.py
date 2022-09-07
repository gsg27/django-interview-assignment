from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.admin.views.decorators import staff_member_required

from .serializer import BookLibrarianSerializer, BookSerializer, UserSerializer,SearchSerializer
from .models import Books, User


class UserCreate(CreateAPIView):
    """
    Create a user with the given credentials and assign role of Librarian or Member based on value of is_librarian or is_member.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class MemberList(APIView):
    """
    Returns a list of members. Only available to Librarians.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_librarian:
            users = User.objects.filter(is_member=True)
            serializer = UserSerializer(users, many=True)
            return Response({"members": serializer.data})
        else:
            return Response(status=401)


class BookList(APIView):
    """
    Returns a list of books.
    Returns only name and availability of books when requested by members.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_librarian:
            books = Books.objects.all()
            serializer = BookLibrarianSerializer(books, many=True)
            return Response({"books": serializer.data})
        elif request.user.is_member:
            books = Books.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response({"books": serializer.data})
        else:
            return Response(status=401)


class BooksAdd(CreateAPIView):
    """
    Add book with given name in the system. Only available to Librarians.
    """
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        if request.user.is_librarian:
            name = request.data['name']
            try:
                Books.objects.create(name=name, added_by=request.user)
                return Response(status=201)
            except:
                return Response(status=400)

        else:
            return Response(status=401)


class BooksUpdate(APIView):
    # queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve a book with given id.
        """

        book = get_object_or_404(Books,pk=pk)

        if request.user.is_librarian:
            serializer = BookLibrarianSerializer(book)
            return Response({'book': serializer.data})
        elif request.user.is_member:
            serializer = BookSerializer(book)
            return Response({'book': serializer.data})
        else:
            return Response(status=401)
        

    def put(self, request, pk, *args, **kwargs):
        """
        Update details of a book with given id. Only for Librarians.
        """

        if request.user.is_librarian:
            name = request.data['name']
            book = get_object_or_404(Books,pk=pk)
            book.name = name
            book.save()
        else:
            return Response(status=401)



    def delete(self, request, pk, format=None):
        """
        Delete a book with given id. Only for Librarians.
        """
        if request.user.is_librarian:
            get_object_or_404(Books,pk=pk).delete()
        else:
            return Response(status=401)


class SearchBookList(APIView):
    """
    Returns a list of books matching the search term.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SearchSerializer

    def post(self, request):
        name = request.data['search']
        if request.user.is_librarian:
            books = Books.objects.filter(name__icontains=name)
            serializer = BookLibrarianSerializer(books, many=True)
            return Response({"books": serializer.data})
        elif request.user.is_member:
            books = Books.objects.filter(name__icontains=name)
            serializer = BookSerializer(books, many=True)
            return Response({"books": serializer.data})
        else:
            return Response(status=401)

class BorrowBook(APIView):
    """
    Borrow the book with given id.
    """
    permission_classes = (IsAuthenticated,)

    def post(self,request,pk):
        if request.user.is_member:
            book = get_object_or_404(Books,pk=pk)
            if book.is_borrowed:
                return Response(data='Book is already borrowed',status=409)
            else:

                book.borrowed_by = request.user
                book.is_borrowed = True
                book.save()
                return Response(status=200, data='Book borrowed successfully')
        else:
            return Response(status=401,data='Only members can borrow books')

class ReturnBook(APIView):
    """
    Return borrowed book with given id.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        if request.user.is_member:

            book = get_object_or_404(Books,pk=pk,borrowed_by=request.user)
            # book = Books.objects.get(pk=pk,borrowed_by=request.user)
            book.is_borrowed = False
            book.borrowed_by = None
            book.save()
            return Response(status=200, data='Book returned successfully')

        else:
            return Response(status=401)

class DeleteMyAccount(APIView):
    """
    Delete your member account. Return any borrowed books before deleting.
    """
    permission_classes = (IsAuthenticated,)


    def delete(self, request,confirm_username):
        if request.user.is_member:
            if  Books.objects.filter(borrowed_by=request.user).count() > 0:
                return Response(status=409, data='You have borrowed books. Return borrowed books before deleting.')
            elif request.user.username == confirm_username:
                get_object_or_404(User,username=request.user.username).delete()
                return Response(status=200, data='User deleted successfully')
            else:
                return Response(status=400, data='username does not match.')
        else:
            return Response(status=401, data='Only members can delete their own account.')

class BorrowedBooksList(APIView):
    """
    Return a list of borrowed books.
    """
    permission_classes= (IsAuthenticated,)


    def get(self, request):
        if request.user.is_member:

            books = Books.objects.filter(borrowed_by=request.user)
            serializer = BookSerializer(books, many=True)
            return Response({"books": serializer.data})

class MembersUpdate(APIView):
    # queryset = Books.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, username, *args, **kwargs):
        """
        Retrieve a member with given username.
        """

        user = get_object_or_404(User,username=username,is_member=True)

        if request.user.is_librarian:
            serializer = UserSerializer(user)
            return Response({'user': serializer.data})
        else:
            return Response(status=401)
        

    def put(self, request, username, *args, **kwargs):
        """
        Update details of a member with given username. Only for Librarians.
        """

        if request.user.is_librarian:
            member = get_object_or_404(User,username=username)
            member.username = request.data['username']
            member.is_librarian = request.data['is_librarian']
            member.is_member = request.data['is_member']
            member.save()
        else:
            return Response(status=401)



    def delete(self, request, username, format=None):
        """
        Delete a member with given username. Only for Librarians.
        """
        if request.user.is_librarian:
            get_object_or_404(User,username=username).delete()
        else:
            return Response(status=401)