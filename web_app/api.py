import numpy as np
import pickle
import re
from collections import Counter
import email
from email.parser import Parser

# Parser
keywords = pickle.load(open('/Users/bellepeng/Desktop/Metis/Work/Projects/P3_Spam/web_app/train_set/keywords.pkl', 'rb'))

def cap_counts(a):
    caps=[1]
    caps_len=[1]
    for i in range(len(a)):
        caps.append(re.findall('([A-Z]+)', a[i]))
        if len(str(caps[i]))==2:
            caps_len.append(0)
        else:
            caps_len.append(len(str(caps[i]))-4)
    return np.mean(np.array(caps_len)[np.nonzero(caps_len)]), max(caps_len), sum(caps_len)

def get_processed_email(s):
    a = Counter(s.lower().split())
    words = s.split()

    oneEmail = [len(words)]

    for key in keywords:
        oneEmail.append(a[key]/oneEmail[0])
    oneEmail.extend(cap_counts(words))
    print(oneEmail)
    return np.array(oneEmail[1:]).reshape(1,-1)

UPLOAD_FOLDER = '/Users/bellepeng/Desktop/Metis/Work/Projects/P3_Spam/web_app/uploads'

def open_email(filename):
    with open(UPLOAD_FOLDER+'/'+filename, 'rb') as f:
        contents = f.read()
    test_email = Parser().parsestr(contents.decode('utf-8', errors='ignore'))
    return test_email.get_payload()

# Model
model_final = pickle.load(open('/Users/bellepeng/Desktop/Metis/Work/Projects/P3_Spam/web_app/train_set/model_final.pkl', 'rb'))

def make_hard_prediction(email):
    processed_email = get_processed_email(email)

    if model_final.predict(processed_email)==0:
        result="Ham!"
    else:
        result="Spam!"
    return result

def make_soft_prediction(email):
    processed_email = get_processed_email(email)
    return model_final.predict_proba(processed_email)[0,1]
