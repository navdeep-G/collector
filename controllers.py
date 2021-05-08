import os
from concurrent.futures import ThreadPoolExecutor

import tornado.web
from tornado.ioloop import IOLoop

from models import add_file, validate_file, get_files, get_log_stream

# It appears that the minio is not asyncio "compatible" - it would block
# So I use threading instead which should work fine since it is an IO-bound
# operation.
_executor = ThreadPoolExecutor()


class AddFileHandler(tornado.web.RequestHandler):
    def get(self):
        """Renders the Add New File form.
        """
        return self.render('templates/add_file.html', file='', errors=[])

    async def post(self):
        """Async handler for accepting file and storing it in DB.
        """
        file = dict(
            file=self.get_body_argument('file'),
            log=self.request.files['log'][0] if 'log' in self.request.files else None
        )

        # Validate the file
        errors = validate_file(file)
        if len(errors) > 0:
            return self.render(
                'templates/add_file.html',
                errors=errors,
                **file
            )

        # Save the file
        success = await IOLoop.current().run_in_executor(
            _executor,
            add_file,
            file
        )
        if not success:
            errors.append('Opps! Something went wrong.')
            return self.render(
                'templates/add_file.html',
                errors=errors,
                **file
            )

        self.redirect('/')


class FilesHandler(tornado.web.RequestHandler):
    def get(self):
        """Renders the list of files."""
        return self.render('templates/list_files.html', files=get_files())


class LogHandler(tornado.web.RequestHandler):
    async def get(self, name):
        """Serves the requested log."""
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', f'attachment; filename={name}.txt')
        for chunk in get_log_stream(name):
            self.write(chunk)
            await self.flush()
        self.finish()


# ONLY FOR DEBUGGING PURPOSES
class PopulateHandler(tornado.web.RequestHandler):
    def get(self):
        # For docker
        #os.system('python /app/populate_files.py &')
        os.system('python populate_files.py &')
        self.redirect('/')
