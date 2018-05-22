#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydst` package."""

import pytest

import pydst
from pandas import DataFrame


def test_DST_subjects():
    assert isinstance(pydst.DST().get_subjects(), DataFrame)
