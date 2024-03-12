import keras
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split

tokenizer = BertTokenizer.from_pretrained('beomi/kcbert-base')
model = TFBertForSequenceClassification.from_pretrained('beomi/kcbert-base')

# 샘플 데이터 - 비속어 포함된 문장들
texts, labels = [], []
dataset = open('dataset.txt', 'r', encoding='utf-8').read().split('\n')
for text, label in map(lambda x: x.split('|'), dataset):
    texts.append(text)
    labels.append(int(label))

# 학습 / 검증용으로 구분
text_train, text_test, label_train, label_test = train_test_split(texts, labels, test_size=0.2, random_state=137)
# 토큰화 및 인코딩
train_encodings = tokenizer(text_train, padding=True, truncation=True)
test_encodings = tokenizer(text_test, padding=True, truncation=True)

# 데이터셋 생성
train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_encodings),
    label_train
))
val_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_encodings),
    label_test
))

model.compile(optimizer=keras.optimizers.Adam(learning_rate=3e-5), loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

# 모델 학습 ( fine-tuning )
model.fit(train_dataset.shuffle(100).batch(16), epochs=2, steps_per_epoch=115, validation_data=val_dataset.batch(16))

# 문장 예측 함수
def predict_sentence(sentence):
    # 토큰화 및 패딩
    inputs = tokenizer(sentence, padding=True, truncation=True, return_tensors="tf")
    # 예측
    outputs = model(inputs)
    # 예측 결과 반환
    return tf.nn.softmax(outputs.logits, axis=1).numpy()[0]


# 문장 예측
while True:
    print(f'{predict_sentence(input())[1]:.2f}%')

    