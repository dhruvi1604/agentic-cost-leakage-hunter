import pandas as pd
from src.features.build_features import build_all_features
def make_sample_df():
    return pd.DataFrame(
        {
            "vendor":["Acme","Acme","Acme","Globex"],
            "amount":[100.0,2000.0,500.0,250.0],
        }
    )
    
def test_build_all_features_adds_columns():
    df=build_all_features(make_sample_df())
    
    assert "vendor_txn_count" in df.columns
    assert "vendor_zscore" in df.columns
    
def test_vendor_txn_count_is_correct():
    df=build_all_features(make_sample_df())
    
    acme=df[df["vendor"]=="Acme"]
    assert acme["vendor_txn_count"].unique().tolist()==[3]
    
    
    
#make_sample_df a tiny fake dataset 4 rows invented vendors this key idea of unit testing 
#feed function a small input where you already know the right answer thencheck it 

#test1 calls your build_all_features function and asserts the engineered columns exist 
# if someone accidentally renames vendor_zscore this turns red before a broken img ships
#test 3 acme appears appears in the fake data so vendor_txn_count for acme rows must be 3 
#we knw bcz we built the input if the groupby logic ever breaks reb
    
    
