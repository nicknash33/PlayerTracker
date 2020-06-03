import tensorflow as tf
from os import listdir
from os.path import isfile, join
from object_detection.utils import dataset_util
import json

flags = tf.app.flags
flafs.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

with open(frame, 'rb') as image:
    f = image.read()
    b = bytearray(f)


def load_into_model(data):
    height = 450
    width = 800
    filename = data['file_name']
    encoded_image_data = data['encoded_image']
    image_format = b'jpeg'

    xmins = [data['xmins'] / width]
    xmaxs = [data['xmaxs'] / width]
    ymins = [data['ymins'] / height]
    ymaxs = [data['ymaxs'] / height]
    classes_text = [data['classes_text']]
    classes = [data['class_id']]

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def get_dims(data):
    xmin = data['loc']['x']
    xmax = xmin + data[loc]['w']
    ymin = data['loc']['y']
    ymax = ymin + data['loc']['h']

    return xmin, xmax, ymin, ymax


def get_class(data):
    return data['type']


def extract_organize_data(data, id):
    frame_data = []
    for box in data:
        extracted_data = None
        (xmin, xmax, ymin, ymax) = get_dims(data[box])
        class_name = get_class(data[box])
        if class_name == 'player':
            class_id = 1
        elif class_name == 'goalie':
            class_id = 2
        elif class_name == 'ref':
            class_id = 3
        else:
            print('Got invalid class name. Defaulting to player')
            class_id = 1

        extracted_data = dict(
            classes_id=class_id,
            classes_text=class_name,
            xmaxs=xmax,
            xmins=xmin,
            ymins=ymin,
            ymaxs=ymax
        )

def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output)
    path = '/Users/nick/PycharmProjects/PlayerTracker/venv/NeuralNetwork/training_data/image_data'
    all_frame_data = [f for f in listdir(path) if isfile(join(path, f))]

    for frame_data in all_frame_data:
        extracted_data = {}
        frame_id = frame_data[:-5]
        image_filename = str(frame_id + '.jpg')
        with open('frame_data') as file:
            data = json.load(file)
            file.close()


