import sys
import run_mf, run_user, run_item # Recommender System Functions
from graphing import versusN

mongo_collection = sys.argv[1] # Get the mongo collection name
# Create the dictionary datasets

max_N = 2

mf_ndcg, mf_r = run_mf.run(mongo_collection, max_N)
item_ndcg, item_r = run_item.run(mongo_collection, max_N)
user_ndcg, user_r = run_user.run(mongo_collection, max_N)

print("Completed data collection... Creating graphs...")
versusN.n_vs_r_precision(user_r, item_r, mf_r, mongo_collection)
versusN.n_vs_ndcg(user_ndcg, item_ndcg, mf_ndcg, mongo_collection)
print("Done!")
