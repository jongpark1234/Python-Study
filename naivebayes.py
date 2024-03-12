from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# 데이터셋
sentences = list(map(lambda x: x.split('|'), open('dataset.txt', 'r', encoding='utf-8').read().split('\n')))

# 문자열 분리 및 데이터 라벨링
X = [sentence[0].strip() for sentence in sentences]
y = [sentence[1] for sentence in sentences]

# 텍스트 데이터 -> 벡터 변환
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)

# 전체 데이터 중 일부를 학습 데이터로, 일부를 테스트 데이터로 분류
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Naive-Bayes 방식으로 학습시키기
# Multinomial 이외에도 Gaussian (연속형 변수) 및 Categorial (범주형 변수) 특성을 가진 나이브 베이즈 분류 방식이 존재하나
# Multinomial (빈도수) 방식이 텍스트 데이터에 적합하므로 MultinomailNB를 채용.
naive_bayes = MultinomialNB().fit(X_train, y_train)

# 테스트셋에 대한 예측값
y_pred = naive_bayes.predict(X_test)

# 모델 평가
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# 평가 보고
print(classification_report(y_test, y_pred))


# 테스트용 문자열에 대한 실제 사용
while True:
    string = input()
    new_sentences_vertorized = vectorizer.transform([string])
    predictions = naive_bayes.predict(new_sentences_vertorized)

    for prediction in predictions:
        print(f"-> Prediction: {'비속어' if prediction == '1' else '일반'}")
