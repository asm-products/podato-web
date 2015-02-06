<a href="https://assembly.com/saulify/bounties?utm_campaign=assemblage&utm_source=saulify&utm_medium=repo_badge"><img src="https://asm-badger.herokuapp.com/saulify/badges/tasks.svg" height="24px" alt="Open Tasks" /></a>

#### Made by Assembly

Assembly products are like open-source and made with contributions from the community. Assembly handles the boring stuff like hosting, support, financing, legal, etc. Once the product launches we collect the revenue and split the profits amongst the contributors.

Visit [https://assembly.com](https://assembly.com) to learn more.

### Contributing

To contribute:

1. [Find a bounty you'd like to work on.](https://assembly.com/podato/bounties)
2. [Fork this repository](https://github.com/asm-products/podato-web/fork), unless you have push rights to this repo.
3. Create a new branch with a descriptive name.
4. Work on your bounty. If your changes have an impact on the instructions in this README, be sure to update it.
5. Make a pull request. It'll be reviewed, and if everything is ok, we'll pull it in. Be sure to somehow link your pull request to the bounty so we can easily reward you for your work, either by linking from the PR to the bounty or vice versa.

### Your dev environment

1. Install the [App Engine SDK for Python](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python)
2. Install the [App Engine SDK for Go](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Go)
3. Add the path to the Go SDK to your PATH by adding the following line to your .bashrc, .profile or equivalent:

        export PATH=/path/to/go_appengine:$PATH

### Running the development server:

from the root of the project, run the following command:

```shell
sh runserver.sh
```
