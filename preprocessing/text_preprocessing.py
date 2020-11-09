

import re
from tqdm import tqdm
import pandas as pd


def hangul_preprocessing(doctor_opinions, remove_stopwords=False, stopwords=None):
	'''
	process hangul to list of words
	:param doctor_opinions: documents to analysis
	:param remove_stopwords: whether remove the stopwords or not
	:param stopwords: list of stopwords to remove
	:return: list of words in document
	'''
	doctor_opinions_cleaned=None
	try:
		if str(doctor_opinions)!='nan':
			stop_words = {'은', '는', '이', '가', '하', '아', '것', '들', '의', '있', '되', '수', '보', '주', '등', '한'}
			from konlpy.tag import Okt

			## remove all non-hangul and space chars
			doctor_opinions_cleaned = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", doctor_opinions)
			open_korean_text = Okt()
			## extract words
			doctor_opinions_cleaned = open_korean_text.morphs(doctor_opinions_cleaned, stem=True)
			### remove stopwords in words list
			if remove_stopwords:
				assert stopwords is not None, 'when remove_stopwords is True, require stopwords list'
				doctor_opinions_cleaned = [token for token in doctor_opinions_cleaned if not token in stop_words]
	except:
		print(doctor_opinions)
	return doctor_opinions_cleaned


def words_transform(wordslist):
	'''
	transform words in  to sequences
	:param wordslist: list of all processed opinions
	:return: sequences lists of each opinions
	'''
	from tensorflow.python.keras.preprocessing.text import Tokenizer
	tokenizer = Tokenizer()
	### train tokenizer
	tokenizer.fit_on_texts(wordslist)
	train_sequences = tokenizer.texts_to_sequences(wordslist)
	return train_sequences


if __name__=='__main__':
	opinions = pd.read_excel(f'dataset/종합검진소견.xlsx')
	opinions = list(opinions['종합검진소견'])

	cleaned_opinions = []
	for opinion in tqdm(opinions):
		cleaned = hangul_preprocessing(doctor_opinions=opinion)
		cleaned_opinions.append(cleaned)
