'''

for keyword filtering of English rows of full raw WeFarm dataset

this expects a file of row indices from the original dataframe
corresponding to unique English language questions--"unique" is
taken to be unique text from any given user--duplicate text 
strings are allowed if coming from different users

this also optionally uses a spell correction dictionary, which
can have corrections for misspellings or common SMS abbreviations;
the included dictionary, corr_al_dcts..., is OK, but not perfect

'''


import pandas as pd
import re
import json


pd.set_option('display.max_columns', None)   # to show full dataframe
# when printing--will display all columns

pathname = "DataKind_farmers/"
raw_filename = 'raw_dataset_producers_direct_copy.csv'
corr_dict_file = "corr_al_dcts_20251114_110823.json"
word_list_path = 'programming_resources/' # eg Br-En conversion
# for converting from British english;
# from "https://raw.githubusercontent.com/hyperreality/American-British-English-Translator/master/data/british_spellings.json"
# (MIT license):
word_list_file = 'british_spellings.json'


spell_correct = True  # for including spell-correct dictionary, eg
# SMS abbreviations, etc
rgx = False   # for including regex searches--with the per-word parsing of 
# this method, this is probably not necessary (though could run in parallel
# over whole un-parsed rows)

# for leading q/Q's:
pat_1 = "^[Qq][^a-zA-Z]+"
pat_2 = "^(qn|Qn|qN|QN)[^A-Za-z]*"
pat_3 = r"^[Qq](?![uU])"
tot_pat = "|".join([pat_1,pat_2,pat_3])   # order matters--re.sub will go 
# from left to right

word_split = re.compile(r'\b(?!\d+\b)\w+\b')  # avoids pure digit "words"

# define keywords that may involve financial inclusion / non-farm
# topics:
t1 = ['fund','funds','funding','funded','lend','lends','lending','credit',
	'debt','loan','loans','grant','grants','financing','subsidy','subsidies',
	'assistance','oneacre','borrow','borrowing']
t2 = ['finance','financial','microfinance','microfinancing','microfinancial']
t3 = ['bank','banks','banking','cooperative','nbfi', 'mfi', 'vsla']
t4 = ['debit','savings','account',
	'withdrawal','withdrawals','deposit','deposits','depositing',
	'transaction','transactions']
t5 = ['payment','paying','expense','expenses','bills']
t6 = ['wages','income']
t7 = ['insurance']
t8 = ['investment','investments','business','businesses',
      'agribusiness','agribusinesses','capital']
t10 = ['profit','profits','profitable']
t11 = ['money']
t12 = ['accounting','accountant']
t_market = ['market','markets','mkt','mkts','mrkt','mrkts']
t_price = ['price','pricing','prices','cost','wholesale','farmgate','farm gate']
t_digital_market = ['sell','selling','sale','seller','buy','buying','buyer']  # these usually
# may have to do with digital marketplace (eg selling a crop)

query_words_plain = (t1+t2+t3+t4+t5+t6+t7+t8+t10+t11+t12+t_market+
                    t_price+t_digital_market)

query_words_regex = []
query_words_regcm = [re.compile(rg) for rg in query_words_regex]

currency_abbr = ['tzs','ugx','ushs','ugshs','kes','ksh','kshs','shs']

corr_dict = {}
if spell_correct:
    with open(pathname+corr_dict_file, 'r') as file:
        cor_aln_dct = json.load(file)
    corr_dict = cor_aln_dct['corr_dict']
    
    # British-American spellings; normalized to American
    with open(word_list_path+word_list_file, 'r') as file:
        br_en_dict = json.load(file)
    br_en_dict = {key.lower():value.lower() for key, value in br_en_dict.items()}
    corr_dict.update(br_en_dict)
    
def clean_text_1(in_str):
    out_str = remove_qs_etc(in_str)
    out_str = num_pun_sep(out_str)
    #out_str = abbrs(out_str)
    return out_str.lower()

def remove_qs_etc(in_string):
    in_string.strip()   # extra leading/trailing spaces
    out_string = re.sub(tot_pat,'',in_string)
    return out_string

