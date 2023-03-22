from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.serializers import ReviewSerializer, CommentSerializer
from api.permissions import IsAdminOrModeratorOrAuthorOnly

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Title


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrModeratorOrAuthorOnly
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrModeratorOrAuthorOnly
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user,
                        review=review)
