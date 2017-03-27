SF SPECS
========

This repository can be used to facilitate story grooming asynchronously
and ensuring the quality of new specs thanks to gating and code review.

HOW TO ADD STORIES
------------------

Simply add a yaml file describing the story and its tasks under the `stories`
directory. Stories can be organized under "epics" if stored in subfolders.

The required format of the yaml story file is explained in the sample story
in the repository. the `validator.py` utility will check the story file for
basic prerequisites (story description and at least one task).

SCRIPTS
-------

* validator.py: a simple syntax checker making sure stories are well defined
* storyboard.py: automated export of yaml stories to Storyboard (assuming
  the stories were validated with validator.py)
