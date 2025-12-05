"""
Comprehensive tests for the vhlib.CDM module.
"""

import pytest
import os
import tempfile
import shutil


class TestCellname2Nameref:
    """Tests for cellname2nameref function."""

    def test_basic_cellname(self):
        """Test parsing a standard cell name."""
        from vhlib.CDM import cellname2nameref

        nameref, index, datestr = cellname2nameref('cell_ctx_0003_001_2003_05_27')

        assert nameref['name'] == 'ctx'
        assert nameref['ref'] == 3
        assert index == 1
        assert datestr == '2003_05_27'

    def test_different_name(self):
        """Test parsing cell name with different region name."""
        from vhlib.CDM import cellname2nameref

        nameref, index, datestr = cellname2nameref('cell_v1_0015_042_2020_12_01')

        assert nameref['name'] == 'v1'
        assert nameref['ref'] == 15
        assert index == 42
        assert datestr == '2020_12_01'

    def test_large_numbers(self):
        """Test parsing cell name with large ref and index numbers."""
        from vhlib.CDM import cellname2nameref

        nameref, index, datestr = cellname2nameref('cell_area_9999_0999_1999_01_31')

        assert nameref['ref'] == 9999
        assert index == 999

    def test_invalid_cellname_too_short(self):
        """Test that invalid cell names raise ValueError."""
        from vhlib.CDM import cellname2nameref

        with pytest.raises(ValueError):
            cellname2nameref('cell_ctx_0003')

    def test_invalid_cellname_empty(self):
        """Test that empty cell name raises ValueError."""
        from vhlib.CDM import cellname2nameref

        with pytest.raises(ValueError):
            cellname2nameref('')


class TestCellname2Date:
    """Tests for cellname2date function."""

    def test_basic_date_extraction(self):
        """Test extracting date from cell name."""
        from vhlib.CDM import cellname2date

        date = cellname2date('cell_ctx_0003_001_2003_05_27')

        assert date == '2003-05-27'

    def test_different_date(self):
        """Test extracting different date."""
        from vhlib.CDM import cellname2date

        date = cellname2date('cell_v1_0015_042_2020_12_01')

        assert date == '2020-12-01'

    def test_january_date(self):
        """Test date with January."""
        from vhlib.CDM import cellname2date

        date = cellname2date('cell_abc_0001_001_2025_01_15')

        assert date == '2025-01-15'


class TestNameref2Cellname:
    """Tests for nameref2cellname function."""

    def test_basic_conversion(self):
        """Test basic conversion from nameref to cellname."""
        from vhlib.CDM import nameref2cellname

        # Using a string path as ds
        cellname = nameref2cellname('/path/to/2003-05-27', 'ctx', 3, 1)

        assert cellname == 'cell_ctx_003_001_2003_05_27'

    def test_with_trailing_slash(self):
        """Test path with trailing slash."""
        from vhlib.CDM import nameref2cellname

        cellname = nameref2cellname('/path/to/2003-05-27/', 'ctx', 3, 1)

        assert cellname == 'cell_ctx_003_001_2003_05_27'

    def test_formatting_with_zero_padding(self):
        """Test that ref and index are zero-padded."""
        from vhlib.CDM import nameref2cellname

        cellname = nameref2cellname('/path/2020-01-15', 'v1', 1, 1)

        assert cellname == 'cell_v1_001_001_2020_01_15'

    def test_large_numbers(self):
        """Test with larger ref and index numbers."""
        from vhlib.CDM import nameref2cellname

        cellname = nameref2cellname('/path/2020-01-15', 'area', 999, 123)

        assert cellname == 'cell_area_999_123_2020_01_15'

    def test_invalid_date_format(self):
        """Test that invalid date format raises ValueError."""
        from vhlib.CDM import nameref2cellname

        with pytest.raises(ValueError):
            nameref2cellname('/path/to/20030527', 'ctx', 3, 1)


class TestRoundTrip:
    """Tests for round-trip conversion between cellname and nameref."""

    def test_roundtrip_conversion(self):
        """Test that cellname -> nameref -> cellname preserves data."""
        from vhlib.CDM import cellname2nameref, nameref2cellname

        original = 'cell_ctx_003_001_2003_05_27'
        nameref, index, datestr = cellname2nameref(original)

        # Create path with date in expected format
        path = f'/path/to/{datestr.replace("_", "-")}'
        reconstructed = nameref2cellname(path, nameref['name'], nameref['ref'], index)

        assert reconstructed == original


