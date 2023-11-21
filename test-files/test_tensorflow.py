import requests
import tensorflow as tf
import tensorflow_text as tf_text

url = "https://github.com/tensorflow/text/blob/master/tensorflow_text/python/ops/test_data/test_oss_model.model?raw=true"
sp_model = requests.get(url).content

tokenizer = tf_text.SentencepieceTokenizer(sp_model, out_type=tf.string)
tokens = tokenizer.tokenize(["What you #$&$*%know you can't explain, but you feel it."])
print(tokens.to_list())
