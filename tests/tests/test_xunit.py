"""
Tests for the XUnit report feature.
"""

import xml.etree.ElementTree as ET

from e3.testsuite import Testsuite as Suite
from e3.testsuite.driver import BasicTestDriver as BasicDriver
from e3.testsuite.result import TestStatus as Status

from .test_basics import run_testsuite


def test_basic():
    """Check that requesting a XUnit testsuite report works."""

    class MyDriver(BasicDriver):
        def run(self, prev):
            self.result.log += "Work is being done..."

        def analyze(self, prev):
            if self.test_env["test_name"] == "test1":
                self.result.set_status(Status.PASS, "all good")
            else:
                self.result.set_status(Status.FAIL, "test always fail!")
            self.push_result()

    class Mysuite(Suite):
        TEST_SUBDIR = "simple-tests"
        DRIVERS = {"default": MyDriver}
        default_driver = "default"

    xunit_file = "xunit.xml"
    run_testsuite(Mysuite, ["--xunit-output", xunit_file])

    # For now, just check that this produces a valid XML file
    ET.parse(xunit_file)
