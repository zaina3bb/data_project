# A Real-World Approach to Data Analysis
# ------------------------------------------------------------------------------------------------------------------------------------

# Introduction to What a Data Analyst Does
# A data analyst plays a crucial role in today’s data-driven world. Their primary responsibility is to gather, process, 
# and analyze data to help businesses make informed decisions. They use statistical techniques, visualization tools,
# and data modeling to uncover patterns and insights that can improve operations, boost profitability, and meet
# organizational goals. In this set of tasks, you will step into the shoes of a data analyst and work with a real-world dataset
# to derive meaningful conclusions and actionable insights.
# ------------------------------------------------------------------------------------------------------------------------------------

# Explanation of the Dataset
# You will be working with a dataset containing 10,000 customer transactions from a retail business. The dataset includes information on:

# * Customer_ID: Unique identifier for each customer.
# * Transaction_ID: Unique identifier for each transaction.
# * Transaction_Date: Date of each transaction.
# * Product_Category: Category of the purchased product (e.g., Beauty, Clothing, Books).
# * Product_Name: Specific product name.
# * Quantity: Number of units purchased.
# * Unit_Price: Price per unit of the product.
# * Unit_Cost: Cost per unit of the product.
# * Payment_Method: Method of payment (e.g., PayPal, Debit Card).
# * Region: Geographic location of the transaction (e.g., Baghdad, Basra, Erbil).
# * Gender: Gender of the customer.
# * Age: Age of the customer.

# Your goal is to analyze the dataset and complete specific tasks outlined below.
# ------------------------------------------------------------------------------------------------------------------------------------

# Tasks for Analysis

# 1. Customer Behavior Analysis
#		* Calculate the number of transactions for each customer.
#		* Identify high-frequency buyers and their total spending.
#		* Segment customers by their spending habits and demographics.

# 2. Product Performance
# 		* Identify the top-selling products by quantity and revenue.
# 		* Determine the most popular product categories.
# 		* Analyze profitability for each product by calculating the profit margin (Unit_Price - Unit_Cost).

# 3. Temporal Patterns
# Extract the year, month, and day from the transaction dates.
# Analyze sales trends over time to identify peak and low periods.
# Examine whether certain seasons or months have higher sales volumes.

# 4. Location-Based Insights
# 		* Analyze sales performance by region (e.g., total revenue per region).
# 		* Identify which regions prefer specific product categories or payment methods.
# 		* Suggest localized marketing strategies based on findings.

# 5. Payment Trends
# 		* Determine the most commonly used payment methods.
# 		* Analyze whether high-value transactions are associated with specific payment methods.
# 		* Investigate if payment preferences differ by region or customer demographics.

# 6. Demographics Analysis
# 		* Examine the relationship between age and spending habits.
# 		* Determine whether gender influences product preferences or spending levels.
# 		* Segment customers into demographic groups and analyze their behaviors.

# 7. Revenue and Growth Opportunities
# 		* Identify high-value customers who contribute significantly to revenue.
# 		* Suggest upselling or cross-selling strategies based on purchase patterns.
# 		* Analyze how discounts might influence sales volumes if data is available.

# 8. Potential Issues to Investigate
# 		* Check for missing or inconsistent data entries.
# 		* Identify outliers in quantity or unit price that might indicate errors.
# 		* Ensure that transaction dates are in a logical chronological order.

# 9. Reporting and Visualizations
# 		* Create bar charts for product and category sales.
# 		* Use line charts to visualize sales trends over time.
# 		* Generate pie charts to represent payment method distributions.
# 		* Design heatmaps to show regional demand for products.
# ------------------------------------------------------------------------------------------------------------------------------------

# Instructions
# Each task should be completed using appropriate tools. For tasks involving calculations or trends, document your findings clearly to provide insights.
# For visualization tasks, create clean and professional charts that communicate your insights effectively.
# By completing these tasks, you will gain hands-on experience in data analysis, enabling you to approach real-world datasets with confidence and analytical precision.

import pandas as pd 
import streamlit as st
# import matplotlib.pyplot as plt

df=pd.read_csv("./data/e_commerce_data.csv")