class TestTrainingHelp:
    """Tests for training help functions."""

    def test_trainingtype_prints_docstring(self, capsys):
        """Test that trainingtype prints its docstring."""
        from vhlib.CDM import trainingtype

        trainingtype()
        captured = capsys.readouterr()

        assert 'trainingtype.txt' in captured.out
        assert 'Bidirectional' in captured.out

    def test_trainingangle_prints_docstring(self, capsys):
        """Test that trainingangle prints its docstring."""
        from vhlib.CDM import trainingangle

        trainingangle()
        captured = capsys.readouterr()

        assert 'trainingangle.txt' in captured.out

    def test_trainingstim_prints_docstring(self, capsys):
        """Test that trainingstim prints its docstring."""
        from vhlib.CDM import trainingstim

        trainingstim()
        captured = capsys.readouterr()

        assert 'trainingstim.txt' in captured.out

    def test_trainingtemporalfrequency_prints_docstring(self, capsys):
        """Test that trainingtemporalfrequency prints its docstring."""
        from vhlib.CDM import trainingtemporalfrequency

        trainingtemporalfrequency()
        captured = capsys.readouterr()

        assert 'trainingtemporalfrequency.txt' in captured.out


class TestUnitquality:
    """Tests for unitquality help function."""

    def test_unitquality_prints_docstring(self, capsys):
        """Test that unitquality prints its docstring."""
        from vhlib.CDM import unitquality

        unitquality()
        captured = capsys.readouterr()

        assert 'unitquality.txt' in captured.out
        assert 'channel' in captured.out


class TestHelpFiles:
    """Tests for help file functions."""

    def test_unitquality_channelshift_prints_docstring(self, capsys):
        """Test that unitquality_channelshift prints docstring."""
        from vhlib.CDM import unitquality_channelshift

        unitquality_channelshift()
        captured = capsys.readouterr()

        assert 'unitquality_channelshift.txt' in captured.out

    def test_testdirinfo_prints_docstring(self, capsys):
        """Test that testdirinfo prints docstring."""
        from vhlib.CDM import testdirinfo

        testdirinfo()
        captured = capsys.readouterr()

        assert 'testdirinfo.txt' in captured.out


class TestAssociateVariablesTxt:
    """Tests for associate_variables_txt help function."""

    def test_associate_variables_txt_prints_docstring(self, capsys):
        """Test that associate_variables_txt prints docstring."""
        from vhlib.CDM import associate_variables_txt

        associate_variables_txt()
        captured = capsys.readouterr()

        assert 'associate_variables.txt' in captured.out


class TestFilterByIndex:
    """Tests for filter_by_index function."""

    def test_filter_within_range(self):
        """Test filtering cells within index range."""
        from vhlib.CDM import filter_by_index

        cells = ['cell_a', 'cell_b', 'cell_c', 'cell_d']
        cellnames = [
            'cell_ctx_0001_001_2020_01_01',
            'cell_ctx_0001_005_2020_01_01',
            'cell_ctx_0001_010_2020_01_01',
            'cell_ctx_0001_015_2020_01_01'
        ]

        filtered_cells, filtered_names, indices = filter_by_index(cells, cellnames, 1, 10)

        assert len(filtered_cells) == 3
        assert len(filtered_names) == 3
        assert indices == [0, 1, 2]

    def test_filter_exact_match(self):
        """Test filtering with exact min=max."""
        from vhlib.CDM import filter_by_index

        cells = ['a', 'b', 'c']
        cellnames = [
            'cell_ctx_0001_005_2020_01_01',
            'cell_ctx_0001_010_2020_01_01',
            'cell_ctx_0001_015_2020_01_01'
        ]

        filtered_cells, filtered_names, indices = filter_by_index(cells, cellnames, 10, 10)

        assert len(filtered_cells) == 1
        assert filtered_cells == ['b']
        assert indices == [1]

    def test_filter_no_matches(self):
        """Test filtering with no matches."""
        from vhlib.CDM import filter_by_index

        cells = ['a', 'b']
        cellnames = [
            'cell_ctx_0001_001_2020_01_01',
            'cell_ctx_0001_002_2020_01_01'
        ]

        filtered_cells, filtered_names, indices = filter_by_index(cells, cellnames, 100, 200)

        assert len(filtered_cells) == 0
        assert indices == []


class TestFilterByReference:
    """Tests for filter_by_reference function."""

    def test_filter_within_range(self):
        """Test filtering cells within reference range."""
        from vhlib.CDM import filter_by_reference

        cells = ['cell_a', 'cell_b', 'cell_c', 'cell_d']
        cellnames = [
            'cell_ctx_0001_001_2020_01_01',
            'cell_ctx_0005_001_2020_01_01',
            'cell_ctx_0010_001_2020_01_01',
            'cell_ctx_0015_001_2020_01_01'
        ]

        filtered_cells, filtered_names, indices = filter_by_reference(cells, cellnames, 1, 10)

        assert len(filtered_cells) == 3
        assert len(filtered_names) == 3
        assert indices == [0, 1, 2]

    def test_filter_exact_ref(self):
        """Test filtering with exact reference."""
        from vhlib.CDM import filter_by_reference

        cells = ['a', 'b', 'c']
        cellnames = [
            'cell_ctx_0005_001_2020_01_01',
            'cell_ctx_0010_001_2020_01_01',
            'cell_ctx_0015_001_2020_01_01'
        ]

        filtered_cells, filtered_names, indices = filter_by_reference(cells, cellnames, 10, 10)

        assert len(filtered_cells) == 1
        assert filtered_cells == ['b']


