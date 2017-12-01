
from __future__ import print_function
import tensorflow as tf
import numpy as np
import pandas as pd
import io
import pickle

def get_batch(batch_size, dataset):
    """takes random rows of dataset and use for training/testing"""
    pass

# import data
pd.set_option('max_colwidth',400)
COLUMNS = ["servo_angles", "position","rotation"]

dataset = pd.read_csv("LUT.txt", names=COLUMNS)#this will need parsing

pos_text = dataset.get("position").to_string()
pos_text = pos_text.replace('{','')
pos_text = pos_text.replace('}','')
pos_text = pos_text.replace('.', '0')
pos_text = pos_text.split('\n')
temp_pos = ""
for line in pos_text:
    temp_pos += line[5:].strip() + '\n'
pos_text = temp_pos
pos_dataset = pd.read_csv(io.StringIO(pos_text), \
                          names = ["x","y","z"])


servo_text = dataset.get("servo_angles").to_string()
servo_text = servo_text.replace('{','')
servo_text = servo_text.replace('}','')

servo_dataset = pd.read_csv(io.StringIO(servo_text), \
                          names = ["prec","s1","s2","s3","s4","s5", "s6"])
servo_dataset = servo_dataset.drop(["prec"], axis=1)

# print(servo_dataset)
# print(pos_dataset)

rot_text = dataset.get("rotation").to_string()
rot_text = rot_text.split('\n')
temp_rot = ""
for line in rot_text:
    temp_rot += "0.0,0.0,0.0" + '\n'
rot_text = temp_rot

rot_dataset = pd.read_csv(io.StringIO(rot_text), \
                          names = ["pitch", "yaw", "roll"])

parsed_dataset = pd.concat([servo_dataset, pos_dataset.get("z")], axis = 1)
f = open("dataset.txt", "wb")
pickle.dump(parsed_dataset, f)
f.close()

f = open("dataset.txt", "rb")
data = pickle.load(f)
f.close()
h = data.shape[0]
train_size = int(h * .8)
predict_size = int(h * .99)
training_data = data.iloc[:train_size, :]
test_data = data.iloc[train_size:predict_size, :]
predict_data = data.iloc[predict_size:, :]

# f_train = open("training_data.csv", "w")
# training_data.to_csv("training_data.csv")
# f_train.close()
# 
# f_test = open("testing_data.csv", "w")
# test_data.to_csv("testing_data.csv")
# f_test.close()
# 
# f_test = open("predict_data.csv", "w")
# predict_data.to_csv("predict_data.csv")
# f_test.close()

  # Load datasets
data_train, data_test, data_predict = "./training_data_x.csv","./testing_data_x.csv", "./predict_data_x.csv"


  # Training examples
training_set = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename=data_train, target_dtype=np.int, features_dtype=np.float64)

  # Test examples
test_set = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename=data_test, target_dtype=np.int, features_dtype=np.float64)

  # Set of examples for which to predict
prediction_set = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename=data_predict, target_dtype=np.int, features_dtype=np.float64)


sess = tf.Session()

def model_fn(features, labels, mode, params):
    """Model function for Estimator."""
    # Connect the first hidden layer to input layer
    # (features["x"]) with relu activation
    first_hidden_layer = tf.layers.dense(features["servo_angles"], 15, activation=tf.nn.elu)

    # Connect the second hidden layer to first hidden layer with relu
    second_hidden_layer = tf.layers.dense(
        first_hidden_layer, 15, activation=tf.nn.relu)

    third_hidden_layer = tf.layers.dense(
        second_hidden_layer, 10, activation=tf.nn.selu)

    # Connect the output layer to second hidden layer (no activation fn)
    output_layer = tf.layers.dense(third_hidden_layer, 1)

    # Reshape output layer to 1-dim Tensor to return predictions
    predictions = tf.reshape(output_layer, [-1])

    # Provide an estimator spec for `ModeKeys.PREDICT`.
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions={"x_pos": predictions})

    # Calculate loss using mean squared error
    loss = tf.losses.mean_squared_error(labels, predictions)

    # Calculate root mean squared error as additional eval metric
    eval_metric_ops = {
        "rmse": tf.metrics.root_mean_squared_error(
            tf.cast(labels, tf.float64), predictions)
    }

    optimizer = tf.train.AdamOptimizer(
        learning_rate=params["learning_rate"])
    train_op = optimizer.minimize(
        loss=loss, global_step=tf.train.get_global_step())

    # Provide an estimator spec for `ModeKeys.EVAL` and `ModeKeys.TRAIN` modes.
    return tf.estimator.EstimatorSpec(
        mode=mode,
        loss=loss,
        train_op=train_op,
        eval_metric_ops=eval_metric_ops)


def get_input_fn(data_set, num_epochs=None, shuffle=True):
    return tf.estimator.inputs.pandas_input_fn(
        x=pd.DataFrame({k: data_set[k].values for k in FEATURES}),
        y = pd.Series(data_set[LABEL].values),
        num_epochs=num_epochs,
        shuffle=shuffle)

m = 10

FEATURES = ["s1","s2","s3","s4","s5", "s6"]
LABEL = "x" # ["x", "y", "z","pitch", "yaw", "roll"]

feature_cols = [tf.feature_column.numeric_column(k) for k in FEATURES]


LEARNING_RATE = .005
model_params = {"learning_rate": LEARNING_RATE}

nn = tf.estimator.Estimator(model_fn=model_fn, params=model_params)

train_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"servo_angles": np.array(training_set.data)},
    y=np.array(training_set.target),
    num_epochs=None,
    shuffle=False)


# Train
nn.train(input_fn=train_input_fn, steps=20000)

# Score accuracy
test_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"servo_angles": np.array(test_set.data)},
    y=np.array(test_set.target),
    num_epochs=1,
    shuffle=False)


ev = nn.evaluate(input_fn=test_input_fn)
print("Loss: %s" % ev["loss"])
print("Root Mean Squared Error: %s" % ev["rmse"])

predict_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"servo_angles": np.array(prediction_set.data)},
    num_epochs=1,
    shuffle=False)

predictions = nn.predict(input_fn=predict_input_fn)
for i, p in enumerate(predictions):
    print("Prediction %s: %s" % (i + 1, p["x_pos"]))