# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])





#District Summary
total_number_schools = school_data["school_name"].count()
total_number_students = student_data["student_name"].count()
total_budget = school_data["budget"].sum()
avg_math_score = student_data["math_score"].mean()
avg_reading_score = student_data["reading_score"].mean()
overall_passing_rate = (avg_math_score + avg_reading_score)/2
percent_students_passing_math_score = school_data_complete.query("math_score > 70")["School ID"].count() / total_number_students * 100
percent_students_passing_reading_score = school_data_complete.query("reading_score > 70")["School ID"].count() / total_number_students * 100

district_summary = pd.DataFrame({"Total Schools":[total_number_schools],
                                 "Total Students":[total_number_students],
                                 "Total Budget":[total_budget],
                                 "Average Math Score":[avg_math_score],
                                 "Average Reading Score":[avg_reading_score],
                                 "% Passing Math":[percent_students_passing_math_score],
                                 "% Passing Reading":[percent_students_passing_reading_score],
                                 "% Overall Passing Rate":[overall_passing_rate]})
district_summary






#School Summary
school_data_complete_new = school_data_complete[["School ID", "school_name", "type", "size", "budget", "Student ID", "student_name", "gender", "grade", "reading_score", "math_score"]].copy()
school_data_complete_new.head()

grouped_school_data = school_data_complete_new.groupby(['school_name', "type"])
total_students_each = grouped_school_data["Student ID"].count()
total_school_budget_each = grouped_school_data["budget"].mean()
per_student_budget_each = total_school_budget_each / total_students_each
avg_math_score_each =  grouped_school_data["math_score"].mean()
avg_reading_score_each = grouped_school_data["reading_score"].mean()
percent_students_passing_math_score_each = school_data_complete[school_data_complete["math_score"]>=70].groupby("school_name")["Student ID"].count()/ total_students_each *100
percent_students_passing_reading_score_each = school_data_complete[school_data_complete["reading_score"]>=70].groupby("school_name")["Student ID"].count()/ total_students_each *100
overall_passing_rate_each = (percent_students_passing_math_score_each + percent_students_passing_reading_score_each)/2

school_summary = pd.DataFrame({"Total Students":total_students_each,
                               "Total School Budget":total_school_budget_each,
                               "Per Student Budget":per_student_budget_each,
                               "Average Math Score":avg_math_score_each,
                               "Average Reading Score":avg_reading_score_each,
                               "% Passing Math":percent_students_passing_math_score_each,
                               "% Passing Reading":percent_students_passing_reading_score_each,
                               "% Overall Passing Rate":overall_passing_rate_each})
school_summary





#Top Performing Schools (By Passing Rate)
Top_schools = school_summary.sort_values(["% Overall Passing Rate"], ascending=False)
Top_schools.head()





#Bottom Performing Schools (By Passing Rate)
bottom_schools = school_summary.sort_values(["% Overall Passing Rate"], ascending=True)
bottom_schools.head()





#Math Score by Grade
nineth_graders = school_data_complete[school_data_complete["grade"] == "9th"]
tenth_graders = school_data_complete[school_data_complete["grade"] == "10th"]
eleventh_graders = school_data_complete[school_data_complete["grade"] == "11th"]
twelfth_graders = school_data_complete[school_data_complete["grade"] == "12th"]

nineth_graders_scores = nineth_graders.groupby(["school_name"]).mean()["math_score"]
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()["math_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()["math_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()["math_score"]

scores_each_grades = pd.DataFrame({"9th": nineth_graders_scores,
                                   "10th":tenth_graders_scores,
                                   "11th":eleventh_graders_scores,
                                   "12th":twelfth_graders_scores})
scores_each_grades





#Reading Score by Grade
nineth_graders = school_data_complete[school_data_complete["grade"] == "9th"]
tenth_graders = school_data_complete[school_data_complete["grade"] == "10th"]
eleventh_graders = school_data_complete[school_data_complete["grade"] == "11th"]
twelfth_graders = school_data_complete[school_data_complete["grade"] == "12th"]

nineth_graders_scores = nineth_graders.groupby(["school_name"]).mean()["reading_score"]
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()["reading_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()["reading_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()["reading_score"]

scores_each_grades = pd.DataFrame({"9th": nineth_graders_scores,
                                   "10th":tenth_graders_scores,
                                   "11th":eleventh_graders_scores,
                                   "12th":twelfth_graders_scores})
scores_each_grades





# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

# Combine the data into a single dataset
school_data_complete["spending"] = pd.cut(school_data_complete["budget"]/school_data_complete["size"], spending_bins, labels = group_names)

#group by spending
by_spending = school_data_complete.groupby("spending")

#calculations
avg_math = by_spending["math_score"].mean()
avg_read = by_spending["reading_score"].mean()
pass_math = school_data_complete[school_data_complete["math_score"] >= 70].groupby("spending")["Student ID"].count()/by_spending["Student ID"].count() *100
pass_read = school_data_complete[school_data_complete["reading_score"] >= 70].groupby("spending")["Student ID"].count()/by_spending["Student ID"].count() *100
overall = (pass_math + pass_read)/2

scores_by_spend = pd.DataFrame({"Average Math Score": avg_math,
                                "Average Reading Score": avg_read,
                                "% Passing Math": pass_math,
                                "% Passing Reading": pass_read,
                                "Overall Passing Rate": overall})
scores_by_spend





# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Combine the data into a single dataset
school_data_complete["school"] = pd.cut(school_data_complete["size"], size_bins, labels = group_names)

#group by size
by_size = school_data_complete.groupby("school")

#calculations
avg_math = by_size["math_score"].mean()
avg_read = by_size["reading_score"].mean()
pass_math = school_data_complete[school_data_complete["math_score"] >= 70].groupby("school")["Student ID"].count()/by_size["Student ID"].count() *100
pass_read = school_data_complete[school_data_complete["reading_score"] >= 70].groupby("school")["Student ID"].count()/by_size["Student ID"].count() *100
overall = (pass_math + pass_read)/2

scores_by_size = pd.DataFrame({"Average Math Score": avg_math,
                               "Average Reading Score": avg_read,
                               "% Passing Math": pass_math,
                               "% Passing Reading": pass_read,
                               "Overall Passing Rate": overall})
scores_by_size





#group by size
by_type = school_data_complete.groupby("type")

#calculations
avg_math = by_type["math_score"].mean()
avg_read = by_type["reading_score"].mean()
pass_math = school_data_complete[school_data_complete["math_score"] >= 70].groupby("type")["Student ID"].count()/by_type["Student ID"].count() *100
pass_read = school_data_complete[school_data_complete["reading_score"] >= 70].groupby("type")["Student ID"].count()/by_type["Student ID"].count() *100
overall = (pass_math + pass_read)/2

scores_by_type = pd.DataFrame({"Average Math Score": avg_math,
                               "Average Reading Score": avg_read,
                               "% Passing Math": pass_math,
                               "% Passing Reading": pass_read,
                               "Overall Passing Rate": overall})
scores_by_type