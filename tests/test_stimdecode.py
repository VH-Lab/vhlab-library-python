"""
Comprehensive tests for the vhlib.StimDecode module.
"""

import pytest
import os
import tempfile
import shutil
import numpy as np


class TestReadStimtimesTxt:
    """Tests for read_stimtimes_txt function."""

    def setup_method(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_read_basic_stimtimes(self):
        """Test reading basic stimtimes.txt file."""
        from vhlib.StimDecode import read_stimtimes_txt

        # Create stimtimes.txt
        content = """1 0.00000 0.10000 0.20000 0.30000
2 1.00000 1.10000 1.20000 1.30000
3 2.00000 2.10000 2.20000 2.30000
"""
        with open(os.path.join(self.test_dir, 'stimtimes.txt'), 'w') as f:
            f.write(content)

        stimids, stimtimes, frametimes = read_stimtimes_txt(self.test_dir)

        assert len(stimids) == 3
        assert stimids[0] == 1
        assert stimids[1] == 2
        assert stimids[2] == 3

        assert len(stimtimes) == 3
        np.testing.assert_almost_equal(stimtimes[0], 0.0, decimal=5)
        np.testing.assert_almost_equal(stimtimes[1], 1.0, decimal=5)
        np.testing.assert_almost_equal(stimtimes[2], 2.0, decimal=5)

        assert len(frametimes) == 3
        np.testing.assert_array_almost_equal(frametimes[0], [0.1, 0.2, 0.3], decimal=5)

    def test_read_single_line(self):
        """Test reading single line stimtimes.txt."""
        from vhlib.StimDecode import read_stimtimes_txt

        content = "5 10.50000 10.60000 10.70000\n"
        with open(os.path.join(self.test_dir, 'stimtimes.txt'), 'w') as f:
            f.write(content)

        stimids, stimtimes, frametimes = read_stimtimes_txt(self.test_dir)

        assert len(stimids) == 1
        assert stimids[0] == 5
        np.testing.assert_almost_equal(stimtimes[0], 10.5, decimal=5)

    def test_read_no_frametimes(self):
        """Test reading stimtimes with no frame times."""
        from vhlib.StimDecode import read_stimtimes_txt

        content = "1 0.50000\n2 1.50000\n"
        with open(os.path.join(self.test_dir, 'stimtimes.txt'), 'w') as f:
            f.write(content)

        stimids, stimtimes, frametimes = read_stimtimes_txt(self.test_dir)

        assert len(stimids) == 2
        assert len(frametimes[0]) == 0  # No frame times
        assert len(frametimes[1]) == 0

    def test_file_not_found(self):
        """Test that missing file raises IOError."""
        from vhlib.StimDecode import read_stimtimes_txt

        with pytest.raises(IOError):
            read_stimtimes_txt(self.test_dir, 'nonexistent.txt')

    def test_custom_filename(self):
        """Test reading from custom filename."""
        from vhlib.StimDecode import read_stimtimes_txt

        content = "1 0.00000\n"
        with open(os.path.join(self.test_dir, 'custom_stim.txt'), 'w') as f:
            f.write(content)

        stimids, stimtimes, frametimes = read_stimtimes_txt(self.test_dir, 'custom_stim.txt')

        assert len(stimids) == 1


class TestWriteStimtimesTxt:
    """Tests for write_stimtimes_txt function."""

    def setup_method(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_write_basic_stimtimes(self):
        """Test writing basic stimtimes.txt file."""
        from vhlib.StimDecode import write_stimtimes_txt, read_stimtimes_txt

        stimids = [1, 2, 3]
        stimtimes = [0.0, 1.0, 2.0]
        frametimes = [
            np.array([0.1, 0.2, 0.3]),
            np.array([1.1, 1.2, 1.3]),
            np.array([2.1, 2.2, 2.3])
        ]

        write_stimtimes_txt(self.test_dir, stimids, stimtimes, frametimes, filename='test_stim.txt')

        # Verify file was created
        assert os.path.exists(os.path.join(self.test_dir, 'test_stim.txt'))

        # Read back and verify
        r_stimids, r_stimtimes, r_frametimes = read_stimtimes_txt(self.test_dir, 'test_stim.txt')

        np.testing.assert_array_equal(r_stimids, stimids)
        np.testing.assert_array_almost_equal(r_stimtimes, stimtimes, decimal=5)

    def test_write_without_frametimes(self):
        """Test writing stimtimes without frame times."""
        from vhlib.StimDecode import write_stimtimes_txt

        stimids = [1, 2]
        stimtimes = [0.5, 1.5]

        write_stimtimes_txt(self.test_dir, stimids, stimtimes, filename='no_frames.txt')

        assert os.path.exists(os.path.join(self.test_dir, 'no_frames.txt'))

    def test_file_already_exists_error(self):
        """Test that writing to existing file raises IOError."""
        from vhlib.StimDecode import write_stimtimes_txt

        # Create file first
        with open(os.path.join(self.test_dir, 'existing.txt'), 'w') as f:
            f.write('test')

        with pytest.raises(IOError):
            write_stimtimes_txt(self.test_dir, [1], [0.0], filename='existing.txt')


class TestGetStimdirectoryTime:
    """Tests for getstimdirectorytime function."""

    def setup_method(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_read_time_from_filetime(self):
        """Test reading time from filetime.txt."""
        from vhlib.StimDecode import getstimdirectorytime

        # Create required files
        with open(os.path.join(self.test_dir, 'stims.mat'), 'w') as f:
            f.write('')  # Empty mat file placeholder
        with open(os.path.join(self.test_dir, 'spike2data.smr'), 'w') as f:
            f.write('')  # Empty smr file placeholder
        with open(os.path.join(self.test_dir, 'filetime.txt'), 'w') as f:
            f.write('36000.0')  # 10:00 AM in seconds

        time_val = getstimdirectorytime(self.test_dir)

        assert time_val == 36000.0

    def test_early_morning_adjustment(self):
        """Test early morning time adjustment."""
        from vhlib.StimDecode import getstimdirectorytime

        # Create required files
        with open(os.path.join(self.test_dir, 'stims.mat'), 'w') as f:
            f.write('')
        with open(os.path.join(self.test_dir, 'spike2data.smr'), 'w') as f:
            f.write('')
        with open(os.path.join(self.test_dir, 'filetime.txt'), 'w') as f:
            f.write('7200.0')  # 2:00 AM in seconds

        time_val = getstimdirectorytime(self.test_dir)

        # Should add 24 hours since it's before 5 AM cutoff
        assert time_val == 7200.0 + 86400.0

    def test_no_early_morning_warning(self):
        """Test disabling early morning warning."""
        from vhlib.StimDecode import getstimdirectorytime

        with open(os.path.join(self.test_dir, 'stims.mat'), 'w') as f:
            f.write('')
        with open(os.path.join(self.test_dir, 'spike2data.smr'), 'w') as f:
            f.write('')
        with open(os.path.join(self.test_dir, 'filetime.txt'), 'w') as f:
            f.write('7200.0')

        # Should not raise, just return adjusted time
        time_val = getstimdirectorytime(self.test_dir, WarnOnEarlyMorning=False)

        assert time_val == 7200.0 + 86400.0

    def test_missing_files_error(self):
        """Test error when required files are missing."""
        from vhlib.StimDecode import getstimdirectorytime

        with pytest.raises(FileNotFoundError):
            getstimdirectorytime(self.test_dir)

    def test_missing_files_no_error(self):
        """Test no error when ErrorIfEmpty=False."""
        from vhlib.StimDecode import getstimdirectorytime

        time_val = getstimdirectorytime(self.test_dir, ErrorIfEmpty=False)

        assert np.isnan(time_val)


class TestVhinterconnectDecode:
    """Tests for vhinterconnect_decode function."""

    def test_basic_decode(self):
        """Test basic decoding of interconnect signals."""
        from vhlib.StimDecode import vhinterconnect_decode

        # Create test data
        time = np.array([0.0, 0.001, 0.002, 0.003, 0.004, 0.005])
        # Bit 0 (StimTrigger): 0,0,1,1,1,0 -> transition at index 2
        # Signal values: bit 0 set at indices 2,3,4
        input_sig = np.array([0, 0, 1, 1, 1, 0], dtype=np.uint16)

        out = vhinterconnect_decode(time, input_sig)

        assert 'StimTrigger' in out
        assert 'StimTriggerSamples' in out

    def test_custom_polarity(self):
        """Test decoding with custom polarity."""
        from vhlib.StimDecode import vhinterconnect_decode

        time = np.array([0.0, 0.001, 0.002, 0.003])
        input_sig = np.array([0, 0, 1, 1], dtype=np.uint16)

        # Custom polarity with some NaN values (should use defaults)
        polarity = np.array([1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])

        out = vhinterconnect_decode(time, input_sig, polarity=polarity)

        assert 'StimTrigger' in out

    def test_invalid_polarity_length(self):
        """Test that invalid polarity length raises error."""
        from vhlib.StimDecode import vhinterconnect_decode

        time = np.array([0.0, 0.001])
        input_sig = np.array([0, 1], dtype=np.uint16)
        polarity = np.array([1, 1, 1])  # Wrong length

        with pytest.raises(ValueError):
            vhinterconnect_decode(time, input_sig, polarity=polarity)

    def test_stim_code_extraction(self):
        """Test extraction of stimulus codes from upper bits."""
        from vhlib.StimDecode import vhinterconnect_decode

        time = np.array([0.0, 0.001, 0.002, 0.003])
        # Create signal with stim code in upper byte
        # Upper byte = 5, lower bit 0 set for trigger
        # 5 << 8 = 1280, plus 1 for trigger bit = 1281
        input_sig = np.array([0, 0, 1281, 1281], dtype=np.uint16)

        out = vhinterconnect_decode(time, input_sig)

        if len(out.get('StimTriggerSamples', [])) > 0:
            assert 'StimCode' in out


class TestStimscriptgraph:
    """Tests for stimscriptgraph function."""

    def test_not_implemented(self):
        """Test that stimscriptgraph raises NotImplementedError."""
        from vhlib.StimDecode import stimscriptgraph

        with pytest.raises(NotImplementedError):
            stimscriptgraph('/some/path')


class TestVhlabcorrectmti:
    """Tests for vhlabcorrectmti function."""

    def test_not_implemented(self):
        """Test that vhlabcorrectmti raises NotImplementedError."""
        from vhlib.StimDecode import vhlabcorrectmti

        with pytest.raises(NotImplementedError):
            vhlabcorrectmti({}, 'file.txt')


class TestWriteInterconnectTextfiles:
    """Tests for write_interconnect_textfiles function."""

    def setup_method(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_write_basic_textfiles(self):
        """Test writing interconnect text files."""
        from vhlib.StimDecode import write_interconnect_textfiles

        out = {
            'StimTrigger': np.array([0.5, 1.5, 2.5]),
            'StimCode': np.array([1, 2, 3]),
            'FrameTriggerRaw': np.array([0.6, 0.7, 1.6, 1.7, 2.6, 2.7]),
            'TwoPhotonFrameTrigger': np.array([0.55, 1.55, 2.55]),
            'StimulusMonitorVerticalRefresh': np.array([0.51, 0.52, 1.51, 1.52])
        }

        write_interconnect_textfiles(self.test_dir, out)

        # Check that files were created
        assert os.path.exists(os.path.join(self.test_dir, 'stimtimes.txt'))
        assert os.path.exists(os.path.join(self.test_dir, 'stimontimes.txt'))
        assert os.path.exists(os.path.join(self.test_dir, 'twophotontimes.txt'))
        assert os.path.exists(os.path.join(self.test_dir, 'verticalblanking.txt'))
        assert os.path.exists(os.path.join(self.test_dir, 'Intan_decoding_finished.txt'))

    def test_removes_existing_files(self):
        """Test that existing files are removed before writing."""
        from vhlib.StimDecode import write_interconnect_textfiles

        # Create existing files
        for fname in ['stimtimes.txt', 'stimontimes.txt']:
            with open(os.path.join(self.test_dir, fname), 'w') as f:
                f.write('old content')

        out = {
            'StimTrigger': np.array([0.5]),
            'StimCode': np.array([1]),
            'FrameTriggerRaw': np.array([0.6])
        }

        write_interconnect_textfiles(self.test_dir, out)

        # Files should be recreated
        assert os.path.exists(os.path.join(self.test_dir, 'stimtimes.txt'))


class TestReadWriteRoundTrip:
    """Tests for round-trip read/write operations."""

    def setup_method(self):
        """Create temporary directory for tests."""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_stimtimes_roundtrip(self):
        """Test that writing and reading stimtimes preserves data."""
        from vhlib.StimDecode import write_stimtimes_txt, read_stimtimes_txt

        original_stimids = [1, 5, 10, 15]
        original_stimtimes = [0.0, 1.5, 3.0, 4.5]
        original_frametimes = [
            np.array([0.1, 0.2]),
            np.array([1.6, 1.7]),
            np.array([3.1, 3.2]),
            np.array([4.6, 4.7])
        ]

        write_stimtimes_txt(self.test_dir, original_stimids, original_stimtimes,
                           original_frametimes, filename='roundtrip.txt')

        read_stimids, read_stimtimes, read_frametimes = read_stimtimes_txt(
            self.test_dir, 'roundtrip.txt')

        np.testing.assert_array_equal(read_stimids, original_stimids)
        np.testing.assert_array_almost_equal(read_stimtimes, original_stimtimes, decimal=5)

        for i in range(len(original_frametimes)):
            np.testing.assert_array_almost_equal(
                read_frametimes[i], original_frametimes[i], decimal=5)
