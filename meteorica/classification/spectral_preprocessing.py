"""
Spectral preprocessing for NIR reflectance spectroscopy.
"""

import numpy as np
from typing import Tuple, Optional


def preprocess_spectrum(wavelengths: np.ndarray, 
                        reflectance: np.ndarray,
                        normalize_at: float = 0.55) -> np.ndarray:
    """
    Preprocess NIR spectrum for CNN classifier.
    
    Args:
        wavelengths: Wavelength array (μm)
        reflectance: Reflectance values
        normalize_at: Wavelength for normalization (μm)
        
    Returns:
        Preprocessed spectrum
    """
    # Remove continuum
    spectrum = remove_continuum(wavelengths, reflectance)
    
    # Apply Savitzky-Golay smoothing
    spectrum = savgol_smooth(spectrum)
    
    # Normalize
    spectrum = normalize_spectrum(spectrum, wavelengths, normalize_at)
    
    return spectrum


def remove_continuum(wavelengths: np.ndarray, 
                    reflectance: np.ndarray) -> np.ndarray:
    """
    Remove continuum by dividing by convex hull.
    
    Args:
        wavelengths: Wavelength array
        reflectance: Reflectance values
        
    Returns:
        Continuum-removed spectrum
    """
    from scipy.spatial import ConvexHull
    
    points = np.column_stack([wavelengths, reflectance])
    hull = ConvexHull(points)
    
    # Find hull vertices in order of increasing wavelength
    hull_points = points[hull.vertices]
    hull_points = hull_points[np.argsort(hull_points[:, 0])]
    
    # Interpolate hull at all wavelengths
    hull_interp = np.interp(wavelengths, hull_points[:, 0], hull_points[:, 1])
    
    # Avoid division by zero
    hull_interp = np.maximum(hull_interp, 1e-6)
    
    return reflectance / hull_interp


def savgol_smooth(spectrum: np.ndarray, 
                  window: int = 11, 
                  polyorder: int = 3) -> np.ndarray:
    """
    Apply Savitzky-Golay smoothing.
    
    Args:
        spectrum: Input spectrum
        window: Window size
        polyorder: Polynomial order
        
    Returns:
        Smoothed spectrum
    """
    from scipy.signal import savgol_filter
    
    if len(spectrum) < window:
        return spectrum
    
    return savgol_filter(spectrum, window, polyorder)


def normalize_spectrum(spectrum: np.ndarray, 
                       wavelengths: np.ndarray,
                       norm_wavelength: float = 0.55) -> np.ndarray:
    """
    Normalize spectrum at specified wavelength.
    
    Args:
        spectrum: Input spectrum
        wavelengths: Wavelength array
        norm_wavelength: Wavelength for normalization (μm)
        
    Returns:
        Normalized spectrum
    """
    # Find index closest to normalization wavelength
    idx = np.argmin(np.abs(wavelengths - norm_wavelength))
    norm_value = spectrum[idx]
    
    if norm_value > 0:
        return spectrum / norm_value
    else:
        return spectrum


def add_realistic_noise(spectrum: np.ndarray, 
                        noise_level: float = 0.002) -> np.ndarray:
    """
    Add Gaussian noise for data augmentation.
    
    Args:
        spectrum: Input spectrum
        noise_level: Standard deviation of noise
        
    Returns:
        Spectrum with added noise
    """
    noise = np.random.normal(0, noise_level, spectrum.shape)
    return spectrum + noise


def shift_wavelengths(wavelengths: np.ndarray, 
                      shift: float = 0.005) -> np.ndarray:
    """
    Apply small wavelength shift for data augmentation.
    
    Args:
        wavelengths: Wavelength array
        shift: Shift amount (μm)
        
    Returns:
        Shifted wavelengths
    """
    return wavelengths + np.random.uniform(-shift, shift)
