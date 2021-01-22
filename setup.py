import io
import os
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as f:
        return f.read()


def load_about():
    about = {}
    with io.open(
        os.path.join(HERE, "oxct", "__about__.py"), "rt", encoding="utf-8"
    ) as f:
        exec(f.read(), about)  # pylint: disable=exec-used
    return about


def load_requirements():
    with io.open(
        os.path.join(HERE, "requirements", "base.in"), "rt", encoding="utf-8"
    ) as f:
        return [line.strip() for line in f if is_requirement(line)]


def is_requirement(line):
    return not (line.strip() == "" or line.startswith("#"))


ABOUT = load_about()


setup(
    name="oxct",
    version=ABOUT["__version__"],
    url="https://github.com/openedx/oxct",
    project_urls={
        "Documentation": "https://github.com/openedx/oxct",
        "Code": "https://github.com/openedx/oxct",
        "Issue tracker": "https://github.com/openedx/oxct/issues",
        "Community": "https://discuss.openedx.org",
    },
    license="AGPLv3",
    author="Open edX",
    author_email="contact@openedx.org",
    description="Open edX Community Tools",
    long_description=load_readme(),
    long_description_content_type="text/x-rst",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=load_requirements(),
    entry_points={
        "console_scripts": [
            "oxct=oxct.client.main:main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
