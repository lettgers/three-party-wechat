'''
@author: viewpoint
'''
import time,datetime
from time import sleep

twepoch = 1288834974657L
datacenter_id_bits = 5L
worker_id_bits = 5L
sequence_id_bits = 12L
max_datacenter_id = 1 << datacenter_id_bits
max_worker_id = 1 << worker_id_bits
max_sequence_id = 1 << sequence_id_bits
max_timestamp = 1 << (64L - datacenter_id_bits - worker_id_bits - sequence_id_bits)
sequence_id = 10

class Snowflake(object):

    def __init__(self):
        pass

    def make_snowflake(self, timestamp_ms, datacenter_id, worker_id, twepoch=twepoch):
        sid = ((int(timestamp_ms) - twepoch) % max_timestamp) << datacenter_id_bits << worker_id_bits << sequence_id_bits
        sid += (datacenter_id % max_datacenter_id) << worker_id_bits << sequence_id_bits
        sid += (worker_id % max_worker_id) << sequence_id_bits
        sid += sequence_id % max_sequence_id
        return sid

    def melt(snowflake_id, twepoch=twepoch):
        """inversely transform a snowflake id back to its parts."""
        sequence_id = snowflake_id & (max_sequence_id - 1)
        worker_id = (snowflake_id >> sequence_id_bits) & (max_worker_id - 1)
        datacenter_id = (snowflake_id >> sequence_id_bits >> worker_id_bits) & (max_datacenter_id - 1)
        timestamp_ms = snowflake_id >> sequence_id_bits >> worker_id_bits >> datacenter_id_bits
        timestamp_ms += twepoch

        return (timestamp_ms, int(datacenter_id), int(worker_id), int(sequence_id))

    def local_datetime(timestamp_ms):
        """convert millisecond timestamp to local datetime object."""
        return datetime.datetime.fromtimestamp(timestamp_ms / 1000.)

# if __name__ == "__main__":
#     print str(Snowflake().make_snowflake(time.time() * 1000, 1, 0))
