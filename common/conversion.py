import numpy as np

DEFAULT_INT = np.int16
DEFAULT_FLOAT = np.float32


def convert(signal: np.ndarray, dtype: np.dtype = DEFAULT_INT):
    """Convert signal to selected dtype."""
    if is_int(dtype):
        return convert_to_int(signal, dtype)
    elif is_float(dtype):
        return convert_to_float(signal, dtype)
    else:
        raise TypeError("Signal dtype isn't int nor float")


def convert_to_int(signal: np.ndarray, dtype: np.dtype = DEFAULT_INT):
    """Convert signal to selected int dtype."""
    if is_int(signal.dtype):
        return convert_int_to_int(signal, dtype)
    elif is_float(signal.dtype):
        return convert_float_to_int(signal, dtype)
    else:
        raise TypeError("Signal dtype isn't int nor float")


def convert_to_float(signal: np.ndarray, dtype: np.dtype = DEFAULT_INT):
    """Convert signal to selected float dtype."""
    if is_int(signal.dtype):
        return convert_int_to_float(signal, dtype)
    elif is_float(signal.dtype):
        return convert_float_to_float(signal, dtype)
    else:
        raise TypeError("Signal dtype isn't int nor float")


def convert_float_to_float(
    signal: np.ndarray, dtype: np.dtype = DEFAULT_FLOAT
):
    """Convert float signal to selected float dtype."""
    return signal.astype(dtype)


def convert_int_to_int(signal: np.ndarray, dtype: np.dtype = DEFAULT_INT):
    """Convert int signal to selected int dtype."""
    float_signal = convert_int_to_float(signal)
    return convert_float_to_int(float_signal, dtype)


def convert_int_to_float(signal: np.ndarray, dtype: np.dtype = DEFAULT_FLOAT):
    """Convert int signal to selected float dtype."""
    signal_dtype_max = np.iinfo(signal.dtype).max
    return (signal / signal_dtype_max).astype(dtype)


def convert_float_to_int(signal: np.ndarray, dtype: np.dtype = DEFAULT_INT):
    """Convert float signal to selected int dtype."""
    dtype_max = np.iinfo(dtype).max
    return (signal * dtype_max).astype(dtype)


def is_int(dtype):
    """Check if dtype is int."""
    return np.issubdtype(dtype, np.integer)


def is_float(dtype):
    """Check if dtype is float."""
    return np.issubdtype(dtype, np.floating)
