"""
Comprehensive tests for the vhlib.md module.
"""

import pytest
import numpy as np


class TestMeasuredData:
    """Tests for MeasuredData class."""

    def test_create_basic(self):
        """Test creating a basic MeasuredData object."""
        from vhlib.md import MeasuredData

        intervals = [[0, 1], [2, 3], [4, 5]]
        md = MeasuredData(intervals, 'Long description', 'Brief')

        assert md.intervals == intervals
        assert md.description_long == 'Long description'
        assert md.description_brief == 'Brief'
        assert len(md.associates) == 0

    def test_create_with_numpy_intervals(self):
        """Test creating MeasuredData with numpy array intervals."""
        from vhlib.md import MeasuredData

        intervals = np.array([[0, 1], [2, 3]])
        md = MeasuredData(intervals)

        assert md.intervals.shape == (2, 2)

    def test_create_with_empty_intervals(self):
        """Test creating MeasuredData with empty intervals."""
        from vhlib.md import MeasuredData

        md = MeasuredData([])

        assert len(md.intervals) == 0

    def test_invalid_intervals_shape(self):
        """Test that invalid intervals shape raises error."""
        from vhlib.md import MeasuredData

        with pytest.raises(ValueError):
            MeasuredData([[1, 2, 3]])  # 3 columns instead of 2


class TestMeasuredDataAssociate:
    """Tests for MeasuredData.associate method."""

    def test_add_associate(self):
        """Test adding an associate."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('test_type', 'test_owner', {'value': 42}, 'test description')

        assert md.numassociates() == 1
        assoc = md.getassociate(0)
        assert assoc['type'] == 'test_type'
        assert assoc['owner'] == 'test_owner'
        assert assoc['data'] == {'value': 42}
        assert assoc['desc'] == 'test description'

    def test_add_associate_dict(self):
        """Test adding an associate using dict format."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        assoc_dict = {
            'type': 'dict_type',
            'owner': 'dict_owner',
            'data': [1, 2, 3],
            'desc': 'dict description'
        }
        md.associate(assoc_dict)

        assert md.numassociates() == 1
        assoc = md.getassociate(0)
        assert assoc['type'] == 'dict_type'

    def test_replace_existing_associate(self):
        """Test that adding duplicate associate replaces it."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type1', 'owner1', 'data2', 'desc1')

        assert md.numassociates() == 1
        assoc = md.getassociate(0)
        assert assoc['data'] == 'data2'

    def test_add_multiple_associates(self):
        """Test adding multiple different associates."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner2', 'data2', 'desc2')
        md.associate('type3', 'owner3', 'data3', 'desc3')

        assert md.numassociates() == 3

    def test_associate_returns_self(self):
        """Test that associate returns self for chaining."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        result = md.associate('type', 'owner', 'data', 'desc')

        assert result is md

    def test_associate_invalid_type(self):
        """Test that non-string type raises error."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])

        with pytest.raises(ValueError):
            md.associate(123, 'owner', 'data', 'desc')

    def test_associate_invalid_owner(self):
        """Test that non-string owner raises error."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])

        with pytest.raises(ValueError):
            md.associate('type', 123, 'data', 'desc')

    def test_associate_invalid_description(self):
        """Test that non-string description raises error."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])

        with pytest.raises(ValueError):
            md.associate('type', 'owner', 'data', 123)


class TestMeasuredDataFindassociate:
    """Tests for MeasuredData.findassociate method."""

    def test_find_by_type(self):
        """Test finding associate by type."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner2', 'data2', 'desc2')

        matches, indices = md.findassociate('type1', '', '')

        assert len(matches) == 1
        assert matches[0]['type'] == 'type1'
        assert indices == [0]

    def test_find_by_owner(self):
        """Test finding associate by owner."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner1', 'data2', 'desc2')
        md.associate('type3', 'owner2', 'data3', 'desc3')

        matches, indices = md.findassociate('', 'owner1', '')

        assert len(matches) == 2
        assert indices == [0, 1]

    def test_find_by_description(self):
        """Test finding associate by description."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner2', 'data2', 'desc1')

        matches, indices = md.findassociate('', '', 'desc1')

        assert len(matches) == 2

    def test_find_by_multiple_criteria(self):
        """Test finding associate by multiple criteria."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type1', 'owner2', 'data2', 'desc1')
        md.associate('type2', 'owner1', 'data3', 'desc1')

        matches, indices = md.findassociate('type1', 'owner1', 'desc1')

        assert len(matches) == 1
        assert indices == [0]

    def test_find_all_with_empty_criteria(self):
        """Test finding all associates with empty criteria."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner2', 'data2', 'desc2')

        matches, indices = md.findassociate('', '', '')

        assert len(matches) == 2
        assert indices == [0, 1]

    def test_find_no_matches(self):
        """Test finding with no matches."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')

        matches, indices = md.findassociate('nonexistent', '', '')

        assert len(matches) == 0
        assert indices == []


