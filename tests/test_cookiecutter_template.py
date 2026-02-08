import pathlib

from cookiecutter.main import cookiecutter

TEMPLATE_DIRECTORY = str(pathlib.Path(__file__).parent.parent)


def test_generated_files(tmpdir):
    generate(
        tmpdir,
        {
            "project_dir_name": "awesome-project",
        },
    )
    assert paths(tmpdir) == {
        "awesome-project",
        "awesome-project/.github",
        "awesome-project/.github/workflows",
        "awesome-project/.github/workflows/publish.yml",
        "awesome-project/.github/workflows/testing.yml",
        "awesome-project/pyproject.toml",
        "awesome-project/setup.py",
        "awesome-project/src",
        "awesome-project/src/awesome_project",
        "awesome-project/src/awesome_project/__init__.py",
        "awesome-project/src/awesome_project/__main__.py",
        "awesome-project/tests",
        "awesome-project/tests/__init__.py",
    }


def generate(directory, context):
    directory_path = pathlib.Path(str(directory))
    temp_config = {
        "replay_dir": str(directory_path.parent / ".cookiecutter_replay"),
        "cookiecutters_dir": str(directory_path.parent / ".cookiecutters"),
    }
    cookiecutter(
        template=TEMPLATE_DIRECTORY,
        output_dir=str(directory),
        no_input=True,
        extra_context=context,
        default_config=temp_config,
    )


def paths(directory):
    generated_paths = list(pathlib.Path(directory).glob("**/*"))
    generated_paths = [path.relative_to(directory) for path in generated_paths]
    return {str(path) for path in generated_paths if str(path) != "."}
