from django.test import TestCase, Client
from .models import Query


class TextViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.query = Query.objects.create(
            name="test",
            data="TESTESTEST",
            slug="test-1"
        )

    def test_get_homepage(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_add_query(self):
        response = self.client.get('/queries/')
        q = Query.objects.get(id=1)

        self.assertEquals(len(response.context['queries']), 1)
        self.assertEquals(q.name, 'test')
        self.assertEqual(q, self.query)

    def test_delete_query(self):
        response = self.client.get('/queries/')
        q = Query.objects.get(id=1)

        self.assertEquals(len(Query.objects.all()), 1)
        q.delete()
        self.assertEquals(len(Query.objects.all()), 0)

    def test_filter_by_target(self):
        Query.objects.create(
            name="test2",
            data="TESTESTEST2",
            slug="test-2"
        )
        Query.objects.create(
            name="test3",
            data="TESTESTEST3",
            slug="test-3"
        )

        response = self.client.get('/queries/', {'type': '', 'date': '', 'status': '',
                                                 'start_date': '', 'end_date': '', 'target': 'test2'})
        self.assertEquals(len(response.context['queries']), 1)
        self.assertEquals(str(response.context['queries'][0]), "TESTESTEST2")

    def test_bad_filter_by_target(self):
        Query.objects.create(
            name="test2",
            data="TESTESTEST2",
            slug="test-2"
        )
        Query.objects.create(
            name="test3",
            data="TESTESTEST3",
            slug="test-3"
        )

        response = self.client.get('/queries/', {'type': '', 'date': '', 'status': '',
                                                 'start_date': '', 'end_date': '', 'target': 'notest'})
        self.assertEquals(len(response.context['queries']), 0)

    def test_query_detail(self):
        response = self.client.get('/queries/test-1', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'queries/query_detail.html')

    def test_bad_query_detail(self):
        try:
            self.client.get('/queries/test-1', follow=True)
        except Exception:
            self.assertTrue(True)