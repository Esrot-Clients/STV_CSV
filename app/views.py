from django.shortcuts import render

from collections import defaultdict
import csv
from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.contrib import messages
from .models import *

# Create your views here.
# ! To show all the Running Campaign
def campaign_list(request):
    campaigns = Campaign.objects.filter(is_active=True)
    return render(request, 'campaign_list.html', {'campaigns': campaigns})


# ! To get preference from voters
def add_vote(request, campaign_name_id):
    campaign = get_object_or_404(Campaign, pk=campaign_name_id)  # Retrieve the campaign by its ID
    
    # Get the list of candidate names for the selected campaign
    candidate_names = campaign.candidates.split(',')  # Assuming candidates are stored as a comma-separated string

    if request.method == 'POST':
        preferences = request.POST.get('preferences')  # Get the preferences as a comma-separated string
        
        # Split the preferences into a list
        preferences_list = preferences.split(', ')

        # Create a new Vote instance and save it to the database with the associated campaign
        vote = Vote.objects.create(
            campaign_name=campaign,
            preference=', '.join(preferences_list),  # Save preferences as a single comma-separated string
        )
        # Show a success message
        messages.success(request, 'Vote submitted successfully.')
        return render(request, 'add_vote.html', {'campaign': campaign, 'candidate_names': candidate_names, 'messages': messages})

    return render(request, 'add_vote.html', {'campaign': campaign, 'candidate_names': candidate_names})



# def calculate_binomial_stv_winner(num_candidates, num_voters, num_seats, voter_choices):
#     # Initialize candidate and vote count dictionaries
#     candidate_votes = defaultdict(int)
#     candidate_exclusion_votes = defaultdict(int)

#     # Calculate the quota
#     quota = num_voters // (num_seats + 1)

#     # # Election count
#     # for choices in voter_choices:
#     #     for candidate in choices:
#     #         candidate_votes[candidate] += 1
    
#     # Election count
#     for choices in voter_choices:
#         for i, candidate in enumerate(choices):
#             rank_weight = 1 / (i + 1)  # Assign weight based on rank (lower rank, higher weight)
#             candidate_votes[candidate] += rank_weight

#     # Surplus transfer
#     elected_candidates = []
#     for candidate, votes in candidate_votes.items():
#         if votes > quota:
#             surplus_votes = votes - quota
#             transfer_value = surplus_votes / votes
#             elected_candidates.append(candidate)
#             for choices in voter_choices:
#                 if candidate in choices:
#                     for i, c in enumerate(choices):
#                         if c != candidate:
#                             candidate_exclusion_votes[c] += transfer_value

#     # Exclusion count without reverse
#     # while len(elected_candidates) < num_seats:
#     #     exclusion_candidate = min(candidate_exclusion_votes, key=candidate_exclusion_votes.get)
#     #     elected_candidates.append(exclusion_candidate)
#     #     del candidate_exclusion_votes[exclusion_candidate]
#     #     for choices in voter_choices:
#     #         if exclusion_candidate in choices:
#     #             next_preference = choices[choices.index(exclusion_candidate) + 1]
#     #             if next_preference not in elected_candidates:
#     #                 candidate_exclusion_votes[next_preference] += 1


#     # Exclusion count with reverse
#     while len(elected_candidates) < num_seats:
#         exclusion_candidate = min(candidate_exclusion_votes, key=candidate_exclusion_votes.get)
#         elected_candidates.append(exclusion_candidate)
#         del candidate_exclusion_votes[exclusion_candidate]
#         for choices in voter_choices:
#             if exclusion_candidate in choices:
#                 choices.reverse()  # Reverse the preferences
#                 next_preference_index = choices.index(exclusion_candidate) + 1
#                 if next_preference_index < num_seats:
#                     next_preference = choices[next_preference_index]
#                     if next_preference not in elected_candidates:
#                         candidate_exclusion_votes[next_preference] += 1
#                 choices.reverse()


#     return elected_candidates[:num_seats]

# def calculate_binomial_stv(dataset, candidates, num_seats):
#     # Count the total votes
#     total_votes = len(dataset)

