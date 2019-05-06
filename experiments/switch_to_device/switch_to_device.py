# SkyNEt imports
from SkyNEt.instruments import InstrumentImporter
import config_switch_to_device as config

# Initialize config object
cf = config.experiment_config()
# Initialize serial object
ser = InstrumentImporter.switch_utils.init_serial(cf.comport)
# Switch to device
InstrumentImporter.switch_utils.connect_single_device(ser, cf.device)

# Status print
print(f'Connected device {cf.device}')