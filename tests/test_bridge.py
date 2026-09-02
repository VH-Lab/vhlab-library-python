"""Unit tests for the MATLAB -> Python bridge contract files.

Each vhlib package carries a `vhlib_matlab_python_bridge.yaml` recording where
every module came from in vhlab-library-matlab. These tests keep the two in
step: a new module without a bridge entry, or a bridge entry pointing at a file
that no longer exists, fails here.
"""

import os
import unittest

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE_NAME = 'vhlib_matlab_python_bridge.yaml'
ROOT_BRIDGE = os.path.join(REPO_ROOT, 'vhlib', BRIDGE_NAME)

# Packages that carry a function-level bridge file.
FUNCTION_PACKAGES = ('vhlib/CDM', 'vhlib/StimDecode', 'vhlib/md',
                     'vhlib/response_stats')


def load(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def bridge_files():
    """Every bridge file in the repository, as absolute paths."""
    found = []
    for dirpath, _dirnames, filenames in os.walk(os.path.join(REPO_ROOT, 'vhlib')):
        if BRIDGE_NAME in filenames:
            found.append(os.path.join(dirpath, BRIDGE_NAME))
    return sorted(found)


def python_modules(package_path):
    """Every non-__init__ module in a package, repo-relative, recursively."""
    modules = []
    for dirpath, _dirnames, filenames in os.walk(os.path.join(REPO_ROOT, package_path)):
        for name in filenames:
            if name.endswith('.py') and name != '__init__.py':
                full = os.path.join(dirpath, name)
                modules.append(os.path.relpath(full, REPO_ROOT))
    return sorted(modules)


class TestBridgeFiles(unittest.TestCase):

    def test_every_package_has_a_bridge_file(self):
        for package in FUNCTION_PACKAGES:
            path = os.path.join(REPO_ROOT, package, BRIDGE_NAME)
            self.assertTrue(os.path.isfile(path),
                            'missing bridge file for package ' + package)
        self.assertTrue(os.path.isfile(ROOT_BRIDGE),
                        'missing top-level bridge file ' + ROOT_BRIDGE)

    def test_bridge_files_parse(self):
        for path in bridge_files():
            data = load(path)
            self.assertIsInstance(data, dict, path + ' is not a mapping')
            self.assertIn('project_metadata', data, path)
            metadata = data['project_metadata']
            for key in ('bridge_version', 'python_package', 'naming_policy',
                        'indexing_policy'):
                self.assertIn(key, metadata, path + ' project_metadata.' + key)

    def test_status_values_are_from_the_vocabulary(self):
        vocabulary = set(load(ROOT_BRIDGE)['status_vocabulary'].keys())
        for path in bridge_files():
            data = load(path)
            entries = list(data.get('functions', [])) + list(data.get('coverage_areas', []))
            entries += list(data.get('downstream_requirements', []))
            for entry in entries:
                label = entry.get('name') or entry.get('matlab_path')
                self.assertIn('status', entry,
                              '%s: %s has no status' % (path, label))
                self.assertIn(entry['status'], vocabulary,
                              '%s: %s has unknown status %r' % (path, label, entry['status']))

    def test_function_entries_are_well_formed(self):
        for path in bridge_files():
            for entry in load(path).get('functions', []):
                label = entry.get('name')
                self.assertIsNotNone(label, path + ': entry with no name')
                self.assertIn(entry.get('type'), ('function', 'class', 'method'),
                              '%s: %s has bad type %r' % (path, label, entry.get('type')))
                self.assertTrue(entry.get('decision_log'),
                                '%s: %s has no decision_log' % (path, label))
                if entry['status'] in ('ported', 'does_not_exist'):
                    self.assertTrue(entry.get('python_path'),
                                    '%s: %s is %s but has no python_path'
                                    % (path, label, entry['status']))
                else:
                    self.assertIsNone(entry.get('python_path'),
                                      '%s: %s is %s but names a python_path'
                                      % (path, label, entry['status']))
                if entry['status'] != 'does_not_exist':
                    self.assertTrue(entry.get('matlab_path'),
                                    '%s: %s has no matlab_path' % (path, label))

    def test_python_paths_exist(self):
        for path in bridge_files():
            data = load(path)
            for entry in data.get('functions', []) + data.get('subpackages', []):
                for key in ('python_path', 'bridge_file'):
                    value = entry.get(key)
                    if not value:
                        continue
                    self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, value)),
                                    '%s: %s -> %s does not exist'
                                    % (path, entry.get('name', entry.get('python_package')), value))

    def test_every_module_is_covered_by_a_bridge_entry(self):
        for package in FUNCTION_PACKAGES:
            data = load(os.path.join(REPO_ROOT, package, BRIDGE_NAME))
            covered = set()
            for entry in data.get('functions', []):
                if entry.get('python_path'):
                    covered.add(entry['python_path'])
            for module in python_modules(package):
                self.assertIn(module, covered,
                              '%s has no entry in %s/%s' % (module, package, BRIDGE_NAME))

    def test_root_bridge_lists_every_package(self):
        data = load(ROOT_BRIDGE)
        listed = {entry['python_path'] for entry in data['subpackages']}
        self.assertEqual(listed, set(FUNCTION_PACKAGES))
        for entry in data['subpackages']:
            self.assertTrue(entry.get('matlab_path'),
                            entry['python_package'] + ' has no matlab_path')


if __name__ == '__main__':
    unittest.main()