#     # Initialize the election count table
#     election_count = {}
#     for candidate in candidates:
#         election_count[candidate] = 0
#     election_count['Nemo'] = 0
#     election_count['Invalid'] = 0

#     # Count the first preferences
#     for vote in dataset:
#         if vote[0] in candidates:
#             election_count[vote[0]] += 1
#         elif vote[0] == '-':
#             election_count['Nemo'] += 1
#         else:
#             election_count['Invalid'] += 1

#     # Calculate the quota
#     quota = total_votes // (num_seats + 1)

#     # Check if any candidate has reached the quota
#     elected_candidates = []
#     for candidate in candidates:
#         if election_count[candidate] >= quota:
#             elected_candidates.append(candidate)

#     # Perform surplus transfers
#     for elected_candidate in elected_candidates:
#         surplus_votes = election_count[elected_candidate] - quota
#         if surplus_votes > 0:
#             transfer_value = surplus_votes / election_count[elected_candidate]

#             # Transfer surplus votes to next preferences
#             for vote in dataset:
#                 if vote[0] == elected_candidate:
#                     for preference in vote[1:]:
#                         if preference != '-':
#                             election_count[preference] += transfer_value

#     # Perform exclusion counts
#     exclusion_count = {}
#     for candidate in candidates:
#         exclusion_count[candidate] = 0

#     for vote in dataset:
#         for i, preference in enumerate(vote[::-1]):
#             if preference in candidates:
#                 exclusion_count[preference] += 1 / (i + 1)

#     # Calculate the quotient
#     quotient = {}
#     for candidate in candidates:
#         if election_count[candidate] != 0:  # Check if the candidate received any votes
#             quotient[candidate] = exclusion_count[candidate] / election_count[candidate]
#         else:
#             quotient[candidate] = float('inf')  # Set quotient as infinity for candidates with no votes

#     # Sort candidates by quotient in ascending order
#     sorted_candidates = sorted(quotient, key=quotient.get)

#     # Determine the elected candidates based on quotient
#     elected_candidates = sorted_candidates[:num_seats]

#     return elected_candidates

#def calculate_binomial_stv(dataset, candidates, num_seats):
#     # Count the total votes
#     total_votes = len(dataset)

#     # Initialize the election count table
#     election_count = {}
#     for candidate in candidates:
#         election_count[candidate] = 0
#     election_count['Nemo'] = 0
#     election_count['Invalid'] = 0

#     # Count the first preferences
#     for vote in dataset:
#         if vote[0] in candidates:
#             election_count[vote[0]] += 1
#         elif vote[0] == '-':
#             election_count['Nemo'] += 1
#         else:
#             election_count['Invalid'] += 1

#     # Calculate the quota
#     quota = total_votes // (num_seats + 1)

#     # Check if any candidate has reached the quota
#     elected_candidates = []
#     for candidate in candidates:
#         if election_count[candidate] >= quota:
#             elected_candidates.append(candidate)

#     # Perform surplus transfers
#     while len(elected_candidates) < num_seats:
#         exclusion_count = {}
#         for candidate in candidates:
#             exclusion_count[candidate] = 0

#         for vote in dataset:
#             for i, preference in enumerate(vote[::-1]):
#                 if preference in candidates:
#                     exclusion_count[preference] += 1 / (i + 1)

#         highest_exclusion_count = max(exclusion_count.values())

#         # Find the candidate with the highest exclusion count
#         for candidate, count in exclusion_count.items():
#             if count == highest_exclusion_count:
#                 highest_exclusion_candidate = candidate
#                 break

#         next_highest_candidate = None
#         for candidate in candidates:
#             if candidate not in elected_candidates:
#                 if next_highest_candidate is None or election_count[candidate] > election_count[next_highest_candidate]:
#                     next_highest_candidate = candidate

#         surplus_votes = election_count[highest_exclusion_candidate] - quota
#         if surplus_votes > 0:
#             transfer_value = surplus_votes / election_count[highest_exclusion_candidate]

