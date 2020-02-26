import pandas as pd
import json
import re 


#１つの問答をjson用のdictに変換する補助関数
def qa2dict(now_qa):
    
    now_question = now_qa[0]
    now_answer   = now_qa[1]
    
    #『』で囲まれたものを書物として抽出して、タグ化する
    book_list = re.findall('『[^』]+』' , now_answer)
    book_list = ['[' + book + ']' for book in book_list]
    print(now_answer)
    print(now_question)
    now_question_list = now_question.split('\n')
    now_answer_list   = now_answer.split('\n')
    
    qa_dict ={}
    qa_dict['title'] = now_question_list[0][:30] #質問の１行目をタイトルに
    qa_dict['lines'] = ['','[**** 質問]'] + now_question_list
    qa_dict['lines'] += ['','[**** 解答]'] + now_answer_list
    if book_list:
        qa_dict['lines'] += ['','[**** 文献]'] + book_list
    return qa_dict

#マシュマロの全問答を集めたエクセルファイルを読み込み
mash_df = pd.read_excel('answer_question.xlsx')
#リストに変換
mash_list = mash_df.values.tolist() #[[質問, 解答],[質問, 解答],…]

#問答を１つずつjson用のdictに変換し、格納
dict_list = []
for mash_qa in mash_list:
    dict_list.append(qa2dict(mash_qa))

#出力用のjsonのdictをつくる
pages_dict = dict(pages=dict_list)
#jsonファイルを書き出し
f2 = open('mash.json', 'w',encoding="utf-8")
json.dump(pages_dict, f2, ensure_ascii=False, indent=4, sort_keys=False)