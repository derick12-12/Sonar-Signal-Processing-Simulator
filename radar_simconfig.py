"radar system parameters & constants by derick eno"



import numpy as np

# physical constants
SPEED_OF_LIGHT = 3e8  # m/s

# radar transmitter parameters
CARRIER_FREQUENCY = 10e9  # 10 GHz (X-band)
PULSE_WIDTH = 1e-6  # 1 microsecond
PRF = 1000  # pulse repetition frequency (Hz)
PRI = 1 / PRF
TRANSMIT_POWER = 1e3  # 1 kW

# receiver parameters
SAMPLING_FREQUENCY = 100e9  # 100 GHz
NOISE_FIGURE_DB = 5  # receiver noise figure
SYSTEM_TEMPERATURE = 290  # kelvin
BOLTZMANN_CONSTANT = 1.38e-23  # J/K

# signal processing parameters
DEFAULT_THRESHOLD = 0.5  # normalized detection threshold
SAMPLES_PER_PULSE = int(PULSE_WIDTH * SAMPLING_FREQUENCY)
TIME_PULSE = np.arange(0, PULSE_WIDTH, 1/SAMPLING_FREQUENCY)

# target scenario parameters
DEFAULT_TARGET_RANGE = 5000  # 5 km
MAX_RANGE = 15000  # 15 km
MIN_RANGE = 100  # meters
DEFAULT_RCS = 10  # radar cross section (m²)
DEFAULT_VELOCITY = 100  # m/s

# simulation parameters
NUM_MONTE_CARLO_TRIALS = 1000
SNR_VALUES_DB = np.arange(-10, 20, 2)  # test range: -10 to 20 dB
TARGET_FALSE_ALARM_RATE = 1e-6

# clutter parameters
CLUTTER_TO_NOISE_RATIO_DB = 20  # strong ground clutter
CLUTTER_CORRELATION = 0.8  # 0=white noise, 1=fully correlated

# visualization parameters
FIGURE_SIZE = (12, 6)
DPI = 100
COLOR_SIGNAL = 'blue'
COLOR_NOISE = 'red'
COLOR_DETECTION = 'green'
COLOR_THRESHOLD = 'orange'

# helper functions
def range_to_time_delay(range_m):
    """convert target range to two-way time delay"""
    return (2 * range_m) / SPEED_OF_LIGHT

def time_delay_to_range(delay_s):
    """convert time delay to target range"""
    return (delay_s * SPEED_OF_LIGHT) / 2

def db_to_linear(db_value):
    """convert decibels to linear scale"""
    return 10 ** (db_value / 10)

def linear_to_db(linear_value):
    """convert linear to decibels"""
    return 10 * np.log10(linear_value)

def calculate_thermal_noise_power():
    """calculate receiver thermal noise power using N = k*T*B*F"""
    bandwidth = 1 / PULSE_WIDTH
    noise_figure_linear = db_to_linear(NOISE_FIGURE_DB)
    
    noise_power = (BOLTZMANN_CONSTANT * 
                   SYSTEM_TEMPERATURE * 
                   bandwidth * 
                   noise_figure_linear)
    
    return noise_power

def calculate_snr_from_range(target_range, target_rcs):
    """
    calculate SNR using radar equation
    SNR ∝ 1/R⁴ (inverse fourth power of range)
    """
    wavelength = SPEED_OF_LIGHT / CARRIER_FREQUENCY
    noise_power = calculate_thermal_noise_power()
    
    # radar equation (unity gain antenna)
    numerator = TRANSMIT_POWER * wavelength**2 * target_rcs
    denominator = (4 * np.pi)**3 * target_range**4 * noise_power
    
    snr_linear = numerator / denominator
    snr_db = linear_to_db(snr_linear)
    
    return snr_db

def print_config():
    """print radar configuration summary"""
    print("=" * 70)
    print("RADAR SYSTEM CONFIGURATION")
    print("=" * 70)
    print(f"\nTRANSMITTER:")
    print(f"  carrier frequency: {CARRIER_FREQUENCY/1e9:.1f} GHz")
    print(f"  pulse width: {PULSE_WIDTH*1e6:.1f} μs")
    print(f"  PRF: {PRF} Hz")
    print(f"  transmit power: {TRANSMIT_POWER/1e3:.1f} kW")
    
    print(f"\nRECEIVER:")
    print(f"  sampling frequency: {SAMPLING_FREQUENCY/1e9:.1f} GHz")
    print(f"  noise figure: {NOISE_FIGURE_DB} dB")
    print(f"  thermal noise power: {linear_to_db(calculate_thermal_noise_power()):.1f} dBW")
    
    print(f"\nSCENARIO:")
    print(f"  max range: {MAX_RANGE/1e3:.1f} km")
    print(f"  default target range: {DEFAULT_TARGET_RANGE/1e3:.1f} km")
    print(f"  default RCS: {DEFAULT_RCS} m²")
    
    wavelength = SPEED_OF_LIGHT / CARRIER_FREQUENCY
    range_resolution = SPEED_OF_LIGHT * PULSE_WIDTH / 2
    max_unambiguous_range = SPEED_OF_LIGHT / (2 * PRF)
    
    print(f"\nPERFORMANCE:")
    print(f"  wavelength: {wavelength*100:.2f} cm")
    print(f"  range resolution: {range_resolution:.1f} m")
    print(f"  max unambiguous range: {max_unambiguous_range/1e3:.1f} km")
    
    default_snr = calculate_snr_from_range(DEFAULT_TARGET_RANGE, DEFAULT_RCS)
    print(f"  SNR at default range: {default_snr:.1f} dB")
    
    print("=" * 70)

if __name__ == "__main__":
    print_config()