# 1. Customer Behavior Analysis
df['Customer_ID'] = df['Customer_ID'].astype(str)
#print(df.columns)
Number_of_trans=df.groupby("Customer_ID")['Transaction_ID'].count().reset_index()
Number_of_trans.columns=["Customer_ID",'Number_of_Transaction']
Number_of_trans=Number_of_trans.sort_values("Number_of_Transaction",ascending=False)
print("The total Number of Transactions for each Customer :")
print(Number_of_trans)

print(df.info())

#df["Unit_Price"]=df["Unit_Price"].astype(float)#it is already float 
df["Quantity"]=df["Quantity"].astype(float)
df['Total_Spent']=df["Unit_Price"]* df["Quantity"]

mean=Number_of_trans['Number_of_Transaction'].mean()
high_frequency_buyers=Number_of_trans[Number_of_trans['Number_of_Transaction']>mean]
high_frequency_buyers=pd.merge(high_frequency_buyers,df.groupby("Customer_ID")['Total_Spent'].sum().reset_index(),on="Customer_ID")

print("\nhigh frequency buyers:")
print(high_frequency_buyers)


low=df['Total_Spent'].quantile(0.25)

high =df['Total_Spent'].quantile(0.75)
#print(high)

df['Spending_Segment']='Medium'
df.loc[df['Total_Spent']<=low,'Spending_Segment']='Low'
df.loc[df['Total_Spent']>high,'Spending_Segment']='High'
spending_segment=df[['Customer_ID', 'Total_Spent', 'Spending_Segment']]
print(spending_segment)


df['Age_Segment']='Adult'
df.loc[df['Age']<18,'Age_Segment']=' Below 18'
df.loc[(df ['Age']>18) & (df ['Age']<=35),'Age_Segment']='Young Adult'
df.loc[df['Age']>50,'Age_Segment']="Senior"


print(df[['Customer_ID', 'Total_Spent','Age' ,'Age_Segment']])

df['Demographics_Segment']=df['Gender']+" "+df['Age_Segment']

print(df[['Customer_ID', 'Demographics_Segment','Total_Spent']])

#now we can group them and see which group spent more 

df_filtered=df.groupby('Demographics_Segment')['Total_Spent'].sum().reset_index()
df_filtered=df_filtered.sort_values("Total_Spent",ascending=False)
print(df_filtered)


#print(df.head)

df.to_csv('./new.csv')




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 2. Product Performance

Top_selling=df.groupby('Product_Name').agg({"Quantity":"sum" , "Total_Spent":"sum"})
Top_selling = Top_selling.sort_values("Total_Spent",ascending=False)
print("\nThe Top selling Product are:")
print(Top_selling)
Top_selling.to_csv('./Top_selling.csv')


popular_categories=df.groupby('Product_Category')['Product_Name'].count().reset_index()
popular_categories.columns=["Product_Category",'Total_products']
print("")
print(popular_categories)


df['profit']=df['Unit_Price']-df['Unit_Cost']

profitability=df.groupby("Product_Name")['profit'].sum().reset_index()
profitability = profitability.sort_values("profit",ascending=False).reset_index(drop=True)
print("\nProfitability Analyzation:")
print(profitability)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#3. Temporal Patterns
df['Transaction_Date']=pd.to_datetime(df['Transaction_Date'])
df['Year']=df['Transaction_Date'].dt.year
df['Month']=df['Transaction_Date'].dt.month
df['Day']=df['Transaction_Date'].dt.day

#print(df.columns)

sales_trends=df.groupby(["Year","Month"])['Total_Spent'].sum().reset_index()
print(sales_trends)
sales_trends_by_totalspent=sales_trends.sort_values("Total_Spent",ascending=False).reset_index(drop=True)
peak_period = sales_trends_by_totalspent.iloc[0]
low_period=sales_trends_by_totalspent.iloc[-1]
print(f"the peak period is: \n{peak_period}\nthe low period is: \n{low_period}")




month_to_season = {
    1: 'Winter', 2: 'Winter', 3: 'Winter',
    4: 'Spring', 5: 'Spring', 6: 'Spring',
    7: 'Summer', 8: 'Summer', 9: 'Summer',
    10: 'Fall', 11: 'Fall', 12: 'Fall'
    }