# separate numbers from letters, and follow punctuation by a space
def num_pun_sep(in_string):
    # thanks to Google GPT--
    # Add space when a digit is followed by a letter
    out_string = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', in_string)
    # Add space when a letter is followed by a digit
    out_string = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', out_string)
    # add space when punctuation is followed by a letter
    out_string = re.sub(r'([,.])([a-zA-Z])',r'\1 \2',out_string)
    # add space when ? is followed by letter or number
    out_string = re.sub(r'(\?)([a-zA-Z0-9])',r'\1 \2',out_string)
    # add spaces around parentheses
    out_string = re.sub(r'(\()',' ( ',out_string)
    out_string = re.sub(r'(\))',' ) ',out_string)
    out_string = re.sub("\s\s+", " ", out_string)  # extra "inner" spaces
    return out_string

def proc_data(df_sub, spell_corr = True):
    
    col_to_parse = 'question_content'

    # this will be a Pandas series, with cleaned lower-cased text in each entry
    tmp_ser = df_sub[col_to_parse].apply(clean_text_1)

    # list of sublists, one sublist (of cleaned lc'd) words per row
    rows_list = [word_split.findall(text) for text in tmp_ser]

    # do spelling corrections (if wanted)
    if spell_corr:
        # since spelling correct can produce multi-word results, unpack as
        # list (w/ .split() for any corrections), then flatten:
        tmp_lst = [[[wrd] if wrd not in corr_dict else corr_dict[wrd].split()
                     for wrd in row] for row in rows_list]
        rows_list = [[wrd for lst in row for wrd in lst] for row in tmp_lst]
        
    # translate currency abbreviations
    rows_list = [[wrd if wrd not in currency_abbr else 'shillings' for wrd in row]
                for row in rows_list]
        
    # for more efficient dataframe storage, join (by space) words in sublists:
    rows_cleaned = [' '.join(row) for row in rows_list]
    df_sub['clean_text'] = rows_cleaned

    # options:
    # () frequency count (eg per row / ie per sublist in rows_list)
    # () coincident words list (ie per row, all matching words are pulled)

    # for basic frequency count (per-row)
    # handles regular Python string search and regex separately
    num_wds_lst_p = [sum([1 if wrd in query_words_plain else 0 
                        for wrd in row]) for row in rows_list]
    num_wds_lst_r = []
    if rgx:
        num_wds_lst_r = [sum([1 if rg.search(' '.join(row)) is not None else 0 
                          for rg in query_words_regcm]) 
                     for row in rows_list]
        tot_row_frq = [sum(el) for el in zip(num_wds_lst_p,num_wds_lst_r)]
    else:
        tot_row_frq = num_wds_lst_p
        
    # post-process frequency counts, eg flag rows (indices) with > 0 counts
    row_ixs_bln = [True if val > 0 else False for val in tot_row_frq]
    df_filter = df_sub.loc[row_ixs_bln]
    
    return df_filter
    
    

###
# raw file loop
###

#chunksize = 10**5
#num_cks = 40
chunksize = 4e6

df_tot_fin = pd.DataFrame()

tot_eng_lng_qss = 0
tot_FI_rows = 0

for file_index, chunk in enumerate(pd.read_csv(pathname+raw_filename, 
                                      chunksize=chunksize)):
    
    print("working on file index %s" % (file_index+1))
    
    # DEBUG:
    #if file_index > 0:
    #    break
    
    # read in dataframe row index file for unique English questions
    idx_filename = 'eng_qss_ids/unq_eng_qss_idx_'+str(file_index+1)+'.csv'
    df_ixs = pd.read_csv(pathname+idx_filename)

    df_sub = chunk[chunk.index.isin(df_ixs['org_idx'])].reset_index(
        names='org_idx')[['org_idx','question_content','question_id']]
    print("file index %s, read in %s rows; reduced to %s rows" %
          (file_index+1,len(chunk),len(df_sub)))
    
    df_res = proc_data(df_sub,spell_corr=True)
    
    tot_eng_lng_qss += len(df_sub)
    tot_FI_rows += len(df_res)
    
    df_tot_fin = pd.concat([df_tot_fin,df_res],ignore_index=True)
    
    print("processed for FI keywords; %s rows" % (len(df_res)))
    
print("%s dataframe rows to save total" % tot_FI_rows)
df_tot_fin.to_csv(pathname+'FI_filter_keywords.csv',
                 index=False)


