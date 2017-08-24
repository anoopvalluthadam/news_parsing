import os
import sys
import inspect
import pytest
import asyncio

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from db.np_mongodb import NPMongoDB # noqa


@pytest.mark.incremental
class TestMongoDB(object):
    @pytest.mark.asyncio
    async def test_single_insert(self, event_loop, db):
        # db = NPMongoDB(connect_string)
        data = {
            'authors': 'test_autor',
            'text': 'test_text',
            'date': 'test_date',
            'url': 'test_url',
            'tags': ['test_tags']
        }
        # result = await db.single_insert(data)
        result = asyncio.ensure_future(db.single_insert(data))
        print(result)
        await result
        assert result.result()

    @pytest.mark.asyncio
    async def test_in_search(self, db):
        result = asyncio.ensure_future(db.in_search(
            ['test_tags'], 'tags'
        ))
        await result
        print(result.result())

    @pytest.mark.asyncio
    async def test_teardown_method(self, db):
        result = asyncio.ensure_future(db.in_search(
            ['test_tags'], 'tags'
        ))
        await result
        assert result.result()
        id_ = (result.result()[0]['_id'])
        result = await db.db.posts.delete_many({'_id': id_})
        assert result.deleted_count
