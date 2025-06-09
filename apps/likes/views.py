from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Like
from .serializers import LikeSerializer
from apps.findings.models import Finding
from apps.publications.models import Publication
from apps.comments.models import Comment


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_finding(request, pk):
    """Like a finding"""
    finding = get_object_or_404(Finding, id=pk, is_active=True)

    like, created = Like.objects.get_or_create(
        user=request.user,
        finding=finding
    )

    if not created:
        return Response(
            {'detail': 'Already liked'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_finding(request, pk):
    """Unlike a finding"""
    finding = get_object_or_404(Finding, id=pk, is_active=True)

    try:
        like = Like.objects.get(user=request.user, finding=finding)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response(
            {'detail': 'Not liked yet'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_publication(request, pk):
    """Like a publication"""
    publication = get_object_or_404(Publication, id=pk, is_active=True)

    like, created = Like.objects.get_or_create(
        user=request.user,
        publication=publication
    )

    if not created:
        return Response(
            {'detail': 'Already liked'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_publication(request, pk):
    """Unlike a publication"""
    publication = get_object_or_404(Publication, id=pk, is_active=True)

    try:
        like = Like.objects.get(user=request.user, publication=publication)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response(
            {'detail': 'Not liked yet'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, pk):
    """Like a comment"""
    comment = get_object_or_404(Comment, id=pk, is_active=True)

    like, created = Like.objects.get_or_create(
        user=request.user,
        comment=comment
    )

    if not created:
        return Response(
            {'detail': 'Already liked'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_comment(request, pk):
    """Unlike a comment"""
    comment = get_object_or_404(Comment, id=pk, is_active=True)

    try:
        like = Like.objects.get(user=request.user, comment=comment)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response(
            {'detail': 'Not liked yet'},
            status=status.HTTP_400_BAD_REQUEST
        )
