import math

__all__=["get_clicked_values"]

def get_clicked_values(xdata, ydata, fitsObj, imgObj, hdul):
    """ Update image object attributes
    :param list xdata: list of xvalues
    :param list ydata: list of yvalues
    :param object fitsObj: fitsObj current object
    :param object imgObj: imgObj current object
    :return object imgObj
    """
    xdataRound = set_round_value(xdata)
    ydataRound = set_round_value(ydata)

    xValueTransformed = int(xdataRound-fitsObj.fitsXCenter*\
                            fitsObj.shidXValue)
    yValueTransformed = int(ydataRound-fitsObj.fitsYCenter*\
                            fitsObj.shidYValue)

    imgObj.xValues = hdul[1].data[fitsObj.currIntegration,
                    fitsObj.currFrame,yValueTransformed,\
                    0:fitsObj.maxXAxis]

    imgObj.yValues = hdul[1].data[fitsObj.currIntegration,
                    fitsObj.currFrame, \
                    0:fitsObj.maxYAxis,xValueTransformed]

#Get z value along time
    imgObj.zValues = hdul[1].data[:,:,yValueTransformed,\
                        xValueTransformed]

    return xValueTransformed, yValueTransformed, imgObj

def set_round_value(data):
    if data %1 >= 0.5:
        return int(math.ceil(data))
    else:
        return int(round(data))


