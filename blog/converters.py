import re


class ChoiceConverter:
    regex = ''

    def to_python(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ''

    def to_url(self, value):
        result = re.match(self.regex, value)
        return result.group() if result is not None else ''


class BlogOrWorksConverter(ChoiceConverter):
    regex = '(blog|works)'
