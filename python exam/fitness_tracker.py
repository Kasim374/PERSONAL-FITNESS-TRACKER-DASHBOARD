
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class FitnessTracker:
    def __init__(self, filename='fitness_activities.csv'):
        self.my_file = filename
        self.data = None
        self.load_my_csv()

    def load_my_csv(self):
        """Loads data and handles the 'Data Handling' requirement"""
        try:
 # Using Pandas to load the CSV
            self.data = pd.read_csv(self.my_file)
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            
 #  Create a computed metric column
            self.data['Cals_Per_Min'] = self.data['Calories Burned'] / self.data['Duration']
            print("Successfully connected to CSV file.")
        except:
  # Simple error handling for missing file
            print("Error: Could not find the CSV. Creating a blank list.")
            self.data = pd.DataFrame(columns=['Date', 'Activity Type', 'Duration', 'Calories Burned'])

    def log_activity(self, activity, time_spent, calories):
        """Adds new activity with basic validation"""
 #  Use conditional logic for validation
        if time_spent <= 0 or calories <= 0:
            print("Invalid input! Time and Calories must be positive.")
            return
            
        new_entry = {
            'Date': datetime.now().strftime('%Y-%m-%d'),
            'Activity Type': activity,
            'Duration': time_spent,
            'Calories Burned': calories
        }
        
# Adding new row to the dataframe
        self.data = pd.concat([self.data, pd.DataFrame([new_entry])], ignore_index=True)
        print(f"Added {activity} to your log.")

    def filter_data(self, activity_name):
        """Requirement: Filter activities based on type"""
# Simple filtering logic
        filtered = self.data[self.data['Activity Type'] == activity_name]
        print(f"\n--- Showing results for: {activity_name} ---")
        print(filtered)

    def do_math_analysis(self):
        """Requirement: Use NumPy for numerical analysis"""
        if self.data.empty:
            return
         
 # Using NumPy for averages and totals
        avg_cals = np.mean(self.data['Calories Burned'])
        total_time = np.sum(self.data['Duration'])
        
# Requirement: Group data by activity type
        group_totals = self.data.groupby('Activity Type')['Duration'].sum()
        
        print("\n--- Summary Report ---")
        print(f"Average Burn: {avg_cals}")
        print(f"Total Minutes Trained: {total_time}")
        print("\nTime spent per category:")
        print(group_totals)

    def create_visuals(self):
        """Requirement: High Weightage Visualization"""
        plt.figure(figsize=(10, 8))

        # 1. Bar Chart: Time per activity
        plt.subplot(2, 2, 1)
        sns.barplot(data=self.data, x='Activity Type', y='Duration')
        plt.title('Time Distribution')

        # 2. Line Graph: Progress over time
        plt.subplot(2, 2, 2)
        plt.plot(self.data['Date'], self.data['Calories Burned'], marker='x', color='red')
        plt.title('Burning Trend')
        plt.xticks(rotation=45)

        # 3. Pie Chart: Activity Percentage
        plt.subplot(2, 2, 3)
        self.data['Activity Type'].value_counts().plot.pie(autopct='%1.0f%%')
        plt.title('Activity Mix')

        # 4. Heatmap: Correlation
        plt.subplot(2, 2, 4)
        sns.heatmap(self.data[['Duration', 'Calories Burned']].corr(), annot=True)
        plt.title('Metric Correlation')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
 
    tracker = FitnessTracker('fitness_activities.csv')
    
    # 1. Activity Logging
    tracker.log_activity('Running', 30, 300)
    
    # 2. Analysis and Metrics
    tracker.do_math_analysis()
    
    # 3. Data Filtering
    tracker.filter_data('Yoga')
    
    # 4. Visualization
    tracker.create_visuals()

