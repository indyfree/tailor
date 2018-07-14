import pandas as pd
import scipy.interpolate as spi


def absolute(a, b):
    '''returns the mean absolute difference'''
    return abs(a - b).mean()


def interpolate_function(a, degree=1, smooth=1):
    '''returns an interpolated function based on a Series'''
    return spi.UnivariateSpline(a.index, a.values, s=smooth, k=degree)


def derivative_euclidean(a, b, degree=1, smooth=1):
    '''returns the mean absolute difference between the interpolation derivatives'''
    # creating the interpolated derivatives
    da = interpolate_function(a, degree, smooth).derivative()
    db = interpolate_function(b, degree, smooth).derivative()
    # create new Series
    # da(a.index) takes the index as x and calculates new y values
    # this way only y for existing x are calculated
    a_new = pd.Series(data=da(a.index), index=a.index)
    b_new = pd.Series(data=db(b.index), index=b.index)
    return absolute(a_new, b_new)


def dynamic_time_warp(a, b):
    return None