df["Season"]=df['Transaction_Date'].dt.month.map(month_to_season)

sales_trends_by_season=df.groupby('Season')["Total_Spent"].sum().reset_index()
sales_trends_by_season=sales_trends_by_season.sort_values("Total_Spent",ascending=False).reset_index(drop=True)
print("\nSales trends by season:")
print(sales_trends_by_season)
peak_period_by_season = sales_trends_by_season.iloc[0] #idk why when i used min and max it's gave a wrong values
low_period_by_season=sales_trends_by_season.iloc[-1]
print(f"the peak period is: \n{peak_period_by_season}\nthe low period is: \n{low_period_by_season}")






#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 #4. Location-Based Insights

Sales_by_region=df.groupby('Region')['Total_Spent'].sum().reset_index()
Sales_by_region=Sales_by_region.sort_values("Total_Spent",ascending=False).reset_index(drop=True)
Sales_by_region.columns=['Region','Total_Spent']
print("\nSales performance by region:")
print(Sales_by_region)


Categories_preferences=df.groupby(['Region','Product_Category'])['Total_Spent'].sum().reset_index()
Categories_preferences=Categories_preferences.loc[Categories_preferences.groupby("Region")["Total_Spent"].idxmax()]
Categories_preferences = Categories_preferences.reset_index(drop=True)

print("\nProduct Categories preferences by region:")
print(Categories_preferences)

#* Suggest localized marketing strategies based on findings.... idk how to do that:(  ,is it just suggestion and have nothing to do with coding?!



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 5. Payment Trends

common_PM=df.groupby("Payment_Method")["Total_Spent"].sum().reset_index()
common_PM=common_PM.sort_values("Total_Spent", ascending=False)
print(common_PM)
print(f"\nThe most common payment method is {common_PM.iloc[0,0]}")  #iloc is so cool


segment_count=df.groupby(['Payment_Method', 'Spending_Segment']).size().reset_index(name='Count')
print(segment_count)
pivot_table = segment_count.pivot(index='Payment_Method', columns='Spending_Segment', values='Count').fillna(0)
print(pivot_table)

payment_method=df.groupby(['Region','Payment_Method'])["Total_Spent"].sum().reset_index()
payment_method=payment_method.loc[payment_method.groupby("Region")["Total_Spent"].idxmax()]
payment_method= payment_method.reset_index(drop=True)
payment_method=payment_method.drop(columns=["Total_Spent"])
print("\nPayment_Method performance based on region:")
print(payment_method)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6. Demographics Analysis

Spending_based_on_age=df.groupby("Age_Segment")["Total_Spent"].sum().reset_index()
Spending_based_on_age=Spending_based_on_age.sort_values("Total_Spent",ascending=False).reset_index(drop=True)
print("\nSales performance by age:")
print(Spending_based_on_age)

Gender_preferences=df.groupby(["Gender","Product_Name"])["Total_Spent"].sum().reset_index()

Gender_preferences=Gender_preferences.sort_values("Total_Spent",ascending=False).reset_index(drop=True)
#print(Gender_preferences)
# pivot_table_2 =Gender_preferences.pivot(index='Product_Name', columns='Gender', values='Total_Spent').fillna(0)
# print(pivot_table_2)
Top_Product_by_Gender=Gender_preferences.loc[Gender_preferences.groupby("Gender")["Total_Spent"].idxmax()].reset_index(drop=True)
print("\n Top Product based on gender:")
print(Top_Product_by_Gender)
Males_preferences=Gender_preferences[Gender_preferences["Gender"]=="Male"].reset_index(drop=True)
print("\nProducts preferences based on gender(Males only):")
print(Males_preferences)
Females_preferences=Gender_preferences[Gender_preferences["Gender"]=="Female"].reset_index(drop=True)
print("\nProducts preferences based on gender(Females only):")
print(Females_preferences)


behavior_analysis=df.groupby('Demographics_Segment').agg({"Total_Spent":['mean',"median","sum"],"Customer_ID":"count"}).reset_index()
behavior_analysis.columns = ['Demographics_Segment', 'Avg_Spent', 'Median_Spent', 'Total_Spent', 'Number_Of_Customer']
behavior_analysis=behavior_analysis.sort_values("Total_Spent",ascending=False)
print("")
print(behavior_analysis)



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 7. Revenue and Growth Opportunities

