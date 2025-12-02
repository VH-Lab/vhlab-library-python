import os

def read_trainingtype(ds, **kwargs):
    """
    Read the trainingtype.txt file and prepare data to associate with cells

    :param ds: vlt.file.dirstruct object
    :param kwargs:
        ErrorIfNoTrainingType (bool, default False)
        ErrorIfNoTrainingAngle (bool, default False)
        ErrorIfNoTF (bool, default False)
        ErrorIfNoTrainingStim (bool, default False)
    :return: list of associate dictionaries
    """

    error_if_no_training_type = kwargs.get('ErrorIfNoTrainingType', False)
    error_if_no_training_angle = kwargs.get('ErrorIfNoTrainingAngle', False)
    error_if_no_tf = kwargs.get('ErrorIfNoTF', False)
    error_if_no_training_stim = kwargs.get('ErrorIfNoTrainingStim', False)

    assoc = []

    try:
        pathname = ds.getpathname()
    except AttributeError:
        if isinstance(ds, str):
            pathname = ds
        else:
            raise ValueError("ds must have getpathname method or be a string path")

    filename = os.path.join(pathname, 'trainingtype.txt')

    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            content = f.readline().strip()

        type_str = ''
        content_lower = content.lower()
        if content_lower == 'none':
            type_str = 'none'
        elif content_lower == 'flash':
            type_str = 'flash'
        elif content_lower in ['bi', 'bidirectional', 'bi-directional']:
            type_str = 'bidirectional'
        elif content_lower in ['uni', 'unidirectional', 'uni-directional']:
            type_str = 'unidirectional'
        elif content_lower in ['counterphase', 'cp', 'counter-phase']:
            type_str = 'counterphase'
        elif content_lower == 'scrambled':
            type_str = 'scrambled'
        elif content_lower in ['multi-dimensional', 'multidimensional']:
            type_str = 'multidimensional'
        elif content_lower in ['constant', 'const']:
            type_str = 'constant'
        else:
            raise ValueError(f"Unknown type in trainingtype.txt: {content}.")

        assoc.append({
            'type': 'Training Type',
            'owner': 'read_trainingtype',
            'data': type_str,
            'desc': 'type of visual training that was used'
        })
    else:
        if error_if_no_training_type:
             raise FileNotFoundError(f"No trainingtype.txt file in {pathname}; error was requested if no file exists.")

    filename = os.path.join(pathname, 'trainingangle.txt')
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            try:
                angles = [float(x) for x in f.read().split()]
            except ValueError:
                angles = []

        assoc.append({
            'type': 'Training Angle',
            'owner': 'read_trainingtype',
            'data': angles,
            'desc': 'angles used for visual training'
        })
    else:
        if error_if_no_training_angle:
             raise FileNotFoundError(f"No trainingangle.txt file in {pathname}; error was requested if no file exists.")

    filename = os.path.join(pathname, 'trainingtemporalfrequency.txt')
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
             try:
                tfs = [float(x) for x in f.read().split()]
             except ValueError:
                tfs = []

        assoc.append({
            'type': 'Training TF',
            'owner': 'read_trainingtype',
            'data': tfs,
            'desc': 'temporal frequencies used for visual training'
        })
    else:
        if error_if_no_tf:
             raise FileNotFoundError(f"No trainingtemporalfrequency.txt file in {pathname}; error was requested if no file exists.")

    filename = os.path.join(pathname, 'trainingstim.txt')
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            content = f.readline().strip().upper()

        assoc.append({
            'type': 'Training Stim',
            'owner': 'read_trainingtype',
            'data': content,
            'desc': 'ID of scrambled stimulus'
        })
    else:
        if error_if_no_training_stim:
             raise FileNotFoundError(f"No trainingstim.txt file in {pathname}; error was requested if no file exists.")

    return assoc
