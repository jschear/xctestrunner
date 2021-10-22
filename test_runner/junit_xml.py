# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helper functions for writing a JUnit XML report."""

import xml.etree.ElementTree as ET


class Test:
  def __init__(self, name, duration):
    self.name = name
    self.duration

  def to_xml(self):
    element = ET.Element('testcase')
    element.set('time', self.name)
    element.set('duration', self.duration)
    return element


class TestSuite:
  # TODO(jschear): tests is a List[Union[TestSuite, Test]], i.e. we allow nested TestSuites -- is that valid JUnit XML? Can we declare the type?
  def __init__(self, name, duration, tests):
    self.name = name
    self.duration = duration
    self.tests = tests

  def to_xml(self):
    element = ET.Element('testsuite')
    element.set('time', self.name)
    element.set('duration', self.duration)
    element.extend([test.to_xml() for test in self.tests])
    return element


class TestSuites:
  def __init__(self, testsuites):
    self.testsuites = testsuites

  def to_xml(self):
    element = ET.Element('testsuites')
    element.extend([testsuite.to_xml() for testsuite in self.testsuites])
    return element


def WriteReport(testsuites, path):
  element_tree = ET.ElementTree(element=testsuites.to_xml())
  # TODO(jschear): indent is Python 3.9+, is there a better option?
  ET.indent(element_tree)
  element_tree.write(path, encoding='UTF-8', xml_declaration=True)
