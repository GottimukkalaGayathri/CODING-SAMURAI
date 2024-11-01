import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
calendar = pd.read_csv('../data/calendar.csv')  # Adjust path as needed
listings = pd.read_csv('../data/listings.csv')  # Adjust path as needed
reviews = pd.read_csv('../data/reviews.csv')    # Adjust path as needed

# Explore the datasets
print("Listings dataset:")
print(listings.head())
print("\nBasic statistics for listings dataset:")
print(listings.describe())

print("\nCalendar dataset:")
print(calendar.head())
print("\nBasic statistics for calendar dataset:")
print(calendar.describe())

print("\nReviews dataset:")
print(reviews.head())
print("\nBasic statistics for reviews dataset:")
print(reviews.describe())

# Data cleaning
# Convert price to numeric, removing dollar signs or commas if necessary
if 'price' in listings.columns:
    listings['price'] = listings['price'].replace('[\$,]', '', regex=True).astype(float)

# Check for missing values in the listings dataset
missing_values = listings.isnull().sum()
print("\nMissing values in listings dataset:")
print(missing_values[missing_values > 0])

# Drop duplicates in the listings dataset
listings_cleaned = listings.drop_duplicates()
print("\nRemoved duplicates from listings dataset. New shape:")
print(listings_cleaned.shape)

# Similar checks for calendar and reviews datasets
missing_calendar = calendar.isnull().sum()
print("\nMissing values in calendar dataset:")
print(missing_calendar[missing_calendar > 0])

missing_reviews = reviews.isnull().sum()
print("\nMissing values in reviews dataset:")
print(missing_reviews[missing_reviews > 0])

# Visualization section
sns.set(style="whitegrid")

# 1. Distribution of prices in the listings dataset
plt.figure(figsize=(10, 6))
sns.histplot(listings_cleaned['price'].dropna(), bins=30, kde=True)
plt.title('Distribution of Airbnb Listing Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.savefig('../output/visuals/price_distribution.png')  # Save the plot
plt.show()

# 2. Count of different property types
plt.figure(figsize=(10, 6))
sns.countplot(data=listings_cleaned, y='property_type', order=listings_cleaned['property_type'].value_counts().index)
plt.title('Count of Airbnb Listings by Property Type')
plt.xlabel('Count')
plt.ylabel('Property Type')
plt.savefig('../output/visuals/property_type_counts.png')  # Save the plot
plt.show()

# 3. Average price by neighborhood
if 'neighbourhood' in listings_cleaned.columns:
    plt.figure(figsize=(12, 6))
    average_price_neighbourhood = listings_cleaned.groupby('neighbourhood')['price'].mean().reset_index()
    sns.barplot(data=average_price_neighbourhood.sort_values('price', ascending=False),
                x='neighbourhood', y='price')
    plt.title('Average Price of Airbnb Listings by Neighbourhood')
    plt.xlabel('Neighbourhood')
    plt.ylabel('Average Price')
    plt.xticks(rotation=45)
    plt.savefig('../output/visuals/average_price_by_neighbourhood.png')  # Save the plot
    plt.show()

# Step 6: Time Series Analysis

# Check the reviews dataset for a date field
print(reviews.head())

# Ensure the date column is in datetime format
reviews['date'] = pd.to_datetime(reviews['date'])

# 1. Count of Listings Over Time
listings_count = reviews.groupby(reviews['date'].dt.to_period('M')).size()
listings_count.index = listings_count.index.to_timestamp()  # Convert PeriodIndex to TimestampIndex

plt.figure(figsize=(12, 6))
plt.plot(listings_count.index, listings_count.values, marker='o')
plt.title('Count of Airbnb Listings Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Listings')
plt.xticks(rotation=45)
plt.grid()
plt.savefig('../output/visuals/listings_count_over_time.png')  # Save the plot
plt.show()

# 2. Average Price Over Time
# First, we need to merge the reviews and listings data on the listing_id
merged_data = pd.merge(reviews, listings[['id', 'price']], left_on='listing_id', right_on='id')

# Convert price to numeric, removing any currency symbols
merged_data['price'] = merged_data['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Now group by date and calculate average price
average_price = merged_data.groupby(merged_data['date'].dt.to_period('M'))['price'].mean()
average_price.index = average_price.index.to_timestamp()  # Convert PeriodIndex to TimestampIndex

plt.figure(figsize=(12, 6))
plt.plot(average_price.index, average_price.values, color='orange', marker='o')
plt.title('Average Price of Airbnb Listings Over Time')
plt.xlabel('Date')
plt.ylabel('Average Price')
plt.xticks(rotation=45)
plt.grid()
plt.savefig('../output/visuals/average_price_over_time.png')  # Save the plot
plt.show()

# Step 7: Correlation Analysis

# First, we need to ensure that we have relevant numerical columns
# Let's create a new DataFrame with selected columns for correlation analysis

# Select relevant features
correlation_data = listings_cleaned[['price', 'bedrooms', 'number_of_reviews', 'review_scores_rating']]

# Calculate correlation matrix
correlation_matrix = correlation_data.corr()

# Display the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# Create a heatmap to visualize the correlations
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Heatmap of Airbnb Listings Features')
plt.savefig('../output/visuals/correlation_heatmap.png')  # Save the plot
plt.show()
