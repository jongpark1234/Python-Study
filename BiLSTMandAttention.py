import keras
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

#### 뭔가 안됨 ====================================================================================================================

class BahdanauAttention(tf.keras.Model):
  def __init__(self, units):
    super(BahdanauAttention, self).__init__()
    self.W1 = keras.layers.Dense(units)
    self.W2 = keras.layers.Dense(units)
    self.V = keras.layers.Dense(1)

  def call(self, values, query): # 단, key와 value는 같음
    # query shape == (batch_size, hidden size)
    # hidden_with_time_axis shape == (batch_size, 1, hidden size)
    # score 계산을 위해 뒤에서 할 덧셈을 위해서 차원을 변경해줍니다.
    hidden_with_time_axis = tf.expand_dims(query, 1)

    # score shape == (batch_size, max_length, 1)
    # we get 1 at the last axis because we are applying score to self.V
    # the shape of the tensor before applying self.V is (batch_size, max_length, units)
    score = self.V(tf.nn.tanh(
        self.W1(values) + self.W2(hidden_with_time_axis)))

    # attention_weights shape == (batch_size, max_length, 1)
    attention_weights = tf.nn.softmax(score, axis=1)

    # context_vector shape after sum == (batch_size, hidden_size)
    context_vector = attention_weights * values
    context_vector = tf.reduce_sum(context_vector, axis=1)

    return context_vector, attention_weights


# 샘플 데이터 - 비속어 포함된 문장들
texts, labels = [], []
dataset = open('dataset.txt', 'r', encoding='utf-8').read().split('\n')
for text, label in map(lambda x: x.split('|'), dataset):
    texts.append(text)
    labels.append(int(label))

# 학습 / 검증용으로 구분
text_train, text_test, label_train, label_test = train_test_split(texts, labels, test_size=0.25, random_state=137)

# 토크나이저 준비
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)

vocab_size = len(tokenizer.word_index) + 1
print(vocab_size)

# 텍스트 시퀀스를 숫자 시퀀스로 변환
texts = tokenizer.texts_to_sequences(texts)
text_train = tokenizer.texts_to_sequences(text_train)
text_test = tokenizer.texts_to_sequences(text_test)

# 패딩을 추가하여 시퀀스 길이 통일
max_len = max([len(text) for text in texts])
text_train = pad_sequences(text_train, maxlen=max_len).tolist()
text_test = pad_sequences(text_test, maxlen=max_len).tolist()

# 모델 구축
sequence_input = keras.Input(shape=(max_len,), dtype='int32')
embedded_sequences = keras.layers.Embedding(vocab_size, 128, input_length=max_len, mask_zero = True)(sequence_input)

lstm = keras.layers.Bidirectional(
   keras.layers.LSTM(64, dropout=0.5, return_sequences=True)
)(embedded_sequences)

lstm, forward_h, forward_c, backward_h, backward_c = keras.layers.Bidirectional(
   keras.layers.LSTM(64, dropout=0.5, return_sequences=True, return_state=True)
)(lstm)

state_h = keras.layers.Concatenate()([forward_h, backward_h]) # 은닉 상태
state_c = keras.layers.Concatenate()([forward_c, backward_c]) # 셀 상태

Attention = BahdanauAttention(16) # 가중치 크기 정의
context_vector, attention_weights = Attention(lstm, state_h)

dense1 = keras.layers.Dense(20, activation="relu")(context_vector)
dropout = keras.layers.Dropout(0.5)(dense1)
output = keras.layers.Dense(1, activation="sigmoid")(dropout)
model = keras.Model(inputs=sequence_input, outputs=output)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(
   text_train,
   label_train,
   epochs=16,
   validation_data=(text_test, label_test),
   verbose=1
)

print(f'\n테스트 정확도: {model.evaluate(text_test, label_test)[1]:.4f}')

# 새로운 문장을 예측하기 위해 전처리
def preprocess_text(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
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