class TestReadTrainingType:
    """Tests for read_trainingtype function."""

    def setup_method(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_read_bidirectional(self):
        """Test reading bidirectional training type."""
        from vhlib.CDM import read_trainingtype

        # Create trainingtype.txt
        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('Bidirectional\n')

        assoc = read_trainingtype(self.test_dir)

        assert len(assoc) == 1
        assert assoc[0]['type'] == 'Training Type'
        assert assoc[0]['data'] == 'bidirectional'

    def test_read_unidirectional(self):
        """Test reading unidirectional training type."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('uni\n')

        assoc = read_trainingtype(self.test_dir)

        assert assoc[0]['data'] == 'unidirectional'

    def test_read_flash(self):
        """Test reading flash training type."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('Flash\n')

        assoc = read_trainingtype(self.test_dir)

        assert assoc[0]['data'] == 'flash'

    def test_read_none(self):
        """Test reading none training type."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('None\n')

        assoc = read_trainingtype(self.test_dir)

        assert assoc[0]['data'] == 'none'

    def test_read_counterphase(self):
        """Test reading counterphase training type."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('CP\n')

        assoc = read_trainingtype(self.test_dir)

        assert assoc[0]['data'] == 'counterphase'

    def test_read_training_angle(self):
        """Test reading training angle."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('Bi\n')
        with open(os.path.join(self.test_dir, 'trainingangle.txt'), 'w') as f:
            f.write('45.0 135.0\n')

        assoc = read_trainingtype(self.test_dir)

        assert len(assoc) == 2
        angle_assoc = [a for a in assoc if a['type'] == 'Training Angle'][0]
        assert angle_assoc['data'] == [45.0, 135.0]

    def test_read_training_tf(self):
        """Test reading training temporal frequency."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('Bi\n')
        with open(os.path.join(self.test_dir, 'trainingtemporalfrequency.txt'), 'w') as f:
            f.write('4.0 8.0\n')

        assoc = read_trainingtype(self.test_dir)

        tf_assoc = [a for a in assoc if a['type'] == 'Training TF'][0]
        assert tf_assoc['data'] == [4.0, 8.0]

    def test_read_training_stim(self):
        """Test reading training stim."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('scrambled\n')
        with open(os.path.join(self.test_dir, 'trainingstim.txt'), 'w') as f:
            f.write('b5\n')

        assoc = read_trainingtype(self.test_dir)

        stim_assoc = [a for a in assoc if a['type'] == 'Training Stim'][0]
        assert stim_assoc['data'] == 'B5'

    def test_no_training_type_file(self):
        """Test when training type file doesn't exist."""
        from vhlib.CDM import read_trainingtype

        # Don't create any files
        assoc = read_trainingtype(self.test_dir)

        assert len(assoc) == 0

    def test_error_if_no_training_type_requested(self):
        """Test error raised when requested and file missing."""
        from vhlib.CDM import read_trainingtype

        with pytest.raises(FileNotFoundError):
            read_trainingtype(self.test_dir, ErrorIfNoTrainingType=True)

    def test_unknown_training_type_raises_error(self):
        """Test that unknown training type raises ValueError."""
        from vhlib.CDM import read_trainingtype

        with open(os.path.join(self.test_dir, 'trainingtype.txt'), 'w') as f:
            f.write('UnknownType\n')

        with pytest.raises(ValueError):
            read_trainingtype(self.test_dir)


class TestRepeatedMeasurementAssociates:
    """Tests for repeated_measurement_associates function."""

    def test_find_repeated_associates(self):
        """Test finding repeated measurement associates."""
        from vhlib.CDM import repeated_measurement_associates

        # Create a cell with associates
        cell = {
            'associates': [
                {'type': 'SP F0 TFOP0 TF Response curve', 'owner': 'test', 'data': 1, 'desc': 'test'},
                {'type': 'SP F0 TFOP1 TF Response curve', 'owner': 'test', 'data': 2, 'desc': 'test'},
                {'type': 'SP F0 TFOP3 TF Response curve', 'owner': 'test', 'data': 3, 'desc': 'test'},
            ]
        }

        n = repeated_measurement_associates(cell, 'SP F0 TFOP%d TF Response curve', 5)

        assert n == [0, 1, 3]

    def test_no_repeated_associates(self):
        """Test when no repeated associates found."""
        from vhlib.CDM import repeated_measurement_associates

        cell = {'associates': []}

        n = repeated_measurement_associates(cell, 'Test%d', 10)

        assert n == []
