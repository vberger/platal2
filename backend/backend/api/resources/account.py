from django import http
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response


from platal.auth import models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = ['hruid', 'full_name', 'sex']
        read_only_fields = fields


class AccountViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AccountSerializer
    lookup_field = 'hruid'

    def get_queryset(self):
        qs = models.Account.objects
        if not self.request.user.is_admin:
            qs = qs.filter(pk=self.request.user.pk)
        return qs

    @list_route()
    def me(self, request, *args, **kwargs):
        me = get_object_or_404(models.Account, pk=request.user.pk)
        serializer=self.get_serializer(me)
        return Response(serializer.data)