#             # Transfer surplus votes to next preferences
#             for vote in dataset:
#                 if vote[0] == highest_exclusion_candidate:
#                     for preference in vote[1:]:
#                         if preference != '-' and preference == next_highest_candidate:
#                             election_count[preference] += transfer_value

#         elected_candidates.append(next_highest_candidate)

#     # Check if elected_candidates reached num_seats
#     if len(elected_candidates) > num_seats:
#         elected_candidates = elected_candidates[:num_seats]

#     # Calculate the quotient
#     quotient = {}
#     for candidate in candidates:
#         if election_count[candidate] != 0:  # Check if the candidate received any votes
#             quotient[candidate] = exclusion_count[candidate] / election_count[candidate]
#         else:
#             quotient[candidate] = float('inf')  # Set quotient as infinity for candidates with no votes

#     # Sort candidates by quotient in ascending order
#     sorted_candidates = sorted(quotient, key=quotient.get)

#     # Determine the elected candidates based on quotient
#     elected_candidates = []
#     schrodingers_candidates = []
#     for candidate in sorted_candidates:
#         if candidate in elected_candidates and candidate in exclusion_count:
#             if quotient[candidate] <= 1:
#                 elected_candidates.append(candidate)
#             else:
#                 schrodingers_candidates.append(candidate)
#         else:
#             elected_candidates.append(candidate)

#     # Sort Schrödinger's candidates by quotient in ascending order
#     schrodingers_candidates = sorted(schrodingers_candidates, key=lambda x: quotient[x])

#     # Determine the final elected candidates by considering Schrödinger's candidates
#     final_elected_candidates = elected_candidates[:num_seats]
#     if len(final_elected_candidates) < num_seats:
#         num_remaining_seats = num_seats - len(final_elected_candidates)
#         final_elected_candidates += schrodingers_candidates[:num_remaining_seats]

#     return final_elected_candidates


# ! Updated code to calculate Binomial STV
def calculate_binomial_stv(dataset, candidates, num_seats):

    filtered_dataset = []
    duplicate_dataset = []

    for data_point in dataset:
        # Condition 1: No. of data points in a data point should be less than or equal to the no. of candidates
        if len(data_point) <= len(candidates):
            # Condition 2: Check for duplicate candidate names in a data point
            candidate_counts = {}
            duplicate_flag = False
            for candidate in data_point:
                if candidate == '-':
                    continue  # Ignore dashes or abstention as it can be multiple
                if candidate in candidate_counts:
                    duplicate_flag = True
                    break
                else:
                    candidate_counts[candidate] = 1

            if duplicate_flag:
                duplicate_dataset.append(data_point)    # Adding duplicate data to duplicate dataset 
            else:
                filtered_dataset.append(data_point)     # Desired data 
        else:
            duplicate_dataset.append(data_point)    # Data having more choices than the total no of candidates to duplicate dataset 

    dataset = filtered_dataset      # Updating the dataset 

    # Count the total votes
    total_votes = len(dataset)

    # Calculate the quota
    quota = total_votes // (num_seats + 1)
    
    # Initialize the election count table
    election_count = {}
    for candidate in candidates:
        election_count[candidate] = 0
    election_count['Nemo'] = 0
    election_count['Invalid'] = 0

    # Count the first preferences
    for vote in dataset:
        if vote[0] in candidates:
            election_count[vote[0]] += 1
        elif vote[0] == '-':
            election_count['Nemo'] += 1
        else:
            election_count['Invalid'] += 1
    
    # Create a copy of the election_count dictionary
    election_count_copy = election_count.copy()                
            
    # Check if any candidate has reached the quota
    # Perform surplus transfers for elected candidates
    while True:
        elected_candidates = []
        for candidate in candidates:
            if election_count[candidate] >= quota:
                elected_candidates.append(candidate)

        if len(elected_candidates) >= num_seats:
            break

        for elected_candidate in elected_candidates:
            surplus_votes = election_count[elected_candidate] - quota
            if surplus_votes > 0:
                transfer_value = surplus_votes / election_count[elected_candidate]

                # Transfer surplus votes to next preferences
                for vote in dataset:
                    if vote[0] == elected_candidate:
                        for preference in vote[1:]:
                            if preference != '-' and preference in candidates:
                                election_count[preference] += transfer_value


    # Initialize the exclusion count table
    exclusion_count = {}
    for candidate in candidates:
        exclusion_count[candidate] = 0
    exclusion_count['Nemo'] = 0
    exclusion_count['Invalid'] = 0

    # Count the last preferences
    #  For exclusion count     
    for vote in dataset:
        if vote[-1] in candidates:
            exclusion_count[vote[-1]] += 1
        elif vote[-1] == '-':
            exclusion_count['Nemo'] += 1
        else:
            exclusion_count['Invalid'] += 1

    # Create a copy of the exclusion_count dictionary
    exclusion_count_copy = exclusion_count.copy()   
    
    # Exclusion Count Calculation
    # Checking which candidates reach quota
