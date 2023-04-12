import datetime
from io import BytesIO
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.base import ContentFile
import base64
from django.core.files.uploadedfile import InMemoryUploadedFile



class RegisterAPI(generics.GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print('ffff',user)
         
        # token = Token.objects.get_or_create(user=user)
        # print('asdasdasdasd',token.key)
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            # "token": Token.objects.create(user).key
        })

class LoginAPI(generics.GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'})
        return Response({
            "user": CustomUserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.create(user=user).key
        })


class PublisherView(ListAPIView):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()
    permission_classes = [IsAuthenticated]



class ArcticleList(ListAPIView):
    queryset = Arcticle.objects.all()
    serializer_class = ArcticleSerializer


class ArcticleCreateAPIView(generics.CreateAPIView):
    queryset = Arcticle.objects.all()
    serializer_class = ArcticleCreateSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        request.data['author_id'] = request.user.id
        return super().create(request, *args, **kwargs)




class ArcticleDetail(generics.RetrieveAPIView):
    queryset = Arcticle.objects.all()
    serializer_class = ArcticleSerializer

class CommentsCreateView(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

class CommentsList(ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer


class ArcticleCommentsList(generics.ListAPIView):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        queryset = Comments.objects.filter(arcticle__id=self.kwargs['pk'])
        return queryset

class LikeListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Like.objects.all()
        user_id = self.request.query_params.get('user', None)
        arcticle_id = self.request.query_params.get('arcticle', None)
        if user_id is not None:
            queryset = queryset.filter(user=user_id)
        if arcticle_id is not None:
            queryset = queryset.filter(arcticle=arcticle_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
def create_like(request):
    user_id = request.data.get('user_id')
    arcticle_id = request.data.get('arcticle_id')
    if not user_id or not arcticle_id:
        return Response({'error': 'Both user_id and article_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        like = Like.objects.create(user_id=user_id, arcticle_id=arcticle_id)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteLike(APIView):
    print('fdsfsdfsdfsdf')
    def delete(self, request, pk):
        arcticle = get_object_or_404(Arcticle, pk=pk)
        print('IDDDD', arcticle)
        user = request.data.get('user_id')
        print('sdfsssss', user)
        like = Like.objects.filter(user_id=user, arcticle_id=arcticle).first()
        print('FMSKDNAJKNDAJKDNAD ',like)
        
        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Like not found."}, status=status.HTTP_404_NOT_FOUND)
        


class ProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,  )

    def post(self, request, *args, **kwargs):

        self.user = request.user
        data = request.data
        base64_image = request.data['profile_pic']
        image_data = base64.b64decode(base64_image)
        image_file = BytesIO(image_data)
        file_name = f'{datetime.datetime.now()}.jpg'
        file = InMemoryUploadedFile(image_file, None, file_name, 'image/jpeg', len(image_data), None)
        profile = Profile (
            user = request.user,
            bio = data['bio'],
            city = data['city'],
            instagram = data['instagram'],
            facebook = data['facebook'],
            twitter = data['twitter'],
            # status = False,
            profile_pic = file,
        )

        profile.save()


        return Response({'profile': ProfileSerializer(profile).data}, status=status.HTTP_201_CREATED)


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def put(self, request, *args, **kwargs):
        profile = self.get_object()

        # если есть изображение в запросе, декодируем его и создаем объект ContentFile
        profile_pic = request.data.get('profile_pic')
        if profile_pic:
            profile_pic_content = ContentFile(base64.b64decode(profile_pic))
            profile_pic_content.name = 'profile_pic.png'
            request.data['profile_pic'] = profile_pic_content

        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)