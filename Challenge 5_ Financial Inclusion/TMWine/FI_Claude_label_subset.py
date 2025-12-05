'''

for using Anthropic Claude to "hand label" a subset of the financial
inclusion keyword filtered subset; this was used to label about
4.4K rows of the FI keyword subset, which itself was about 237K rows

there are 7 categories total; see Claude prompt below for their
definitions, with examples

'''

import pandas as pd
import json
import random
from datetime import datetime

from dotenv import load_dotenv
import os
load_dotenv()
import glob

claude_prompt_preamble = '''This is a text classification task. You will receive a short, quoted sample text, often in the form of a question. The context is farming in east Africa. The text may have spelling and grammar peculiarities. Do your best to classify the text by choosing from the following coded category options: 
() pce--for pricing related questions
() mkt--regarding market availability, and buying and selling items
() sta--for farming business startup-related questions
() pft--for questions about future farming prospects and profits
() lon--for loan- and borrowing-specific questions
() mny--for more general questions related to obtaining money for farming
() msc--for any questions you can't categorize as above, or are unsure of

Some examples:

EXAMPLE 1 (two examples):
(i) what is the price of medium goat
(ii) How much does it cost to instal drip irrigation on a one point of land?
RESPONSE 1:
pce

EXAMPLE 2 (two examples):
(i) I have kienyeji eggs for sale. can i get buyers please
(ii) where is the market of goat's meat here in jinja
RESPONSE 2:
mkt

EXAMPLE 3:
how much capital do one need to start up pig farming as business
RESPONSE 3:
sta

EXAMPLE 4 (two examples):
(i) Which cash crop can i plant  at this season  make a good money
(ii) Whats more profitable between an acre of watermelon & cabbages?
RESPONSE 4:
pft

EXAMPLE 5:
I want to borrow me 500000 shillings to increase my business.
RESPONSE 5:
lon

EXAMPLE 6:
I need money from wefarm so as to improve productivity in my cows?
RESPONSE 6:
mny

EXAMPLE 7:
What herbicide should i buy
RESPONSE 7:
msc

~~~

TASK:
'''


my_api_key = os.getenv("ANTHROPIC_API_KEY")

from anthropic import Anthropic

claude_model = "claude-3-5-haiku-20241022"
max_claude_tokens = 300   # set this low enough to prevent wasting tokens

claude_on = True


pd.set_option('display.max_columns', None)   # to show full dataframe
# when printing--will display all columns
pd.set_option('display.max_colwidth', None)   # to display full column 
# content (for strings)


pathname = "DataKind_farmers/"
fi_filename = 'FI_filter_keywords.csv'
out_filename = 'FI_claude_cat.csv'


df_topics = pd.read_csv(pathname+fi_filename)

def show_samples(topic_label,num,df_in=df_topics):
    # shows sample row values according to topic label
    ser = df_in.loc[df_in['fi_topic']==topic_label,
                    'question_content'].sample(num)
    for ii,txt in enumerate(ser):
        print("%s: %s" % (ii,txt))

def general_samples(num,df_in=df_topics):
    ser = df_in['question_content'].sample(num)
    for ii,txt in enumerate(ser):
        print("%s: %s" % (ii,txt))

def make_tag_sample(topic_label,df_in=df_topics):
    # returns single sample of given topic, w/ original index
    row = df_in.loc[df_in['fi_topic']==topic_label].sample(1)
    return int(row['org_idx'].iloc[0]), row['question_content'].iloc[0]


# get Claude running:
if claude_on:
    client = Anthropic(api_key=my_api_key)
    
# load existing saved json org_idx labeling files--this was for
# doing the runs in chunks, of say 500 rows, to make sure Claude
# was doing OK:
file_prefix = 'fi_claude_cat.csv_'
file_pattern = os.path.join(pathname+'financial_inclusion_data/', f'{file_prefix}*.json')
json_files = glob.glob(file_pattern)

abd_oix = []   # what org_idx have been labeled already
uip = input("found %s json files of correct prefix; load? (y/n) " % 
      len(json_files))
