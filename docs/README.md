# Development Guide

## DB design
### The `challenge_pool`
The `challenge_pool` holds a set of challenges.
An example of single entry in the `challenge_pool` can be:
```json
{
"id": 9,
"name": "5 Burpees",
"author": "David Sean",
"challenge": {
    "timeout": 300,
    "description": "Do 5 burpees"
    }
}
```
TODO: ^^ change the `challenge` key to `challenge_body` to reduce namespace confusion.
Since `challenge_pool` is a set, all challenges it holds are unique.
Initially, the pool is populated from challenges stored as yaml files under the `challenges/` directory.
It will eventually be possible to dynamically add new challenges directly from Discord using `!add_challenge` command.

### The `users` collection
This one is straight-forward:
```json
{
"id": 9,
"name": "dav#6692"
}
```
We would have to be carefull that this doesn't grow indefinitely. Perhaps a last-activity field so that old one can be pruned after inactivity?

### The `issued_challenge` collection

An `issued_challenge` is created after the challenge timeout is reached.
It contains a `challenge_id` that references a challenge from the `challenge_pool`, and contains a list of `user_ids` that references users that participated.
And example `issued_challenge` entry would look like:
```json
{
"id": 5,
"date": "2021-05-22T22:16:58+00:00",
"challenge_id": 2,
"user_ids": [2, 3 ,6, 7],
}
```

With these three collections, we can compute stats over a day or a week... or year (can count in dates intervals).
The `!reset` command can be deprecated since weeks/days are automatic

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
