from django.shortcuts import render
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.admin.views.decorators import staff_member_required

from .serializer import BookLibrarianSerializer, BookSerializer, UserSerializer
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


class BooksUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticated,)

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
    Returns a list of books.
    Returns only name and availability of books when requested by members.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_librarian:
            books = Books.objects.all()
            serializer = BookLibrarianSerializer(books, many=True)
            return Response({"books": serializer.data})
        # elif request.user.is_member:
        #     books = Books.objects.all()
        #     serializer = BookSerializer(books, many=True)
        #     return Response({"books": serializer.data})
        else:
            return Response(status=401)

