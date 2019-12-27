"""
Nozomi
Render Dependency Module
Author: hugh@blinkybeach.com
"""


class RenderDependency:
    """
    Abstract class providing underlying functionality for rendering dependencies
    built from files.
    """

    _DEFAULT_NAME = 'Render Dependency'

    def __init__(
        self,
        script_name: str,
        extension: str,
        path: str,
        name: str = None,
    ):
        assert isinstance(self._EXTENSION, str)
        assert isinstance(self._NAME, str)

        assert extension[:1] == '.'

        self._name = name
        if self._name is None:
            self._name = self._DEFAULT_NAME

        assert isinstance(script_name, str)
        self._script_name = script_name

        assert isinstance(path, str)

        self._full_path = path + self._script_name + self._EXTENSION
        self._content = self._load_file(self._full_path)
        return

    def _load_file(self, full_path) -> str:
        """
        Return a file's contents as a string
        """
        with open(full_path, 'r') as file:
            return file.read()

    def __str__(self) -> str:
        return self._content

    def __repr__(self) -> str:
        return self._name + ': ' + self._script_name + self._EXTENSION
