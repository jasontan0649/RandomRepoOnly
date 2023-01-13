# import pickle
# import pandas as pd

class models_features:
    regression_feature_cols = [
        "Race",
        "Gender",
        "Body_Size",
        "Age_Range",
        "Kids_Category",
        "Basket_Size",
        "Basket_colour",
        "Attire",
        "Shirt_Colour",
        "shirt_type",
        "Pants_Colour",
        "pants_type",
        "Wash_Item",
        "Washer_No",
        "Dryer_No",
        "Spectacles",
        "TimeSpent_minutes",
        "buyDrinks",
        "Num_of_Baskets",
        "City",
        "State",
        "Postcode",
        "Temperature",
        "humidity",
        "windspeed",
        "conditions",
        "isRain",
        "DayOfWeek",
        "HourInDay",
    ]
    regression_target = "TotalSpent_RM"
    classification_feature_cols = [
        "Race",
        "Gender",
        "Body_Size",
        "Age_Range",
        "Kids_Category",
        "Basket_Size",
        "Basket_colour",
        "Attire",
        "Shirt_Colour",
        "shirt_type",
        "Pants_Colour",
        "pants_type",
        "TotalSpent_RM",
        "Washer_No",
        "Dryer_No",
        "Spectacles",
        "TimeSpent_minutes",
        "buyDrinks",
        "Num_of_Baskets",
        "City",
        "State",
        "Postcode",
        "Temperature",
        "humidity",
        "windspeed",
        "conditions",
        "isRain",
        "DayOfWeek",
        "HourInDay",
    ]

    label_encoding_columns = [
        "Race",
        "Gender",
        "Body_Size",
        "Kids_Category",
        "Basket_Size",
        "Basket_colour",
        "Attire",
        "Shirt_Colour",
        "shirt_type",
        "Pants_Colour",
        "pants_type",
        "Wash_Item",
        "Washer_No",
        "Dryer_No",
        "Spectacles",
        "City",
        "State",
        "Postcode",
        "conditions",
        "isRain",
        "DayOfWeek",
    ]
    classification_target = "Wash_Item"

# df = pd.read_csv("processed_data.csv")
# # Perform label encoding from the categorical cols input data first
# for col in label_encoding_columns:
#     print(col)
#     pkl_file = open(f"./encoders/{col}_encoder.pkl", "rb")
#     label_encoder = pickle.load(pkl_file)
#     pkl_file.close()
#     df[col] = label_encoder.transform(df[col])
# model = pickle.load("model.pkl")
# model
# print(df.info())
