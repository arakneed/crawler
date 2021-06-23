import pytest
from contextlib import asynccontextmanager
from pathlib import Path
import pathlib
import arakneed


@pytest.fixture
def web_task():
    return arakneed.Task('page', 'https://www.baidu.com')


class TestVisitWeb:

    async def test_visit_page(self, visitor, web_task):
        async with visitor.visit(web_task) as result:
            assert result.status == 200


class FsVisitor(arakneed.Visitor):

    @asynccontextmanager
    async def visit(self, task):
        async with self.fs(task.key) as result:
            yield result

    @asynccontextmanager
    async def fs(self, path):
        if not isinstance(path, pathlib.Path):
            if path.__fspath__ or isinstance(path, str):
                path = Path(path)
            else:
                raise arakneed.CrawlerError(TypeError('invalid path'))
        if not path.exists():
            raise arakneed.CrawlerError(ValueError('path not exists'))

        yield path


@pytest.fixture
def fs_visitor(config, cacher, logger):
    return FsVisitor(config, cacher=cacher, logger=logger)


@pytest.fixture
def fs_task(tmp_path):
    return arakneed.Task('fs', tmp_path)


class TestVisitFs:

    async def test_visit_path(self, fs_visitor, fs_task):
        file = fs_task.key / 'file.txt'
        file.touch()
        file.write_text('file')

        async with fs_visitor.visit(fs_task) as result:
            files = list(result.iterdir())
            assert files[0].read_text() == 'file'

    async def test_visit_legacy_path(self, fs_visitor, tmpdir):
        fs_task = arakneed.Task('fs', tmpdir)
        tmp_path = Path(tmpdir)
        file = tmp_path / 'file.txt'
        file.touch()
        file.write_text('file')

        async with fs_visitor.visit(fs_task) as result:
            files = list(result.iterdir())
            assert files[0].read_text() == 'file'
