# Development Guide

## Packaging and Deploying
This repository hosts the `WellnessBot` client package. It is hosted on `pypi` and can be installed on any machine using pip:
```bash
python3 -m pip install WellnessBot
```

Here I will describe how we build and publish new package distributions based on [this](https://www.codementor.io/@arpitbhayani/host-your-python-package-using-github-on-pypi-du107t7ku) guide:

1. First you will need a `pypi` if you do not have both of these you will need to create these accounts.
2. Create a `.pypirc` file in the home directory with the following structure replacing USERNAME and PASSWORD with your account credentials:
    ```rc
    [distutils]
    index-servers =
        pypi

    [pypi]
    repository: https://upload.pypi.org/legacy/
    username: USERNAME
    password: PASSWORD
    ```
4. After it is merged into master increment the version number appropriately in [here](../app/__version__.py)
5. Build the distribution:
    ```bash
    ./scripts/build.sh
    ```
6. After validating the package works push to pypi:
    ```bash
    ./scripts/publish.sh pypi
    ```
