import keras
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.datasets import imdb

# 샘플 데이터 - 비속어 포함된 문장들
texts, labels = [], []
dataset = open('dataset.txt', 'r', encoding='utf-8').read().split('\n')
for text, label in map(lambda x: x.split('|'), dataset):
    texts.append(text)
    labels.append(int(label))


# 토크나이저 준비
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)

vocab_size = len(tokenizer.word_index) + 1

# 학습 / 검증용으로 구분
text_train, text_test, label_train, label_test = train_test_split(texts, labels, test_size=0.25, random_state=137)

# 텍스트 시퀀스를 숫자 시퀀스로 변환
sequences = tokenizer.texts_to_sequences(texts)

# 패딩을 추가하여 시퀀스 길이 통일
max_length = max([len(seq) for seq in sequences])


padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post').tolist()

# 모델 구축
model = keras.Sequential([
    keras.layers.Embedding(vocab_size, 16, input_length=max_length),
    keras.layers.GlobalAveragePooling1D(),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# 손실 함수 및 옵티마이저 설정
model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

# 모델 훈련
model.fit(padded_sequences, labels, epochs=50, verbose=1)


# 새로운 문장을 예측하기 위해 전처리
def preprocess_text(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_length, padding='post')
    return padded_sequence

# 비속어 감지 함수
def detect_profanity(text):
    preprocessed_text = preprocess_text(text)
    prediction = model.predict(preprocessed_text)[0][0]
    if prediction < 0.75:
        return f"정상 문장입니다. ( {prediction * 100}% )"
    else:
        return f"비속어가 포함된 문장입니다. ( {prediction * 100}% )"

print('Start')

while True:
    test_sentence = input()
    print(detect_profanity(test_sentence))
