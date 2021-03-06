Prototype sequence correction
=============================

[![Build Status](https://travis-ci.org/nanoporetech/medaka.svg?branch=master)](https://travis-ci.org/nanoporetech/medaka)

Medaka demonstrates a framework for error correcting sequencing data,
particularly aimed at nanopore sequencing. Tools are provided for both training
and inference. The code exploits the [keras]('https://keras.io') deep learning
library.

The framework provided has had limited testing and benchmarking, but it is
being released in an effort to allow researchers to experiment without having
to write much of the tedious data preparation code. Researchers can extend the
tools provided to achieve better results that those obtained currently.

Development of medaka as a "base-space" consensus tool has been paused to focus
on methods which exploit the nanopore signal data. Nevertheless researchers may
find medaka useful as a method to generate quickly sufficiently accurate
consensus sequences in many use cases; see the
[Benchmarks](https://nanoporetech.github.io/medaka/benchmarks.html) page for
further details.

Documentation can be found at https://nanoporetech.github.io/medaka/.


Installation
------------
  
Medaka should be installed inside a virtual environment. A Makefile is
provided to fetch, compile and install all direct dependencies into an
environment.

To setup the environment run:

    git clone https://github.com/nanoporetech/medaka.git
    cd medaka
    make install
    . ./venv/bin/activate