#     excluded_candidates = []
#     for candidate in candidates:
#         if exclusion_count[candidate] >= quota:
#             excluded_candidates.append(candidate)
            
    # Check if any candidate has reached the quota
    # Perform surplus transfers for excluded candidates
    # Check if any candidate has reached the quota in exclusion count
    if any(exclusion_count[candidate] >= quota for candidate in candidates):
#         while True:
            excluded_candidates = []
            for candidate in candidates:
                if exclusion_count[candidate] >= quota:
                    excluded_candidates.append(candidate)

#             if not excluded_candidates:  # No more excluded candidates, exit the loop
#                 break

            for excluded_candidate in excluded_candidates:
                surplus_votes = exclusion_count[excluded_candidate] - quota
                if surplus_votes > 0:
                    transfer_value = surplus_votes / exclusion_count[excluded_candidate]

                    # Transfer surplus votes to next preferences
                    for vote in dataset:
                        if vote[-1] == excluded_candidate:
                            for preference in vote[:-1]:  # Exclude the last preference as it's the current candidate
                                if preference != '-' and preference in candidates:
                                    election_count[preference] += transfer_value
                                    
                            # Deduct the surplus votes from the exclusion count of the current candidate
                            exclusion_count[excluded_candidate] -= surplus_votes

            # Recalculate the exclusion count after the surplus transfers
            
            # Clear the exclusion count for candidates that have been excluded
            for excluded_candidate in excluded_candidates:
                exclusion_count[excluded_candidate] = 0

    # Update the list of excluded candidates based on new exclusion count
    excluded_candidates = [candidate for candidate in candidates if exclusion_count[candidate] >= quota]

    # Check if there are any common candidate between elected and excluded candidates list
    # If yes then calculate the quotient else not    
    common_candidates = list(set(elected_candidates) & set(excluded_candidates))
    
    if common_candidates:
        # Calculate the quotient
        quotient = {}
        for candidate in common_candidates:
            # Perform quotient calculation for the common candidate
            if election_count_copy[candidate] != 0:  # Check if the candidate received any votes
                quotient[candidate] = exclusion_count_copy[candidate] / election_count_copy[candidate]
            else:
                quotient[candidate] = float('inf')  # Set quotient as infinity for candidates with no votes
        
        # Sort candidates by quotient in ascending order
        sorted_candidates = sorted(quotient, key=quotient.get)
                
        # Determine the elected candidates based on quotient
        # If a candidate is present in both elected and excluded candidates list and got a quitient > 1 then we will exclude him 
        elected_candidates = []
        schrodingers_candidates = []
        for candidate in sorted_candidates:
            if candidate in elected_candidates and candidate in excluded_candidates:
                if quotient[candidate] > 1:
                    elected_candidates.remove(candidate)
        
    return elected_candidates[:num_seats]


# ! To Extract Data from CSV file
def process_csv_file(file_path):
    voter_choices = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if it exists
        for row in reader:
            voter_choices.append(row)
    return voter_choices


