import pandas as pd
import sys
from pprint import pprint
import json
import openpyxl
import re
import csv
 #スレッドをたどる
def get_text(now_id):
    return no_retweets[no_retweets['Column1.tweet.id'] == now_id]['Column1.tweet.full_text'].values[0]

def thread(now_id):
    # 元のidのtextを積む
    text_data = get_text(now_id)
    # 元のidをin_reply_to_status_idに含むものを探す
    has_in_reply_to_status_id = no_retweets[no_retweets['Column1.tweet.in_reply_to_status_id_str'] == now_id]
    #見つかるうちは、元のidをin_reply_to_status_idに含むものを探す
    while len(has_in_reply_to_status_id)>0:
        now_id = has_in_reply_to_status_id['Column1.tweet.id'].values[0]
        text_data += '\n' + get_text(now_id)
        #print (now_id, text_data)
        has_in_reply_to_status_id = no_retweets[no_retweets['Column1.tweet.in_reply_to_status_id_str'] == now_id]
    return text_data

#全ツイートcvsファイル読み込み
#excelでjs->json->csv
tweets_df = pd.read_csv('minithink.csv')

#リツイートは省く
no_retweets = tweets_df[~tweets_df['Column1.tweet.full_text'].str.contains('RT')]

# expanded_urlsを持つものだけを抽出
no_retweets_with_expanded_urls = no_retweets[no_retweets['Column1.tweet.entities.urls.expanded_url'].notnull()]
# expanded_urlsにhttps://marshmallow-qa.comを含むもの＝マショマロの解答のトップ　を抽出
marshmallow_tops = no_retweets_with_expanded_urls[no_retweets_with_expanded_urls['Column1.tweet.source'].str.contains("https://marshmallow-qa.com")]
#答えを収集しリストに格納
# print(marshmallow_tops['Column1.tweet.id'])
answers = [[now_tweet_id, thread(now_tweet_id)] for now_tweet_id in marshmallow_tops['Column1.tweet.id']]

for i in answers:
    i[1]=i[1].replace("\n","")
    i[1]=re.sub(r'#マシュマロを投げ合おう',"",i[1])
    i[1]=re.sub(r"https://t\.co/.*[亜-熙ぁ-んァ-ヶ]??","",i[1])

with open("answerslist.csv", "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(answers)