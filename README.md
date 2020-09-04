# PL-courseInstance-config (plcc)

Python module to help config PrairieLearn's (PL) courseInstance.json

- [PL-courseInstance-config (plcc)](#pl-courseinstance-config-plcc)
  - [What This Is](#what-this-is)
  - [Software Requirements](#software-requirements)
  - [Getting Started](#getting-started)
  - [How to Use](#how-to-use)
    - [Pre-requisite](#pre-requisite)
    - [Use plcc](#use-plcc)
  - [Features](#features)

## What This Is

In [PrairieLearn](https://prairielearn.readthedocs.io/en/latest/), courses are categorized by individual instances they're offered. For example, a class called CS 101 may be offered in the Spring 2018, Spring 2019, Spring 2020 etc. Each of the offerings of a class is an instance of the class.

Each instance is configured by a file called `infoCourseInstance.json`, that defines some important information about the instance itself, such as access times, users, and timezones etc. [More Info](https://prairielearn.readthedocs.io/en/latest/courseInstance/)

The most difficult property in this file to deal with is `"userRoles"` which includes a mapping `<email> : <user role>` for every single person involved with the course, whenever a new person is added or dropped, this file would need to be updated and synced up with the PL server to maintain consistency. This can be annoying, and error prone. This module aims to solve some of the issues, especially pushing updates to said section, such as at the beginning of the course when administrators might need to manage thousands of students.

Current version is built with Canvas in mind, future versions will provide more flexibility.

## Software Requirements

Language Requirement: python 3.8+ (uses `collections.abc` lib)

Dependencies: None 🎉

## Getting Started

Download the latest release [https://github.com/bojinyao/PL-courseInstance-config](https://github.com/bojinyao/PL-courseInstance-config)

This project is written as a python module, technically you do not need to unzip the file. However, considering the length of the project name, we will refer to this project as `plcc` from here on.

## How to Use

### Pre-requisite

Download course roster as a csv file from Canvas.

1. Go to Roster Photos
2. Click Export

Make sure you have an existing, non-empty `infoCourseInstance.json` file, this module will NOT create the file for you for safety reasons.

### Use plcc

For full command-line options:

```bash
python3 plcc -h
```

To load course roster csv, the command might look like:

```bash
python3 plcc <path to json> --csv <path to csv>
```

The `--csv` option can be shortened to `-c`

## Features

After its execution, the module will print a small summary to stdout that tells you if any changes are made to the json file. And if there are, it will tell you how entries are added, updated, or deleted. It will also warn you of changed roles or emails not found.

If no change is made to the json file, it will let you know of that fact too.

By Default, `"userRoles"` will be grouped by roles, with `"Instructor"` at the top, then `"TA"`, then `"Student"`. The reason being there are usually more Students than TAs, and more TAs than Instructors.
