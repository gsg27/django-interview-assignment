from django.shortcuts import render
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
        try:
            book = Books.objects.get(pk=pk)
            if request.user.is_librarian:
                serializer = BookLibrarianSerializer(book)
                return Response({'book': serializer.data})
            elif request.user.is_member:
                serializer = BookSerializer(book)
                return Response({'book': serializer.data})
            else:
                return Response(status=401)
        except:
            return Response(status=400)

    def put(self, request, pk, *args, **kwargs):
        """
        Update details of a book with given id.
        """
        try:
            if request.user.is_librarian:
                name = request.data['name']
                book = Books.objects.get(pk=pk)
                book.name = name
                book.save()
            else:
                return Response(status=401)
        except:
            return Response(status=400)


    def delete(self, request, pk, format=None):
        """
        Delete a book with given id.
        """
        if request.user.is_librarian:
            try:
                Books.objects.get(pk=pk).delete()
                return Response(status=200,)
            except:
                return Response(status=400)

        else:
            return Response(status=401)


class SearchBookList(APIView):
    """
    Returns a list of books matching the search term.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SearchSerializer

    def post(self, request):
        if request.user.is_librarian:
            name = request.data['search']
            books = Books.objects.filter(name__icontains=name)
            serializer = BookLibrarianSerializer(books, many=True)
            return Response({"books": serializer.data})
        elif request.user.is_member:
            name = request.data['search']
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
            book = Books.objects.get(pk=pk)
            if book.is_borrowed:
                return Response(data='Book is already borrowed',status=409)
            else:

                book.borrowed_by = request.user
                book.is_borrowed = True
                book.save()
                return Response(status=200)
        else:
            return Response(status=401,data='Only members can borrow books')