class TestMeasuredDataDisassociate:
    """Tests for MeasuredData.disassociate method."""

    def test_disassociate_single(self):
        """Test removing single associate."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner2', 'data2', 'desc2')

        md.disassociate(0)

        assert md.numassociates() == 1
        assert md.getassociate(0)['type'] == 'type2'

    def test_disassociate_multiple(self):
        """Test removing multiple associates."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner2', 'data2', 'desc2')
        md.associate('type3', 'owner3', 'data3', 'desc3')

        md.disassociate([0, 2])

        assert md.numassociates() == 1
        assert md.getassociate(0)['type'] == 'type2'

    def test_disassociate_returns_self(self):
        """Test that disassociate returns self."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')

        result = md.disassociate(0)

        assert result is md

    def test_disassociate_invalid_index(self):
        """Test that invalid index is handled gracefully."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')

        # Should not raise, just ignore invalid index
        md.disassociate(100)

        assert md.numassociates() == 1


class TestMeasuredDataAssociates2struct:
    """Tests for MeasuredData.associates2struct method."""

    def test_basic_conversion(self):
        """Test converting associates to struct."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('Type One', 'owner', 'data1', 'desc')
        md.associate('Type Two', 'owner', 'data2', 'desc')

        s = md.associates2struct()

        assert s['Type_One'] == 'data1'
        assert s['Type_Two'] == 'data2'

    def test_empty_associates(self):
        """Test converting empty associates."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])

        s = md.associates2struct()

        assert s == {}


