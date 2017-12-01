import pandas as pd
import io
import pickle

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

f_train = open("training_data.csv", "w")
training_data.to_csv("training_data.csv")
f_train.close()

f_test = open("testing_data.csv", "w")
test_data.to_csv("testing_data.csv")
f_test.close()

f_test = open("predict_data.csv", "w")
predict_data.to_csv("predict_data.csv")
f_test.close()