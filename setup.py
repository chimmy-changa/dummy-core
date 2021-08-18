# Copyright 2020-2021 The MathWorks, Inc.
import os
from setuptools.command.install import install
import setuptools
from pathlib import Path
from shutil import which
from matlab_web_desktop_proxy.default_config import default_config

npm_install = ["npm", "--prefix", "gui", "install", "gui"]
npm_build = ["npm", "run", "--prefix", "gui", "build"]


class InstallNpm(install):
    def run(self):

        # Ensure npm is present
        if which("npm") is None:
            raise Exception(
                "npm must be installed and on the path during package install!"
            )

        self.spawn(npm_install)
        self.spawn(npm_build)
        target_dir = Path(self.build_lib) / self.distribution.packages[0] / "gui"
        self.mkpath(str(target_dir))
        self.copy_tree("gui/build", str(target_dir))

        # In order to be accessible in the package, turn the built gui into modules
        (Path(target_dir) / "__init__.py").touch(exist_ok=True)
        for (path, directories, filenames) in os.walk(target_dir):
            for directory in directories:
                (Path(path) / directory / "__init__.py").touch(exist_ok=True)

        super().run()


tests_require = [
    "pytest",
    "pytest-env",
    "pytest-cov",
    "pytest-mock",
    "pytest-dependency",
    "pytest-aiohttp",
    "requests",
    "psutil",
    "aioresponses",
]

HERE = Path(__file__).parent.resolve()
long_description = (HERE / "README.md").read_text()

setuptools.setup(
    name="dummy-core",
    version="0.2.0",
    url=default_config["url"],
    author="The MathWorks, Inc.",
    # TODO: Update email
    author_email="jupyter-support@mathworks.com",
    license="MATHWORKS CLOUD REFERENCE ARCHITECTURE LICENSE",
    # TODO: Update description
    description="Jupyter extension to proxy MATLAB JavaScript Desktop",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["devel", "tests"]),
    # TODO: keywords, classfiers.
    keywords=["Jupyter"],
    classifiers=["Framework :: Jupyter"],
    python_requires="~=3.7",
    install_requires=["aiohttp>=3.7.4"],
    setup_requires=["pytest-runner"],
    tests_require=tests_require,
    extras_require={"dev": ["aiohttp-devtools"] + tests_require},
    entry_points={
        "matlab_web_desktop_proxy_configs": [
            "default_config = matlab_web_desktop_proxy.default_config:default_config"
        ],
        "console_scripts": [
            "matlab-web-desktop-app = matlab_web_desktop_proxy.app:main"
        ],
    },
    include_package_data=True,
    zip_safe=False,
    cmdclass={"install": InstallNpm},
)