# ! Check result By csv upload
def check_result(request, campaign_name_id):
    campaign = get_object_or_404(Campaign, pk=campaign_name_id)  # Retrieve the campaign by its ID

    if request.method == 'POST':
        try:
            # Your existing form data processing code here

            # Handle the CSV file upload
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                # Read the CSV data and extract information
                csv_data = csv_file.read().decode('utf-8').splitlines()

                # Create an empty list to store extracted preferences
                preferences = []

                # Process the CSV data
                csv_reader = csv.DictReader(csv_data)
                for row in csv_reader:
                    # Access the "Preference" column and split it into a list
                    preference_column = row['Preference']
                    preference_list = preference_column.split(', ')
                    
                    # Append the preference list to the preferences list
                    preferences.append(preference_list)

                # Now, 'preferences' contains a list of preference lists from the CSV file
                # Remove blank spaces from each string in the list of lists and convert to lowercase
                # preferences = [[s.strip().lower() for s in sublist] for sublist in preferences]
                # exit(preferences)
            
            candidates = (campaign.candidates)
            # Remove blank spaces from candidate names and convert to lowercase
            # candidates = [candidate.strip().lower() for candidate in campaign.candidates]
            num_seats = int(campaign.num_seats)
            # voter_choices_input = preferences
            # Convert the input strings to lists
            # candidates = candidates_input.split(',')
            # voter_choices = [list(line.strip()) for line in voter_choices_input.strip().split('\n')]
            
            # Remove blank spaces from each string in the list of lists
            # preferences = [[s.strip() for s in sublist] for sublist in preferences]
            
            # Call the calculate_binomial_stv function with the correct arguments
            elected_candidates = calculate_binomial_stv(preferences, candidates, num_seats)

            context = {
                'results': elected_candidates,
                'candidates': candidates,
                'num_seats': num_seats,
                'voter_choices': preferences,
            }

            # Continue with the rest of your view logic
            return render(request, 'results.html', context)
        except Exception as e:
            print("An exception occurred:", str(e))
            import traceback
            traceback.print_exc()
            exception_message = str(e)
            return render(request, 'results.html', {'exception_message': exception_message})

    return render(request, 'check_results.html', {'campaign_name_id': campaign_name_id})


# ! The main view
# def stv_calculator(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         # Save the CSV file temporarily
#         temp_file_path = default_storage.save(csv_file.name, csv_file)
#         # Process the uploaded CSV file
#         voter_choices = process_csv_file(temp_file_path)
#         candidates = request.POST.get('candidates').split(",")
#         num_seats = int(request.POST.get('num_seats'))  # Get the number of seats from form input
#         num_candidates = len(candidates)  # Get the number of candidates
#         results = calculate_binomial_stv_winner(num_candidates, len(voter_choices), num_seats, voter_choices)
#         # Delete the temporary file
#         default_storage.delete(temp_file_path)
#         return render(request, 'results.html', {'results': results, 'voter_choices': voter_choices})
#     return render(request, 'upload.html')


def stv_calculator(request):
    # if request.method == 'POST':
    #     voter_choices = request.POST.get('voter_choices')
    #     voter_choices = [choices.split(',') for choices in voter_choices.split('\n') if choices]
    #     candidates = request.POST.get('candidates').split(",")
    #     num_seats = int(request.POST.get('num_seats'))
    #     num_candidates = len(candidates)
    #     # results = calculate_binomial_stv_winner(num_candidates, len(voter_choices), num_seats, voter_choices)
    #     results = calculate_binomial_stv(voter_choices, candidates, num_seats)
    #     return render(request, 'results.html', {'results': results, 'voter_choices': voter_choices})
    # return render(request, 'upload.html')

    if request.method == 'POST':
        candidates = list(request.POST.get('candidates'))
        num_seats = int(request.POST['num_seats'])
        voter_choices_input = request.POST.get('voter_choices')

        # Convert the input strings to lists
        # candidates = candidates_input.split(',')
        voter_choices = [list(line.strip()) for line in voter_choices_input.strip().split('\n')]

        # Call the calculate_binomial_stv function with the correct arguments
        results = calculate_binomial_stv(voter_choices, candidates, num_seats)
        return render(request, 'results.html', {'results': results, 'voter_choices': voter_choices})
    return render(request, 'upload.html')




