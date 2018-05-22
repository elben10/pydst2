#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydst` package."""

import pytest

from click.testing import CliRunner

import pydst
from pydst import cli
from pandas import DataFrame


def test_DST_subjects():
    assert isinstance(pydst.DST().get_subjects(), DataFrame)
