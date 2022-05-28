# TM-compiler

A Turing Machine compiler. 

## What does it do?

This compiler compiles a pseudo-assembly like description of a machine into a list of transitions runnable on a [TM simulator](http://morphett.info/turing/turing.html). In other words, it makes it easier to write Turing Machines.

## Features

- Programmatic generation of Turing Machines
- Persistent bits of "memory" through conditional flags
- State labels and fall-through transitions

## How do I use it?

1. Write a description of a machine using the `compile` function (see [palindrome.py](palindrome.py) for an example)
2. Run the script you've written (`python3 palindrome.py`)
3. Paste the output into a TM simulator

## Acknowledgements

Written during UNSW's COMP4141 course.
