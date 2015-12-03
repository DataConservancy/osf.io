from rest_framework import generics
from rest_framework import permissions as drf_permissions

from modularodm import Q

from framework.auth.oauth_scopes import CoreScopes

from website.models import Institution, Node, User

from api.base import permissions as base_permissions
from api.base.filters import ODMFilterMixin
from api.base.views import JSONAPIBaseView
from api.base.utils import get_object_or_error
from api.nodes.serializers import NodeSerializer, NodeDetailSerializer
from api.users.serializers import UserSerializer, UserDetailSerializer

from .serializers import InstitutionSerializer, InstitutionDetailSerializer


class InstitutionList(JSONAPIBaseView, generics.ListAPIView):
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.INSTITUTION_READ]
    required_write_scopes = [CoreScopes.NULL]
    model_class = Institution

    serializer_class = InstitutionSerializer
    view_category = 'institutions'
    view_name = 'institution-list'

    def get_queryset(self):
        return Institution.find()


class InstitutionDetail(JSONAPIBaseView, generics.RetrieveAPIView):
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.INSTITUTION_READ]
    required_write_scopes = [CoreScopes.NULL]
    model_class = Institution

    serializer_class = InstitutionDetailSerializer
    view_category = 'institutions'
    view_name = 'institution-detail'

    def get_object(self):
        inst = get_object_or_error(
            Institution,
            self.kwargs['institution_id'],
            display_name='institution'
        )
        return inst

class InstitutionNodeList(JSONAPIBaseView, ODMFilterMixin, generics.ListAPIView):
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.INSTITUTION_READ, CoreScopes.NODE_BASE_READ]
    required_write_scopes = [CoreScopes.NULL]
    model_class = Node

    serializer_class = NodeSerializer
    view_category = 'institutions'
    view_name = 'institution-nodes'

    def get_default_odm_query(self):
        inst = Institution.load(self.kwargs['institution_id'])
        query = Q('primary_institution', 'eq', inst)
        return query

    def get_queryset(self):
        query = self.get_query_from_request()
        return Node.find(query)

class InstitutionNodeDetail(JSONAPIBaseView, generics.RetrieveAPIView):
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.INSTITUTION_READ, CoreScopes.NODE_BASE_READ]
    required_write_scopes = [CoreScopes.NULL]
    model_class = Node

    serializer_class = NodeDetailSerializer
    view_category = 'institutions'
    view_name = 'institution-node-detail'

    def get_object(self):
        node = get_object_or_error(
            Node,
            self.kwargs['node_id'],
            display_name='node'
        )
        return node

class InstitutionUserList(JSONAPIBaseView, ODMFilterMixin, generics.ListAPIView):
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.INSTITUTION_READ, CoreScopes.USERS_READ]
    required_write_scopes = [CoreScopes.NULL]
    model_class = User

    serializer_class = UserSerializer
    view_category = 'institutions'
    view_name = 'institution-users'

    def get_default_odm_query(self):
        inst = Institution.load(self.kwargs['institution_id'])
        query = Q('affiliated_institutions', 'eq', inst)
        return query

    def get_queryset(self):
        query = self.get_query_from_request()
        return User.find(query)

class InstitutionUserDetail(JSONAPIBaseView, generics.RetrieveAPIView):
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
    )

    required_read_scopes = [CoreScopes.INSTITUTION_READ, CoreScopes.USERS_READ]
    required_write_scopes = [CoreScopes.NULL]

    serializer_class = UserDetailSerializer
    view_category = 'institutions'
    view_name = 'institution-user-detail'

    def get_object(self):
        user = get_object_or_error(
            User,
            self.kwargs['user_id'],
            display_name='user'
        )
        return user
