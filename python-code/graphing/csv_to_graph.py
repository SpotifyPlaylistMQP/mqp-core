import csv
import sys
import pprint
from master_grapher import *

# Function to convert a csv file to a dict
def convert_to_dict(csv_file):
    try:
        reader = csv.DictReader(open(csv_file, 'rb'))
    	created_dict = []
    	for line in reader:
    		created_dict.append(line)
    	return clean_dict(created_dict)
    except Exception, e:
        print(e)

def clean_dict(dirty_dict):
    clean_dict = dict()
    for i in range(len(dirty_dict)):
        clean_dict[int(dirty_dict[i]['N'])] = str(dirty_dict[i][' NDCG'])
    return clean_dict

def get_mf_ndcg(dataset):
    mf_feature_csv = '../evaluation_data/feature_mf_' + dataset
    mf_normal_csv = '../evaluation_data/mf_' + dataset
    mf_feat_dict = convert_to_dict(mf_feature_csv)
    mf_normal_dict = convert_to_dict(mf_normal_csv)
    return mf_normal_dict, mf_feat_dict

def get_user_item_ndcg(dataset):
    user_csv = '../evaluation_data/user_' + dataset
    item_csv = '../evaluation_data/item_' + dataset
    user_dict = convert_to_dict(user_csv)
    item_dict = convert_to_dict(item_csv)
    return user_dict, item_dict

# Main function
def main():
    dataset = None
    if(len(sys.argv) > 1):
        argument = sys.argv[1]
    else:
        print('No command argument entered!')
        exit()

    if(str(argument) == '-1'):
        print('Running graph evaluation with [..]_mpd_square_100')
        dataset = 'mpd_square_100'
    elif(str(argument) == '-2'):
        print('Running graph evaluation with [..]_mpd_square_1000')
        dataset = 'mpd_square_1000'
    else:
        print('Invalid argument entered!')
        print('-1 run with [..]_mpd_square_100')
        print('-2 run with [..]_mpd_square_1000')
        exit()

    mf_normal_dict, mf_feat_dict = get_mf_ndcg(dataset)
    user_dict, item_dict = get_user_item_ndcg(dataset)
    try:
        compare_ndcg(mf_normal_dict, mf_feat_dict, 'mf_mpd_square_100')
    except Exception, e:
        print(e)
    try:
        super_ndcg(mf_normal_dict, mf_feat_dict, user_dict, item_dict, 'mf_mpd_square_100')
    except Exception, e:
        print(e)

if __name__== "__main__":
  main()
