# Guide to contributing to SatChecker

Welcome to the SatChecker contributing guide! SatChecker is a tool for predicting satellite positions and providing other relevant data, developed by the IAU Centre for the Protection of the Dark and Quiet Sky from Satellite Constellation Interference (IAU CPS) SatHub group.

Bug report/fixes, feature requests, and other contributions are welcome, and all issues and pull requests will be reviewed by a repo maintainer to ensure consistency with the project's scope and other guidelines.

For any questions not answered here please email sathub@cps.iau.org or open an issue. We are in the process of creating additional issues for the GitHub repo based off of known issues and changes to make, so that section is a work in progress.

## Getting Started
1. Fork and clone the repository ([instructions](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo))
2. Follow the local environment setup instructions in the wiki (https://github.com/iausathub/satchecker/wiki/setup)
3. For the step to run retrieve_tle.py to populate the database, make sure you only use **celestrak** as a data source unless you create a Space-Track.org account, as they require a user account for API access. It's recommended to run retrieve_tle.py on several different days to get a wider range of data used for testing, so that you can make sure that functionality dependent on selecting the TLE with an epoch closest to a requested date works correctly.
4. Review the issues or propose a new feature.
5. Open a pull request when you're done - if this was for a new feature, only features approved by a project maintainer will be considered for merging into the project.

## Code Quality
* Please review the IAU CPS SatHub general guidelines [here](https://github.com/iausathub/.github/blob/main/CONTRIBUTING.md).
  
* The project has Ruff and Black set up to run as part of pull requests and commits to branches in this repository, and info on the rules used for those can be found in the wiki [here](https://github.com/iausathub/satchecker/wiki/Development-Workflow).

* The wiki also has instructions for how to update the .rst documentation files, which is required for any changes to either add functions/modules or change parameters.

* Pytest is used for testing.

* Use Google-style docstrings -- example:
```
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.

    Raises:
        ValueError: If either `a` or `b` is not an integer.
    """
```

## Pull request guidelines
* Create a new pull request for each feature or bug fix.
* Add a clear title and description of the changes.
* Don't forget to include relevant tests or examples to demonstrate the changes, and make sure all existing tests still pass.
* Include a link to any relevant issues or discussions.


#### License Info
All code that is part of SatChecker is currently released under the [BSD-3-Clause](https://opensource.org/licenses/BSD-3-Clause) license.