high_spenders=df[df['Spending_Segment']=='High']
high_spenders=high_spenders.groupby("Customer_ID")["Total_Spent"].sum().reset_index()
print("High-value customers:")
print(high_spenders)

total_revenue=df["Total_Spent"].sum()
high_spenders_revenue=high_spenders["Total_Spent"].sum()
contribution=(high_spenders_revenue/total_revenue)*100
print( f"\nHigh-value customers contribute {contribution:.3f}% to total revenue")

upsell_suggestions = {
    "Biography": "Collector's Edition Biography","Camera": "Mirrorless Camera",
    "Candle": "Scented Candle Set","Cookbook": "Premium Cookbook with Video Tutorials",
    "Curtains": "Designer Curtains", "Dress": "Evening Gown",
    "Foundation": "Long-Lasting Foundation","Headphones": "Noise-Canceling Headphones",
    "Jacket": "Leather Jacket ","Jeans": "Designer Jeans",
    "Lamp": "Smart Lamp ","Laptop": "Premium Business Laptop",
    "Lipstick": "Luxury Lipstick Set","Mascara": "Waterproof Mascara",
    "Misc": "Personalized Miscellaneous Items","Novel": "Special Edition or Signed Copy",
    "Perfume": "Limited Edition Perfume","Smartphone": "Premium Smartphone Model",
    "T-Shirt": "Branded T-Shirt","Textbook": "Annotated Edition ",
    "Vase": "Handcrafted Vase"}


cross_sell_suggestions = {
    "Biography":"Bookmark","Camera":"Camera Bag",
    "Candle":"Candle Holder","Cookbook":"Recipe Notebook",
    "Curtains":"Matching Cushions","Dress":"Jewelry",
    "Foundation":"Makeup Brush","Headphones":"Headphone Case",
    "Jacket":"Scarf","Jeans":"Belt", 
    "Lamp":"Light Bulb","Laptop":"Laptop Bag",
    "Lipstick":"Lip Balm","Mascara":"Eyeliner",
    "Misc":"Personalized Accessories","Novel":"Bookmark", 
    "Perfume":"Body Lotion","Smartphone":"Screen Protector", 
    "T-Shirt":"Sneakers","Textbook":"Notebook",
    "Vase": "Flowers"}


def Cross_sell_suggestions(row):
    if row["Spending_Segment"] in ["Medium", "Low"]:
        return cross_sell_suggestions.get(row["Product_Name"], None)
    else:
        return None
df["cross_sell_suggestions"] = df.apply(Cross_sell_suggestions, axis=1)


def Up_sell_Suggestions(row):
    if row["Spending_Segment"] =="High":
        return upsell_suggestions.get(row["Product_Name"],None)
    else:
        return None
df["Up_sell_Suggestions"]=df.apply(Up_sell_Suggestions,axis=1)

df.to_csv('./new.csv')


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 8. Potential Issues to Investigate

print("Missing values in each column:")
print(df.isnull().sum())


quantity_outliers = df[(df['Quantity'] < 0) | (df['Quantity'] > df['Quantity'].quantile(0.99))]
quantity_outliers=quantity_outliers[["Customer_ID","Quantity"]]
print("\nQuantity outliers:")
print(quantity_outliers)

unit_price_outliers = df[df['Unit_Price'] > df['Unit_Price'].quantile(0.99)]
unit_price_outliers=unit_price_outliers[["Customer_ID","Unit_Price"]]
print("\nUnit price outliers:")
print(unit_price_outliers)

df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])

if not df['Transaction_Date'].is_monotonic_increasing:
    print("Dates are not in order. Sorting them...")
    df = df.sort_values('Transaction_Date')
    print("Dates are in order now ")
else:
    print("Dates are in order")
df.to_csv("df_ordered_dates.csv")



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------



st.set_page_config(page_title="Data Analysis Project", layout="wide")
st.title("Data Analysis Project")


