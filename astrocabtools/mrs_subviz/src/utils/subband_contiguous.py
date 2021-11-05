__all__=["subband_contiguous"]


def subband_contiguous(subbandList):
    """ Check if the subbands of the list are contiguous
    :param list subbandList: subbands selected
    :return: Mool
    """

    contiguousSubbands = [["1S","1M"],["1M","1L"],["1L","2S"],["2S","2M"],["2M","2L"],
                          ["2L","3S"],["3S","3M"],["3M","3L"],["3L","4S"],["4S", "4M"], ["4M","4L"]]

    for i in range(0, len(subbandList)-1):
        if not [subbandList[i], subbandList[i+1]] in contiguousSubbands:
            return False

    return True
