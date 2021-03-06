import argparse
import logging
from preferences_editor import PreferencesEditor
import sys

DEBUG = "debug"
DETECTION_RATE = "detectionrate" #ms
LASER_INTENSITY = "laserintensity"
MARKER_RADIUS = "markerradius"
IGNORE_LASER_COLOR = "ignorelasercolor"

class Configurator():
    def _check_rate(self, rate):
        value = int(rate)
        if value < 1:
            raise argparse.ArgumentTypeError("DETECTION_RATE must be a number " +
                "greater than 0")
        return value  

    def _check_intensity(self, intensity):
        value = int(intensity)
        if value < 0 or value > 255:
            raise argparse.ArgumentTypeError("LASER_INTENSITY must be a number " +
                "between 0 and 255")
        return value   

    def _check_radius(self, radius):
        value = int(radius)
        if value < 1 or value > 20:
            raise argparse.ArgumentTypeError("MARKER_RADIUS must be a number " +
                "between 1 and 20")
        return value  

    def _check_ignore_laser_color(self, ignore_laser_color):
        ignore_laser_color = ignore_laser_color.lower()
        if ignore_laser_color != "red" and ignore_laser_color != "green":
            raise argparse.ArgumentTypeError("IGNORE_LASER_COLOR must be a string " +
                "equal to either \"green\" or \"red\" without quotes")
        return ignore_laser_color  

    def __init__(self):
        
        config, preferences = PreferencesEditor.map_configuration()

        # Parse command line arguments
        parser = argparse.ArgumentParser(prog="EDFTS.py")
        parser.add_argument("-d", "--debug", action="store_true", 
            help="turn on debug log messages")
        parser.add_argument("-r", "--detection-rate", type=self._check_rate,
            help="sets the rate at which shots are detected in milliseconds. " +
                "this should be set to about the length of time your laser trainer " +
                "stays on for each shot, typically about 100 ms")
        parser.add_argument("-i", "--laser-intensity", type=self._check_intensity, 
            help="sets the intensity threshold for detecting the laser [0,255]. " +
                "this should be as high as you can set it while still detecting " +
                "shots")
        parser.add_argument("-m", "--marker-radius", type=self._check_radius,
            help="sets the radius of shot markers in pixels [1,20]")
        parser.add_argument("-c", "--ignore-laser-color",
            type=self._check_ignore_laser_color,
            help="sets the color of laser that should be ignored by EDFTS (green " +
                "or red). No color is ignored by default")
        args = parser.parse_args()

        preferences[DEBUG] = args.debug

        if args.detection_rate:
            preferences[DETECTION_RATE] = args.detection_rate

        if args.laser_intensity:
            preferences[LASER_INTENSITY] = args.laser_intensity

        if args.marker_radius:
            preferences[MARKER_RADIUS] = args.marker_radius

        if args.ignore_laser_color:
            preferences[IGNORE_LASER_COLOR] = args.ignore_laser_color

        self._preferences = preferences
        self._config_parser = config

    def get_preferences(self):
        return self._preferences

    def get_config_parser(self):
        return self._config_parser

    def get_logger(self):
        logger = logging.getLogger('EDFTS')
        stdhandler = logging.StreamHandler(sys.stdout)

        if self._preferences[DEBUG]:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stdhandler.setFormatter(formatter)
        logger.addHandler(stdhandler)

        return logger