# A, B, C, D, E, F, G, H

# D, E, F, A, B, C, G, H
# D, A, B, C, E, F, G, H
# A, D, E, F, G, H, B, C
# A, B, C, D, E, F, G, H
# E, F, G, A, B, C, D, H
# D, E, F, A, B, C, G, H
# D, A, B, C, E, F, G, H
# A, D, E, F, G, H, B, C
# A, B, E, F, G, C, D, H
# F, A, B, D, E, C, G, H
# D, A, E, F, B, C, G, H
# E, F, G, A, B, C, D, H
# D, E, F, A, B, C, G, H
# D, A, B, C, E, F, G, H
# A, D, E, F, G, H, B, C
# A, B, C, D, E, F, G, H
# E, F, G, A, B, C, D, H
# D, E, F, A, B, C, G, H
# D, A, B, C, E, F, G, H
# A, D, E, F, G, H, B, C
# A, B, E, F, G, C, D, H
# F, A, B, D, E, C, G, H
# D, A, E, F, B, C, G, H
# E, F, G, A, B, C, D, H
# D, E, F, A, B, C, G, H
# D, A, B, C, E, F, G, H
# A, D, E, F, G, H, B, C
# A, B, C, D, E, F, G, H
# E, F, G, A, B, C, D, H
# D, E, F, A, B, C, G, H
# D, A, B, C, E, F, G, H

# 'H', 'F', 'G', 'E', '-', '-', '-', '-'
# 'H', 'F', 'G', 'E', '-', '-', '-', '-'
# 'H', 'F', 'G', 'E', '-', '-', '-', '-'
# 'H', 'F', 'G', 'E', '-', '-', '-', '-'
# 'H', 'F', 'G', 'E', '-', '-', '-', '-'
# 'H', 'F', 'G', 'E', '-', '-', '-', '-'

# 'C', 'B', 'D', 'A', '-', '-', '-', '-'
# 'C', 'B', 'D', 'A', '-', '-', '-', '-'
# 'C', 'B', 'D', 'A', '-', '-', '-', '-'
# 'C', 'B', 'D', 'A', '-', '-', '-', '-'
# 'C', 'B', 'D', 'A', '-', '-', '-', '-'
# 'C', 'B', 'D', 'A', '-', '-', '-', '-'
# 'C', 'B', 'D', 'A', '-', '-', '-', '-'
# 'C', 'B', 'D', 'A', '-', '-', '-', '-'

# '-', '-', '-', '-', 'G', 'H', 'F', 'E'
# '-', '-', '-', '-', 'G', 'H', 'F', 'E'
# '-', '-', '-', '-', 'G', 'H', 'F', 'E'
# '-', '-', '-', '-', 'G', 'H', 'F', 'E'

# 'D', 'B', 'A', 'C', 'F', 'H', '-', '-'
# 'D', 'B', 'A', 'C', 'F', 'H', '-', '-'
# 'D', 'B', 'A', 'C', 'F', 'H', '-', '-'

# 'C', 'E', 'G', 'A', 'H', 'B', 'D', 'F'
# 'C', 'E', 'G', 'A', 'H', 'B', 'D', 'F'

# 'F', 'G', 'H', 'E', 'A', 'B', 'C', 'D'
# 'F', 'G', 'H', 'E', 'A', 'B', 'C', 'D'
# 'F', 'G', 'H', 'E', 'A', 'B', 'C', 'D'
# 'F', 'G', 'H', 'E', 'A', 'B', 'C', 'D'

# 'D', 'E', 'B', 'A', 'H', 'F', 'G', 'E'

# 'A', 'D', 'E', 'F', 'H', 'G', 'C', 'B'
# 'A', 'D', 'E', 'F', 'H', 'G', 'C', 'B'
# 'A', 'D', 'E', 'F', 'H', 'G', 'C', 'B'

# 'G', 'A', 'F', 'B', 'C', 'H', 'D', 'E