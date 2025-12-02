from .add_testdir_info import add_testdir_info

def findtestdirinfo(ds, tag):
    """
    Find a test directory record from testdirinfo.txt file

    :param ds: vlt.dirstruct object
    :param tag: directory label to look for (without ' test')
    :return: directory name string or None if not found
    """

    # In MATLAB: assoc = add_testdir_info(ds);
    # My python impl returns (assoc, cells) tuple.
    assoc, _ = add_testdir_info(ds)

    target_type = f"{tag} test"

    for item in assoc:
        if item.get('type') == target_type:
            return item.get('data')

    return None
