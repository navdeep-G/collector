import os
from concurrent.futures import ThreadPoolExecutor

import tornado.web
from tornado.ioloop import IOLoop

from models import add_feedback, validate_feedback, get_feedbacks, get_log_stream

# It appears that the minio is not asyncio "compatible" - it would block
# So I use threading instead which should work fine since it is an IO-bound
# operation.
_executor = ThreadPoolExecutor()


class AddFeedbackHandler(tornado.web.RequestHandler):
    def get(self):
        """Renders the Add New Feedback form.
        """
        return self.render('templates/add_feedback.html',feedback='', errors=[])

    async def post(self):
        """Async handler for accepting feedback and storing it in DB.
        """
        feedback = dict(
            feedback=self.get_body_argument('feedback'),
            log=self.request.files['log'][0] if 'log' in self.request.files else None
        )

        # Validate the feedback
        errors = validate_feedback(feedback)
        if len(errors) > 0:
            return self.render(
                'templates/add_feedback.html',
                errors=errors,
                **feedback
            )

        # Save the feedback
        success = await IOLoop.current().run_in_executor(
            _executor,
            add_feedback,
            feedback
        )
        if not success:
            errors.append('Opps! Something went wrong.')
            return self.render(
                'templates/add_feedback.html',
                errors=errors,
                **feedback
            )

        self.redirect('/')


class FeedbacksHandler(tornado.web.RequestHandler):
    def get(self):
        """Renders the list of feedbacks."""
        return self.render('templates/list_feedbacks.html', feedbacks=get_feedbacks())


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
        #os.system('python /app/populate_feedbacks.py &')
        os.system('python populate_feedbacks.py &')
        self.redirect('/')
