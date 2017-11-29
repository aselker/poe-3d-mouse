import pandas as pd
import io
import pickle

def import_data(input_name = "../solnTable.csv"):
    pd.set_option('max_colwidth',400)
    COLUMNS = ["servo_angles", "position","rotation"]

    dataset = pd.read_csv(input_name, names=COLUMNS)#this will need parsing

    pos_text = dataset.get("position").to_string()
    pos_text = pos_text.replace('{','')
    pos_text = pos_text.replace('}','')
    pos_text = pos_text.split('\n')
    temp_pos = ""
    for line in pos_text:
        temp_pos += line[5:] + '\n'
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

    rot_dataset = pd.read_csv(io.StringIO(rot_text), \
                          names = ["pitch", "yaw", "roll"])

    f = open("dataset.txt", "wb")
    pickle.dump([pos_dataset, rot_dataset, servo_dataset], f)
    f.close()

    print("Data parsed")