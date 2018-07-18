"""Tests for doozer.contrib.sphinx."""

from docutils.statemachine import StringList
import pytest

from doozer import Extension
from doozer.contrib import sphinx


@pytest.fixture
def modules_tmpdir(tmpdir, monkeypatch):
    """Add a temporary directory for modules to sys.path."""
    tmp = tmpdir.mkdir("tmp_modules")
    monkeypatch.syspath_prepend(str(tmp))
    return tmp


@pytest.fixture
def test_module(modules_tmpdir, test_app):
    """Create a module for a fake extension."""
    fake_extension = modules_tmpdir.join("fake_extension.py")
    fake_extension.write(
        "\n".join(
            (
                "from doozer import Extension",
                "class FakeExtension(Extension):",
                "    def register_cli(self): pass",
            )
        )
    )


@pytest.fixture
def test_directive(test_module):
    """Return an instance of DoozerCLIDirective."""
    return sphinx.DoozerCLIDirective(
        name="doozercli",
        arguments=["fake_extension:FakeExtension"],
        options={},
        content=StringList([], items=[]),
        lineno=1,
        content_offset=0,
        block_text=".. doozercli:: fake_extension:FakeExtension\n",
        state=None,
        state_machine=None,
    )


def test_doozerclidirective_doesnt_change_prog(test_directive):
    """Test that DoozerCLIDirective.prepare_autoprogram doesn't change prog."""
    test_directive.options["prog"] = "testing"
    test_directive.prepare_autoprogram()
    assert test_directive.options["prog"] == "testing"


def test_doozerclidirective_sets_parser(test_directive):
    """Test that DoozerCLIDirective.prepare_autoprogram sets the parser."""
    test_directive.prepare_autoprogram()
    assert test_directive.arguments == ("doozer.cli:parser",)


def test_doozerclidirective_sets_prog(test_directive):
    """Test that DoozerCLIDirective.prepare_autoprogram sets prog."""
    test_directive.prepare_autoprogram()
    assert test_directive.options["prog"] == "doozer --app APP_PATH"


def test_doozerclidirective_register_cli(test_directive):
    """Test that DoozerCLIDirective.register_cli doesn't fail."""
    # This will only test that it runs without raising an exception.
    test_directive.register_cli()


def test_import_extension(test_module):
    """Test that _import_extension returns the extension."""
    import_path = "fake_extension:FakeExtension"
    extension = sphinx._import_extension(import_path)
    assert issubclass(extension, Extension)


def test_setup():
    """Test that setup registers the directive."""

    class SphinxApplication:
        def add_directive(self, directive, cls):
            self.directive = directive
            self.cls = cls

    app = SphinxApplication()

    sphinx.setup(app)

    assert app.directive == "doozercli"
    assert app.cls is sphinx.DoozerCLIDirective
