"""Sphinx contrib plugin for documenting Doozer CLI extensions."""

from sphinxcontrib.autoprogram import AutoprogramDirective

from doozer import Application
from doozer.extensions import Extension


def _import_extension(import_path: str) -> Extension:
    module_name, extension_name = import_path.split(':', 1)
    module = __import__(module_name, fromlist=[extension_name])
    return getattr(module, extension_name)


class DoozerCLIDirective(AutoprogramDirective):
    """A Sphinx directive that can be used to document a CLI extension.

    This class wraps around
    `autoprogram <https://pythonhosted.org/sphinxcontrib-autoprogram/>`_
    to generate Sphinx documentation for extensions that extend the
    Doozer CLI.

    .. code::

        .. doozercli:: doozer_database:Database
           :start_command: db

    .. versionchanged:: 1.2.0

        The ``prog`` option will default to the proper way to invoke
        command line extensions.
    """

    def prepare_autoprogram(self) -> None:
        """Prepare the instance to be run through autoprogram."""
        # Tell autoprogram how to find the argument parser.
        self.arguments = 'doozer.cli:parser',

        # Most Doozer CLI extensions will be invoked the same way. The
        # extension authors shouldn't have to include that in their
        # Sphinx documentation.
        self.options.setdefault('prog', 'doozer --app APP_PATH')

    def register_cli(self) -> None:
        """Register the CLI."""
        import_path, = self.arguments
        extension = _import_extension(import_path)
        extension().register_cli()

    def run(self) -> None:
        """Register the CLI and run autoprogram."""
        self.register_cli()
        self.prepare_autoprogram()

        return super().run()


def setup(app: Application) -> None:
    """Register the extension."""
    app.add_directive('doozercli', DoozerCLIDirective)
