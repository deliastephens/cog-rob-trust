# cog-rob-trust
Exploring a simple implementation of a meta-MDP for trust-generating policies.

## Getting Started

### Local Installation
You can choose to run this machine locally, but you'll need to set up and install a few dependencies first:

* [Jupyter Notebooks](https://jupyter.org/), for running and viewing the `.ipynb` files.
* [`IPython`](https://ipython.org/install.html) for the notebook.
* [`pyperplan`](https://github.com/aibasel/pyperplan), the lightweight STRIPS planner we've chosen to use as our planner (`optic` is very tricky to compile, and we won't be needing its `durative-actions` capabilities).

If installing Python packages locally, it's easiest done with a Python Virtual Environment. Python3 supports [virtual environments natively](https://docs.python.org/3/library/venv.html), or you can use a package like [Anaconda](https://www.anaconda.com/). All of the above can be installed with `pip`, the [Python package manager](https://pip.pypa.io/en/stable/) once the appropriate virtual environment is activated.

To start a Jupyter Notebook (once everything is installed and you're in the correct virtual environment), navigate to the `cog-rob-trust` folder and run the following:

```
jupyter notebook
```

A window should open up automatically!

### BinderHub
Alternatively, you may edit the `.ipynb` file on BinderHub; note that you'll have to copy/paste your changes back into a local repo and push them to Git if you want them to stay up there!

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/deliastephens/cog-rob-trust/HEAD)