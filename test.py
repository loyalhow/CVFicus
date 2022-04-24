from tensorflow.python.client import device_lib
import tensorflow as tf
# gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
# for gpu in gpus:
#     tf.config.experimental.set_memory_growth(gpu, True)
print(device_lib.list_local_devices())
print(tf.__version__)
print(tf.test.is_gpu_available())