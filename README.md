# Debate-Gender-Stats

Welcome to the project!! This project is designed to provide equity teams and debaters with enhanced insights into the performance of male and female speakers at competitive debating tournaments. It consists of a piece of software that analyzes a speaker tab, probabilistically categorizes speakers as male or female on the basis of their first name, then calculates a number of metrics which measure the relative performance of each group.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and running purposes.

### Prerequisites

This project requires Python 3.4 to be installed on your computer. If you do not have Python installed, or are running an older version of Python, If you are running an older version of Python, [download the latest version here](https://www.python.org/downloads/). To check if you have Python 3 installed, navigate to your Terminal, and, at the prompt, type `python3` and press enter. If something akin to the following appears, then you have a version of Python 3 running on your machine:

```
Python 3.4.3 (v3.4.3:9b73f1c3e601, Feb 23 2015, 02:52:03) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

To exit from this Python shell, simply type `quit()` and press enter.

The following installation instructions assume a familiarity running commands in a Terminal. __If you are unfamiliar with running commands on a terminal, there are two conventions to keep in mind__ when following the below instructions: (1) The `$` sign is a convention indicating that the following command is a command to be run in Terminal; do not include it when actually running your commands. (2) Square brackets are used to indicate variable information that you should include without the square brackets. For example, if a command says, `$ cd [project_folder]`, the real command would look something like `$ cd debate-gender-stats` depending on the name of the project folder and your current location in your computer's file tree.

### Installation


1. Download the git repository to your computer:
```
$ git clone [project_url]
```

2. Install libraries

Navigate to the newly-created project folder in your Terminal (by typing `$ cd debate-gender-stats` and pressing enter), and run the following command to install the necessary pip dependencies:
```
$ pip install -r requirements.txt
```

You should now be all set to run it!

## Running the Project

To run the project on your machine, drag the debate speaker tab (in the .csv format of the data released by APDA board) whcih you wish to analyze into the project folder. Then, navigate to the project folder in your Terminal. At the prompt, type:

```$ python3 debate_gender_stats.py [filename]```

Where `[filename]` is the name of the debate tab file that you have just added to the folder.

## Built With

## Contributing

We would welcome suggestions and contributions!

To offer feedback and ideas, please [open an issue in the GitHub repository](https://github.com/cooper-mj/debate-gender-stats/issues), or [send me an email](mailto:coopermj@stanford.edu).

If you'd just like to add a new feature, don't hesitate to open a pull request!

## Authors

* **[Michael Cooper](https://github.com/cooper-mj)** - _Initial work, current active developer._

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


