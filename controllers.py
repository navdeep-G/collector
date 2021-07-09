from abc import ABC
from concurrent.futures import ThreadPoolExecutor

import tornado.web
from tornado.ioloop import IOLoop

from models import add_entry, validate_entries, get_entries, get_file_stream

_executor = ThreadPoolExecutor()


class AddFileHandler(tornado.web.RequestHandler, ABC):
    
    def initialize(self, path):
        self.path = path
        
    def get(self):
        """Renders the Add New File form.
        """
        return self.render(self.path, description='', errors=[])

    async def post(self):
        """Async handler for accepting file and storing it in DB.
        """
        entry = dict(
            description=self.get_body_argument('description'),
            file=self.request.files['file'][0] if 'file' in self.request.files else None
        )

        # Validate the file
        errors = validate_entries(entry)
        if len(errors) > 0:
            return self.render(
                'example/templates/add_entry.html',
                errors=errors,
                **entry
            )

        # Save the file
        success = await IOLoop.current().run_in_executor(
            _executor,
            add_entry,
            entry
        )
        if not success:
            errors.append('Opps! Something went wrong.')
            return self.render(
                'example/templates/add_entry.html',
                errors=errors,
                **entry
            )

        self.redirect('/')


class DescriptionHandler(tornado.web.RequestHandler, ABC):

    def initialize(self, path):
        self.path = path

    def get(self):
        """Renders the list of files."""
        return self.render(self.path, entries=get_entries())


class FileHandler(tornado.web.RequestHandler, ABC):
    async def get(self, name):
        """Serves the requested file."""
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', f'attachment; filename={name}.txt')
        for chunk in get_file_stream(name):
            self.write(chunk)
            await self.flush()
        self.finish()