st.sidebar.title('Data Analysis Project')
option = st.sidebar.selectbox('Choose Analysis Type', 
                              ['Customers Behavior', 'Products Performance', 'Temporal Patterns', 
                               'Location-Based Insights', 'Payment Trends', 'Demographics Analysis'])


if option == 'Customers Behavior':
    st.title('Customers Behavior Analysis')
    cols=st.columns(3)
    with cols[0]:
        st.subheader('No. of Transactions per Customer')
        st.write(Number_of_trans)

    with cols[1]:
        st.subheader('High-Frequency Buyers')
        st.write(high_frequency_buyers)
    with cols[2]:
        st.subheader('Spending Segmentation')
        st.write(spending_segment)




   

    
   

# Product Performance
elif option == 'Products Performance':
    st.title('Products Performance Analysis')
    cols = st.columns(2)
    with cols[0]:

        st.subheader('Top Selling Products')
        st.write(Top_selling)
    with cols[1]:
        st.subheader("product sales")

        top_selling=df.groupby('Product_Name').agg({"Quantity":"sum" , "Total_Spent":"sum"})
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(top_selling.index, top_selling["Total_Spent"], color='skyblue')
        ax.set_title("Products Sales Performance")
        ax.set_xlabel("Product")
        ax.set_ylabel("Total Revenue")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    cols=st.columns(2)
    with cols[0]:
        st.subheader('Product Categories')
        st.write(popular_categories)
    with cols[1]:
        categories_sales=df.groupby('Product_Category')['Total_Spent'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(categories_sales["Product_Category"], categories_sales["Total_Spent"], color='pink')
        ax.set_title("Categories Sales Performance ")
        ax.set_xlabel("Product Category")
        ax.set_ylabel("Total Revenue")
        plt.xticks(rotation=45)
        st.pyplot(fig)




    st.subheader('Product Profitability')
    st.write(profitability)

 

  

# Temporal Patterns
elif option == 'Temporal Patterns':
    st.title('Sales Temporal Patterns')

    
    st.subheader('Sales Trends by Year and Month')
    st.write(sales_trends)

 
    st.subheader('Sales by Season')
    st.write(sales_trends_by_season)

    st.subheader("Sales Trends Over Time")
    fig, ax = plt.subplots(figsize=(8, 6))
    sales=df.groupby(["Product_Name","Transaction_Date"])['Total_Spent'].sum().reset_index()
    for product in sales["Product_Name"].unique():
        product_data = sales[sales["Product_Name"] == product]
        ax.plot(product_data["Transaction_Date"], product_data["Total_Spent"], marker="o", label=product)
    ax.set_title("Sales Trends Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Revenue")
    ax.legend(title="Product")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Location-Based Insights
elif option == 'Location-Based Insights':
    st.title('Location-Based Sales Insights')

    st.subheader('Sales by Region')
    st.write(Sales_by_region)
    st.subheader("Product Categories preferences by Region")
    st.write(Categories_preferences)

# Payment Trends
elif option == 'Payment Trends':
    st.title('Payment Trends Analysis')

    st.subheader('Payment Methods Distribution')
    payment_methods = df.groupby("Payment_Method")["Total_Spent"].sum().reset_index().sort_values('Total_Spent', ascending=False)
    st.write(payment_methods)
    st.subheader("Payment_Method performance based on region:")
    st.write(payment_method)
    
    st.subheader('Payment Methods Distribution')
    colors = ['gold', 'lightblue', 'lightgreen','pink']
    fig, ax = plt.subplots()
    ax.pie(common_PM["Total_Spent"], labels=common_PM["Payment_Method"], colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  
    st.pyplot(fig)

# Demographics Analysis
elif option == 'Demographics Analysis':
    st.title('Demographics-Based Analysis')

   
    st.subheader("Spending performance by age:")
    st.write(Spending_based_on_age)
    
    st.subheader('Gender Preferences for Products')
    gender_preferences = df.groupby(["Gender", "Product_Name"])["Total_Spent"].sum().reset_index().sort_values('Total_Spent', ascending=False)
    st.write(gender_preferences)
    st.subheader("\nProducts preferences based on gender(Males only):")
    st.write(Males_preferences)
    st.subheader("\nProducts preferences based on gender(Females only):")
    st.write(Females_preferences)








