from collections import defaultdict

import tornado.web


class Rating(tornado.web.UIModule):
    def render(self: 'Rating', name: str, checked: int = 3, disabled: bool = False, num_of_stars: int = 5) -> str:
        """
             Generates HTML code for showing rating stars.

             :param name: name of the rating radio group
             :param checked: how many stars should be checked by default
             :param disabled: property of radio button
             :param num_of_stars: total number of stars showed
             :return: HTML string
         """

        additional_params = defaultdict(lambda: ' disabled' if disabled else '')
        additional_params[int(checked)] += ' checked'

        stars = [f'<label for="{name}{i}"></label>'
                 f'<input id="{name}{i}" type="radio" name="{name}" value="{i}"{additional_params[i]}>'
                 for i in range(1, num_of_stars + 1)]
        stars = '\n    '.join(stars)

        return f'<div class="star-rating">\n    {stars}\n</div>'
