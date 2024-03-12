from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer

model_name = 'smilegate-ai/kor_unsmile'
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
pipe = TextClassificationPipeline(
    model = model,
    tokenizer = tokenizer,
    device = -1,   # cpu: -1, gpu: gpu number
    top_k = None,
    function_to_apply = 'sigmoid'
)

print('Start')
while True:
    s = input()
    result = pipe(s)[0]

    category = max(result, key=lambda x: x['score'])
    print(f'-> Category: {category["label"]} ( {category["score"] * 100:.2f}% )')