if uip=='y':
    for file_path in json_files:
        with open(file_path, 'r') as fl:
            data = json.load(fl)
            if type(data) != dict:
                raise ValueError
            if set(data) != set(['parsed','unparsed']):
                raise ValueError
            sub_lst = [oix for oix,_ in data['parsed']]
            abd_oix += sub_lst
            sub_lst = [oix for oix,_ in data['unparsed']]
            abd_oix += sub_lst
            

token_count = 0


# control mixing--this is a crude way for random sampling to keep
# the labeled classes balanced in frequency; there are a lot more
# 'price' and 'market' type questions in the FI filtere dataset
# than other types:
'''
# original mixture
sel_lst = (['mkt','pce'] + 3*['sta','pft','lon','ufi_spl'] + 
           3*['dmg'] + ['ufi_mkp'])
'''
sel_lst = ['pce'] + 2*['lon','ufi_spl']   # narrow to this, to help
# with class balance
#           3*['dmg'] + ['ufi_mkp'])
resp_list = ['pce','mkt','sta','pft','lon','mny','msc']  # these
# are the expected categories from Claude

# for processing Claude responses
def proc_response(in_text):
    if in_text in resp_list:
        ret_type = 'ok'
        return (ret_type,in_text)
    elif in_text[:3] in resp_list:
        # note that Claude will sometimes try to be helpful, and
        # return category ~guess, along with explanation of
        # reasoning--so truncate
        ret_type = 'trunc'
        return (ret_type,in_text[:3])
    else:
        ret_type = 'err'
        return (ret_type,None)

cls_list = []   # for storing classification results; tuples,
# of type (org_idx,cat) where cat is the returned text category
# (when valid)
err_list = []   # for storing errors / unparseables returned from
# the API
exception_list = [18242281]  # for questions that caused Claude
# to break (eg about drugs)
max_claude_check = 500
for jj in range(max_claude_check):
    
    tag = random.sample(sel_lst,1)[0]
    oix, txt = make_tag_sample(tag)
    
    if oix in exception_list or oix in abd_oix:
        continue
    
    print("query sentence: %s" % txt)
    
    if claude_on:
        #usr_inp = input("ask Claude? (y/n) ")
        if True: #usr_inp == 'y':
            prompt_text = claude_prompt_preamble + "'"+txt+"'"
            #print(prompt_text)  # DEBUG
            #cnf_inp = input("confirm send to Claude? (y/n) ")
            if True: #cnf_inp=='y':
                response = client.messages.create(
                model=claude_model,
                max_tokens=max_claude_tokens,
                messages=[
                    {"role": "user", "content": prompt_text}
                    ]
                )
                print("reply:\n%s\n" % response.content[0].text)
                ret_type,ret_text = proc_response(
                    response.content[0].text)
                if ret_type=='ok' or ret_type=='trunc':
                    print("return parsed")
                    cls_list.append((oix,ret_text))
                else:
                    print("return unparseable")
                    err_list.append((oix,response.content[0].text))
                    
                token_count += (response.usage.input_tokens + 
                    response.usage.output_tokens)
    
print("total tokens used for claude: %s" % token_count)

if claude_on:
    us_cc = input("save labels list(s)? (y/n) ")
    if us_cc == 'y':
        out_dict = {'parsed':cls_list, 'unparsed':err_list}
        now = datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        out_file = pathname + out_filename + '_' + timestamp_str + '.json'
        with open(out_file, 'w') as json_file:
            json.dump(out_dict, json_file, indent=4) # indent for 
            # pretty-printing


'''
# to examine json files
file_prefix = 'fi_claude_cat.csv_'
file_pattern = os.path.join(pathname+'financial_inclusion_data/', f'{file_prefix}*.json')
json_files = glob.glob(file_pattern)
tot_dct = {}
keys = ['parsed','unparsed']
tot_dct = {key:[] for key in keys}
for file_path in json_files:
    with open(file_path, 'r') as fl:
        data = json.load(fl)
        for key in keys:    
            tot_dct[key] += data[key]
frq_dct = Counter([tag for _,tag in tot_dct['parsed']])
'''

