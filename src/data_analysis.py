import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Read both datasets
df_adaptations = pd.read_csv('best_movie_adaptations.csv', escapechar='\\')

# Combine datasets and add source column
df_adaptations['source'] = 'adaptation'
df = df_adaptations

# Remove duplicates based on Name and Author
df = df.drop_duplicates(subset=['Name', 'Author'])

def perform_detailed_eda():
    # Set style for better visualization
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    
    # Create figure for all plots
    plt.figure(figsize=(20, 25))
    
    # 1. Rating Distribution Analysis
    plt.subplot(3, 2, 1)
    sns.histplot(data=df, x='Avg Rating', bins=30, color='skyblue')
    plt.title('Distribution of Average Ratings', pad=20, fontsize=14)
    plt.xlabel('Average Rating', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    
    # Calculate skewness and distribution statistics
    valid_ratings = df[df['Avg Rating'] > 0]['Avg Rating']  # Only consider non-zero ratings
    skewness = stats.skew(valid_ratings)
    mean_rating = valid_ratings.mean()
    std_rating = valid_ratings.std()
    
    rating_stats = {
        'distribution_type': 'positively skewed' if skewness > 0 else 'negatively skewed' if skewness < 0 else 'normal',
        'skewness': skewness,
        'rating_range': (valid_ratings.quantile(0.05), valid_ratings.quantile(0.95))
    }
    
    # 2. Popularity Metrics Analysis
    plt.subplot(3, 2, 2)
    sns.scatterplot(data=df[df['Rating Count'] > 0], x='Rating Count', y='Score', alpha=0.6, color='coral')
    plt.xscale('log')
    plt.title('Rating Count vs Score', pad=20, fontsize=14)
    plt.xlabel('Rating Count (log scale)', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    
    # Calculate correlation (excluding zeros)
    valid_data = df[(df['Rating Count'] > 0) & (df['Score'] > 0)]
    correlation = valid_data['Rating Count'].corr(valid_data['Score'])
    
    # 3. Vote Count vs Average Rating
    plt.subplot(3, 2, 3)
    sns.scatterplot(data=df[df['Vote Count'] > 0], x='Vote Count', y='Avg Rating', alpha=0.6, color='green')
    plt.title('Vote Count vs Average Rating', pad=20, fontsize=14)
    plt.xlabel('Vote Count', fontsize=12)
    plt.ylabel('Average Rating', fontsize=12)
    
    # 4. Top Books Analysis (excluding zero ratings)
    plt.subplot(3, 2, 4)
    top_rated = df[df['Avg Rating'] > 0].nlargest(10, 'Avg Rating')
    sns.barplot(data=top_rated, y='Name', x='Avg Rating', color='purple')
    plt.title('Top 10 Highest Rated Books', pad=20, fontsize=14)
    plt.xlabel('Average Rating', fontsize=12)
    
    # 5. Most Popular Books (excluding zero ratings)
    plt.subplot(3, 2, 5)
    most_popular = df[df['Rating Count'] > 0].nlargest(10, 'Rating Count')
    sns.barplot(data=most_popular, y='Name', x='Rating Count', color='orange')
    plt.title('Top 10 Most Rated Books', pad=20, fontsize=14)
    plt.xlabel('Number of Ratings', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('eda_analysis.png', dpi=300, bbox_inches='tight')
    
    # Generate detailed analysis report
    analysis_report = {
        'Rating Distribution': {
            'distribution_type': rating_stats['distribution_type'],
            'skewness': round(rating_stats['skewness'], 3),
            'most_common_range': f"{rating_stats['rating_range'][0]:.2f} - {rating_stats['rating_range'][1]:.2f}",
            'mean_rating': round(mean_rating, 2),
            'std_rating': round(std_rating, 2)
        },
        'Popularity Metrics': {
            'rating_score_correlation': round(correlation, 3),
            'rating_count_range': f"{valid_data['Rating Count'].min():,} - {valid_data['Rating Count'].max():,}",
            'score_range': f"{valid_data['Score'].min():.1f} - {valid_data['Score'].max():.1f}"
        },
        'Top Books': {
            'by_rating': df[df['Avg Rating'] > 0].nlargest(3, 'Avg Rating')[['Name', 'Author', 'Avg Rating']].drop_duplicates().to_dict('records'),
            'by_popularity': df[df['Rating Count'] > 0].nlargest(3, 'Rating Count')[['Name', 'Author', 'Rating Count']].drop_duplicates().to_dict('records')
        }
    }
    
    # Print detailed analysis
    print("\n=== Detailed EDA Analysis ===")
    print("\n1. Rating Distribution:")
    print(f"- Distribution type: {analysis_report['Rating Distribution']['distribution_type']}")
    print(f"- Skewness: {analysis_report['Rating Distribution']['skewness']}")
    print(f"- Most books rate between: {analysis_report['Rating Distribution']['most_common_range']} stars")
    print(f"- Mean rating: {analysis_report['Rating Distribution']['mean_rating']}")
    print(f"- Standard deviation: {analysis_report['Rating Distribution']['std_rating']}")
    
    print("\n2. Popularity Metrics:")
    print(f"- Correlation between rating count and score: {analysis_report['Popularity Metrics']['rating_score_correlation']}")
    print(f"- Rating count range: {analysis_report['Popularity Metrics']['rating_count_range']}")
    print(f"- Score range: {analysis_report['Popularity Metrics']['score_range']}")
    
    print("\n3. Top Books by Rating:")
    for i, book in enumerate(analysis_report['Top Books']['by_rating'], 1):
        print(f"{i}. {book['Name']} by {book['Author']} (Rating: {book['Avg Rating']:.2f})")
    
    print("\n4. Top Books by Popularity (Rating Count):")
    for i, book in enumerate(analysis_report['Top Books']['by_popularity'], 1):
        print(f"{i}. {book['Name']} by {book['Author']} ({book['Rating Count']:,} ratings)")
    
    return analysis_report

# Run the analysis
try:
    analysis_results = perform_detailed_eda()
    print("\nAnalysis completed successfully!")
except Exception as e:
    print(f"An error occurred during analysis: {str(e)}")
    print("Please ensure you have all required packages installed:")
    print("pip install pandas matplotlib seaborn scipy numpy")