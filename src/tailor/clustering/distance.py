
import pandas as pd
import scipy.interpolate as spi


def euclidean(a, b):
    '''returns the mean absolute difference'''
    return abs(a - b).mean()


def derivative_euclidean(a, b, smooth=1):
    '''returns the mean absolute difference between the interpolation derivatives'''
    # creating the interpolated derivative for a
    xa = a.index
    ya = a.values
    sa = spi.UnivariateSpline(xa, ya, s=smooth)
    sa = sa.derivative()
    # creating the interpolated derivative for b
    xb = b.index
    yb = b.values
    sb = spi.UnivariateSpline(xb, yb, s=smooth)
    sb = sb.derivative
    # calculating new Series
    a_d = pd.Series(data=sa(xa), index=xa)
    b_d = pd.Series(data=sb(xb), index=xb)
    return abs(a_d - b_d).mean()


def dynamic_time_warp(a, b):
    return None
