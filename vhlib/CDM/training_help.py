def trainingtype():
    """
    Help function for the trainingtype.txt text file

    In an experiment directory, the 'trainingtype.txt' file lives in the root
    directory. It indicates what type of training was used for that experiment. It should be
    a string with the following values (the string values are listed here in single quotes, but
    single quotes should not be used in the file):

    Capitalization is unimportant here.

    Types:
    ------------------------------------------------------------------------------------
    'Bi','Bi-directional','Bidirectional'   |  Bidirectional training
    'Uni','Uni-directional','Unidirectional'|  Unidirectional training
    'Flash'                                 |  Flash training
    'Scrambled'                             |  Scrambled training
    'Multidirectional'                      |  Multi-directional training
    'Counterphase','CP','Counter-Phase'     |  Counterphase training
    'None'                                  |  None
    """
    print(trainingtype.__doc__)

def trainingangle():
    """
    Help function for the trainingangle.txt file

    trainingangle.txt is a text file that can exist in the root directory of
    an experiment directory.  It should contain a text representation of 1 or 2 (or more)
    numbers that indicate the training angles used (either in orientation or direction space).
    """
    print(trainingangle.__doc__)

def trainingstim():
    """
    Help function for the trainingstim.txt text file

    In an experiment directory, the 'trainingstim.txt' file lives in the root
    directory. It indicates what stim id of scrambled training was used for that experiment. It should be
    a string with one of the following values:
         b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,...
         a1,a2,a3,a4,a5,a6,a7,a8,...
         s1,s2,s3,s4,s5,s6,s7,s8,s9,s10

    Capitalization is unimportant here.
    """
    print(trainingstim.__doc__)

def trainingtemporalfrequency():
    """
    Help function for the trainingtemporalfrequency.txt file

    trainingtemporalfrequency.txt is a text file that can exist in the root directory of
    an experiment directory.  It should contain a text representation of 1 or 2 (or more)
    numbers that indicate the training temporalfrequencies used.
    """
    print(trainingtemporalfrequency.__doc__)
