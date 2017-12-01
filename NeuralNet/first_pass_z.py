from __future__ import print_function
import tensorflow as tf
import numpy as np
import pandas as pd
import io
import pickle

data_train, data_test, data_predict = "./training_data_z.csv","./testing_data_z.csv", "./predict_data_z.csv"


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
    first_hidden_layer = tf.layers.dense(features["servo_angles"], 15, activation=tf.nn.relu)

    # Connect the second hidden layer to first hidden layer with relu
    second_hidden_layer = tf.layers.dense(
        first_hidden_layer, 15, activation=tf.nn.tanh)

    third_hidden_layer = tf.layers.dense(
        second_hidden_layer, 10, activation=tf.nn.relu)

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


LEARNING_RATE = .001
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