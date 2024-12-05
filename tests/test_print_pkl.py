import pandas as pd

data_path = "./final_result.pkl"
try:
    faq_data = pd.read_pickle(data_path)
    if isinstance(faq_data, dict):
        faq_df = pd.DataFrame({
            "question": list(faq_data.keys()),
            "answer": list(faq_data.values())
        })

        print(faq_df.tail(100))

except Exception as e:
    print(e)
