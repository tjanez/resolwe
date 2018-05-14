"""Resolwe collection serializer."""
from django.contrib.auth.models import AnonymousUser

from rest_framework import serializers

from resolwe.flow.models import Collection, DescriptorSchema
from resolwe.permissions.shortcuts import get_objects_for_user
from resolwe.rest.fields import ProjectableJSONField

from .base import ResolweBaseSerializer
from .data import DataSerializer
from .descriptor import DescriptorSchemaSerializer


class CollectionSerializer(ResolweBaseSerializer):
    """Serializer for Collection objects."""

    slug = serializers.CharField(read_only=False, required=False)
    settings = ProjectableJSONField(required=False)
    descriptor = ProjectableJSONField(required=False)

    class Meta:
        """CollectionSerializer Meta options."""

        model = Collection
        update_protected_fields = ('contributor',)
        read_only_fields = ('id', 'created', 'modified', 'descriptor_dirty')
        fields = ('slug', 'name', 'description', 'settings', 'descriptor_schema', 'descriptor',
                  'data') + update_protected_fields + read_only_fields

    def _serialize_data(self, data):
        """Return serialized data or list of ids, depending on `hydrate_data` query param."""
        if self.request and self.request.query_params.get('hydrate_data', False):
            serializer = DataSerializer(data, many=True, read_only=True)
            serializer.bind('data', self)
            return serializer.data
        else:
            return [d.id for d in data]

    def _filter_queryset(self, perms, queryset):
        """Filter object objects by permissions of user in request."""
        user = self.request.user if self.request else AnonymousUser()
        return get_objects_for_user(user, perms, queryset)

    def get_data(self, collection):
        """Return serialized list of data objects on collection that user has `view` permission on."""
        data = self._filter_queryset('view_data', collection.data.all())

        return self._serialize_data(data)

    def get_fields(self):
        """Dynamically adapt fields based on the current request."""
        fields = super(CollectionSerializer, self).get_fields()

        if self.request.method == "GET":
            fields['data'] = serializers.SerializerMethodField()
        else:
            fields['data'] = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

        if self.request.method == "GET":
            fields['descriptor_schema'] = DescriptorSchemaSerializer(required=False)
        else:
            fields['descriptor_schema'] = serializers.PrimaryKeyRelatedField(
                queryset=DescriptorSchema.objects.all(), required=False
            )

        return fields