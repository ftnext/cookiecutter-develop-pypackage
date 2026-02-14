import pathlib

from cookiecutter.main import cookiecutter

TEMPLATE_DIRECTORY = str(pathlib.Path(__file__).parent.parent)


def test_generated_files_without_taskipy(tmpdir):
    generate(
        tmpdir,
        {
            "project_dir_name": "awesome-project",
            "use_taskipy": "no",
        },
    )
    assert paths(tmpdir) == expected_paths()

    project_root = pathlib.Path(str(tmpdir)) / "awesome-project"
    pyproject = (project_root / "pyproject.toml").read_text(encoding="utf-8")
    workflow = (
        project_root / ".github" / "workflows" / "testing.yml"
    ).read_text(encoding="utf-8")

    assert "[tool.taskipy.tasks]" not in pyproject
    assert '"taskipy"' not in pyproject
    assert "pytest -v" in workflow
    assert "task test" not in workflow


def test_generated_files_with_taskipy(tmpdir):
    generate(
        tmpdir,
        {
            "project_dir_name": "awesome-project",
            "use_taskipy": "yes",
        },
    )
    assert paths(tmpdir) == expected_paths()

    project_root = pathlib.Path(str(tmpdir)) / "awesome-project"
    pyproject = (project_root / "pyproject.toml").read_text(encoding="utf-8")
    workflow = (
        project_root / ".github" / "workflows" / "testing.yml"
    ).read_text(encoding="utf-8")

    assert "[tool.taskipy.tasks]" in pyproject
    assert '"taskipy"' in pyproject
    assert 'format_black = "black -l 79 src tests setup.py"' in pyproject
    assert "task test" in workflow
    assert "pytest -v" not in workflow


def expected_paths():
    return {
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