class TestMeasuredDataGetassociate:
    """Tests for MeasuredData.getassociate method."""

    def test_get_single(self):
        """Test getting single associate by index."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')

        assoc = md.getassociate(0)

        assert assoc['type'] == 'type1'

    def test_get_multiple(self):
        """Test getting multiple associates by indices."""
        from vhlib.md import MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')
        md.associate('type2', 'owner2', 'data2', 'desc2')
        md.associate('type3', 'owner3', 'data3', 'desc3')

        assocs = md.getassociate([0, 2])

        assert len(assocs) == 2
        assert assocs[0]['type'] == 'type1'
        assert assocs[1]['type'] == 'type3'


class TestModuleLevelFunctions:
    """Tests for module-level functions in vhlib.md."""

    def test_findassociate_with_dict(self):
        """Test findassociate with dict input."""
        from vhlib.md import findassociate

        cell = {
            'associates': [
                {'type': 'type1', 'owner': 'owner1', 'data': 'data1', 'desc': 'desc1'},
                {'type': 'type2', 'owner': 'owner2', 'data': 'data2', 'desc': 'desc2'},
            ]
        }

        matches, indices = findassociate(cell, 'type1', '', '')

        assert len(matches) == 1
        assert indices == [0]

    def test_findassociate_with_measureddata(self):
        """Test findassociate with MeasuredData input."""
        from vhlib.md import findassociate, MeasuredData

        md = MeasuredData([[0, 1]])
        md.associate('type1', 'owner1', 'data1', 'desc1')

        matches, indices = findassociate(md, 'type1', '', '')

        assert len(matches) == 1

    def test_findassociate_empty_associates(self):
        """Test findassociate with empty associates list."""
        from vhlib.md import findassociate

        cell = {'associates': []}

        matches, indices = findassociate(cell, 'type1', '', '')

        assert matches == []
        assert indices == []

    def test_findassociate_invalid_input(self):
        """Test findassociate with invalid input."""
        from vhlib.md import findassociate

        with pytest.raises(ValueError):
            findassociate("invalid", 'type', '', '')

    def test_associate_with_dict(self):
        """Test associate with dict input."""
        from vhlib.md import associate

        cell = {'associates': []}

        result = associate(cell, 'type1', 'owner1', 'data1', 'desc1')

        assert len(result['associates']) == 1
        assert result['associates'][0]['type'] == 'type1'

    def test_associate_with_dict_struct(self):
        """Test associate with dict struct input."""
        from vhlib.md import associate

        cell = {'associates': []}
        assoc_struct = {
            'type': 'type1',
            'owner': 'owner1',
            'data': 'data1',
            'desc': 'desc1'
        }

        result = associate(cell, assoc_struct)

        assert len(result['associates']) == 1

    def test_associate_replaces_existing(self):
        """Test that associate replaces existing matching associate."""
        from vhlib.md import associate

        cell = {
            'associates': [
                {'type': 'type1', 'owner': 'owner1', 'data': 'old_data', 'desc': 'desc1'}
            ]
        }

        result = associate(cell, 'type1', 'owner1', 'new_data', 'desc1')

        assert len(result['associates']) == 1
        assert result['associates'][0]['data'] == 'new_data'

    def test_disassociate_with_dict(self):
        """Test disassociate with dict input."""
        from vhlib.md import disassociate

        cell = {
            'associates': [
                {'type': 'type1', 'owner': 'owner1', 'data': 'data1', 'desc': 'desc1'},
                {'type': 'type2', 'owner': 'owner2', 'data': 'data2', 'desc': 'desc2'}
            ]
        }

        result = disassociate(cell, 0)

        assert len(result['associates']) == 1
        assert result['associates'][0]['type'] == 'type2'

    def test_disassociate_multiple_indices(self):
        """Test disassociate with multiple indices."""
        from vhlib.md import disassociate

        cell = {
            'associates': [
                {'type': 'type1', 'owner': 'owner1', 'data': 'data1', 'desc': 'desc1'},
                {'type': 'type2', 'owner': 'owner2', 'data': 'data2', 'desc': 'desc2'},
                {'type': 'type3', 'owner': 'owner3', 'data': 'data3', 'desc': 'desc3'}
            ]
        }

        result = disassociate(cell, [0, 2])

        assert len(result['associates']) == 1
        assert result['associates'][0]['type'] == 'type2'

    def test_associate_all(self):
        """Test associate_all function."""
        from vhlib.md import associate_all

        cells = [
            {'associates': []},
            {'associates': []},
        ]
        assoclist = [
            {'type': 'type1', 'owner': 'owner1', 'data': 'data1', 'desc': 'desc1'},
            {'type': 'type2', 'owner': 'owner2', 'data': 'data2', 'desc': 'desc2'},
        ]

        result = associate_all(cells, assoclist)

        assert len(result) == 2
        assert len(result[0]['associates']) == 2
        assert len(result[1]['associates']) == 2

    def test_associate_all_single_cell(self):
        """Test associate_all with single cell (not list)."""
        from vhlib.md import associate_all

        cell = {'associates': []}
        assoclist = [
            {'type': 'type1', 'owner': 'owner1', 'data': 'data1', 'desc': 'desc1'},
        ]

        result = associate_all(cell, assoclist)

        assert len(result['associates']) == 1


class TestSpikeTriggeredAverage:
    """Tests for spiketriggeredaverage function."""

    def test_basic_sta(self):
        """Test basic spike-triggered average calculation."""
        from vhlib.md import spiketriggeredaverage

        # Create test signal
        signal_t = np.arange(0, 1, 0.001)  # 1 second, 1kHz
        signal = np.sin(2 * np.pi * 10 * signal_t)  # 10 Hz sine wave

        # Spike times - ensure they have enough room for the window (50ms before and after)
        spiketimes = [0.1, 0.2, 0.3, 0.4, 0.5]

        sta, t_sta, count = spiketriggeredaverage(
            spiketimes, signal, signal_t, [-0.05, 0.05])

        assert count == 5
        assert len(sta) == len(t_sta)
        assert t_sta[0] < 0  # Starts before spike
        assert t_sta[-1] > 0  # Ends after spike

    def test_sta_no_spikes_in_range(self):
        """Test STA with no spikes in valid range."""
        from vhlib.md import spiketriggeredaverage

        signal_t = np.arange(0, 1, 0.001)
        signal = np.ones_like(signal_t)

        # Spikes outside signal range
        spiketimes = [2.0, 3.0]

        sta, t_sta, count = spiketriggeredaverage(
            spiketimes, signal, signal_t, [-0.05, 0.05])

        assert count == 0

    def test_sta_single_spike(self):
        """Test STA with single spike."""
        from vhlib.md import spiketriggeredaverage

        signal_t = np.arange(0, 1, 0.001)
        signal = np.zeros_like(signal_t)
        signal[500] = 1.0  # Impulse at t=0.5

        spiketimes = [0.5]

        sta, t_sta, count = spiketriggeredaverage(
            spiketimes, signal, signal_t, [-0.01, 0.01])

        assert count == 1
        # STA should have peak near center
        center_idx = len(sta) // 2
        assert sta[center_idx] > 0

    def test_sta_short_signal(self):
        """Test STA with very short signal."""
        from vhlib.md import spiketriggeredaverage

        signal_t = np.array([0])  # Single sample
        signal = np.array([1.0])

        spiketimes = [0.0]

        sta, t_sta, count = spiketriggeredaverage(
            spiketimes, signal, signal_t, [-0.01, 0.01])

        # Should return None or empty due to insufficient data
        assert sta is None or count == 0

    def test_sta_window_larger_than_signal(self):
        """Test STA when window is larger than available signal."""
        from vhlib.md import spiketriggeredaverage

        signal_t = np.arange(0, 0.1, 0.001)  # 100ms
        signal = np.ones_like(signal_t)

        spiketimes = [0.05]

        sta, t_sta, count = spiketriggeredaverage(
            spiketimes, signal, signal_t, [-0.1, 0.1])  # 200ms window

        # Spike at 0.05 can't have 100ms before it in 100ms signal
        assert count == 0
