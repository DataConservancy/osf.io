from nose.tools import *  # flake8: noqa

from website.project.metadata.schemas import LATEST_SCHEMA_VERSION
from website.project.model import ensure_schemas

from api.base.settings.defaults import API_BASE

from tests.base import ApiTestCase
from osf_tests.factories import (
    AuthUserFactory
)


class TestMetaSchemaList(ApiTestCase):
    def setUp(self):
        super(TestMetaSchemaList, self).setUp()
        self.user = AuthUserFactory()
        ensure_schemas()
        self.url = '/{}metaschemas/'.format(API_BASE)

    def test_pass_authenticated_user_can_view_schemas(self):
        res = self.app.get(self.url, auth=self.user.auth)
        assert_equal(res.status_code, 200)

    def test_cannot_update_metaschemas(self):
        res = self.app.put_json_api(self.url, auth=self.user.auth, expect_errors=True)
        assert_equal(res.status_code, 405)

    def test_cannot_post_metaschemas(self):
        res = self.app.post_json_api(self.url, auth=self.user.auth, expect_errors=True)
        assert_equal(res.status_code, 405)

    def test_schemas_are_latest_versions(self):
        res = self.app.get(self.url, auth=self.user.auth)
        assert_equal(res.status_code, 200)
        for schema in res.json['data']:
            assert_equal(schema['attributes']['schema_version'], LATEST_SCHEMA_VERSION)

    def test_pass_unauthenticated_user_can_view_schemas(self):
        res = self.app.get(self.url)
        assert_equal(res.status_code, 200)
