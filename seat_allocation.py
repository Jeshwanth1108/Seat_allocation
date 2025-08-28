import pandas as pd

# Load data
students_df = pd.read_csv("student_details.csv")
preferences_df = pd.read_csv("preference_data.csv")
institutions_df = pd.read_csv("institution_data.csv")

# Sort students by Rank (lowest to highest)
students_df = students_df.sort_values('Rank')

# Track allocations
allocations = []

# Columns relevant for caste seat allocation
caste_columns = ['SC', 'SC-CC', 'ST', 'BC', 'Minority', 'OC']

# Make a mutable copy of available seats per college
college_seats = institutions_df.set_index('CollegeID').copy()

# Go through each student in rank order
for idx, student in students_df.iterrows():
    unique_id = student['UniqueID']
    gender = student['Gender']
    caste = student['Caste']
    
    # Get the preferences for this student, ordered by preference number
    prefs = preferences_df[preferences_df['UniqueID'] == unique_id].sort_values('PrefNumber')
    seat_allocated = False
    
    for _, pref in prefs.iterrows():
        college_id = int(pref['CollegeID'])
        pref_no = int(pref['PrefNumber'])
        
        if college_id not in college_seats.index:
            continue  # college not in seat matrix
        
        row = college_seats.loc[college_id]
        
        caste_col = caste if caste in caste_columns else None
        if not caste_col:
            continue  # Unsupported caste
        
        if row[caste_col] > 0:
            # Allocate seat
            college_seats.at[college_id, caste_col] -= 1
            college_seats.at[college_id, 'TOTAL No. of students admitted'] += 1
            
            allocations.append({
                "UniqueID": unique_id,
                "CollegeID": college_id,
                "PrefNumber": pref_no,
                "Gender": gender,
                "Caste": caste,
            })
            seat_allocated = True
            break
    
    if not seat_allocated:
        allocations.append({
            "UniqueID": unique_id,
            "CollegeID": 0,    # 0 means no college allocated
            "PrefNumber": 0,   # 0 means no preference allocated
            "Gender": gender,
            "Caste": caste,
        })

# Convert allocations to DataFrame
alloc_df = pd.DataFrame(allocations, columns=["UniqueID", "CollegeID", "PrefNumber", "Gender", "Caste"])

# Ensure CollegeID and PrefNumber are integers (using Int64 nullable dtype)
alloc_df = alloc_df.astype({"CollegeID": "Int64", "PrefNumber": "Int64"})

# Save to CSV
alloc_df.to_csv("seat_allotment_results.csv", index=False)

print("Allocation process completed. Results saved to 'seat_allotment_results.csv'")

