
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[140]:


from matplotlib import pyplot as plt 
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[141]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[288]:


species.head()


# In[369]:


dup_list = species[species['scientific_name'].duplicated()]
dup_list.head()


# In[386]:


dup_list_full = pd.merge(dup_list, species, on = 'scientific_name', how = 'left')
dup_list_full = dup_list_full[['category_x', 'scientific_name', 'common_names_y', 'conservation_status_y']]
dup_list_full.columns = ['category', 'scientific_name', 'common_names', 'conservation_status']
dup_list_full.head()


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[143]:


species.scientific_name.nunique()


# In[144]:


species.shape


# In[145]:


species.category.unique()


# What are the different values of `category` in `species`?

# In[241]:


species.category.value_counts()


# In[253]:


species.category.value_counts().plot(kind = 'bar', title = 'Species at the National Parks')
plt.savefig('Species_counts.png')


# What are the different values of `conservation_status`?

# In[181]:


species.conservation_status.unique()


# In[180]:


species.conservation_status.value_counts()


# In[248]:


species.conservation_status.value_counts().plot(kind = 'bar', title = 'Conservation Status', fontsize = 14);


# In[388]:


species[species.conservation_status != 'No Protection'].conservation_status.value_counts().plot(kind = 'bar', title = 'Conservation Status'
                                                                                               , sort_columns = True);
plt.tight_layout()
plt.savefig('ConservStatus_counts.png')


# # Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[150]:


species.groupby('conservation_status').scientific_name.count()


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[151]:


species.fillna('No Protection', inplace = True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[152]:


species.groupby('conservation_status').scientific_name.count()


# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[153]:


protection_counts = species.groupby('conservation_status')    .scientific_name.count().reset_index()    .sort_values(by='scientific_name')
protection_counts.head()


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[182]:


plt.figure(figsize = (10,4))
ax = plt.subplot()

plt.bar(range(len(protection_counts)), protection_counts.scientific_name)

ax.set_xticks(range(len(protection_counts)))
ax.set_xticklabels(protection_counts.conservation_status.values)

plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')

plt.show()


# In[259]:


Cons_status = protection_counts[protection_counts['conservation_status'] != 'No Protection']

plt.figure(figsize = (10,4))
ax = plt.subplot()

plt.bar(range(len(Cons_status)), Cons_status.scientific_name)

ax.set_xticks(range(len(Cons_status)))
ax.set_xticklabels(Cons_status.conservation_status.values)

plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')

plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[156]:


species['is_protected'] = species['conservation_status'].apply(lambda x: True if x != "No Protection" else False)


# In[157]:


species.head()


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[158]:


category_counts = species.groupby(['category', 'is_protected']).scientific_name.count().reset_index()


# Examine `category_count` using `head()`.

# In[159]:


category_counts.head()


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[160]:


category_pivot = category_counts.pivot(columns = 'is_protected', index = 'category', values = 'scientific_name').reset_index()


# Examine `category_pivot`.

# In[161]:


category_pivot.head()


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[162]:


category_pivot.columns = ['category', 'not_protected', 'protected']
category_pivot.head()


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[163]:


category_pivot['percent_protected'] = category_pivot['protected'] / (category_pivot['protected'] + category_pivot['not_protected'])


# Examine `category_pivot`.

# In[316]:


print category_pivot


# In[352]:



plt.bar(range(len(category_pivot['category'])), category_pivot['percent_protected'].sort_values(ascending = False),
       color = ('C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7'))
ax1 = plt.subplot()
ax1.set_xticks(range(len(category_pivot.category)))

ax1.set_xticklabels(category_pivot.sort_values('percent_protected', ascending = False).category.values
, rotation =45)

plt.tight_layout()
plt.savefig('percentages.png')
plt.show()


# In[351]:


category_pivot.sort_values('percent_protected', ascending = False).category.values


# In[304]:


list(category_pivot.category.values)


# In[292]:


table = category_pivot[['category', 'percent_protected']]
for i in table.index:
    print "{:.2%} of {}s are under protection".format(table['percent_protected'][i], table['category'][i])
    
    


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[165]:


contingency = [[176,38], [442,79]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[166]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[167]:


test = chi2_contingency(contingency)
print test[1]


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[168]:


contingency2 = [[176,38],[74,5]]


# In[169]:


test2 = chi2_contingency(contingency2)
print test2[1]


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# Testing a Chi Square test on the whole table

# In[290]:


contingency3 = [[73,7],
                [442,79],
                [116,11],
                [176,38], 
                [328,5],
                [74,5],
                [4424,46]]
test3 = chi2_contingency(contingency3)
print test3


# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[170]:


observations = pd.read_csv('observations.csv')


# In[171]:


observations.head()


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[172]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[173]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[174]:


species['is_sheep'] = species['common_names'].apply(lambda x: True if 'Sheep' in x else False)


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[197]:


sheep = species[species['is_sheep'] == True].reset_index(drop=True)
print sheep


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[198]:


sheep_species = sheep[sheep['category'] == 'Mammal'].reset_index(drop=True)
print sheep_species


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[199]:


sheep_observations = pd.merge(sheep_species, observations)

print sheep_observations


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[214]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
print obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[215]:


plt.figure(figsize = (16,4))
ax = plt.subplot()

plt.bar(range(len(obs_by_park.observations)), obs_by_park.observations)

ax.set_xticks(range(len(obs_by_park.park_name)))
ax.set_xticklabels(list(obs_by_park.park_name))

plt.ylabel("Number of Observations")
plt.title("Observations of Sheep per Week")

plt.show()


# I want to get a more detailed picture of sheep observation. I will make a stacked bar chart that shows the observation at each park of the three different kinds of sheep. 

# In[401]:


obs_sheep = sheep_observations[['scientific_name', 'park_name', 'observations']]
obs_sheep_pivot = obs_sheep.pivot(columns = 'park_name', index = 'scientific_name', values = 'observations')
obs_sheep_pivot.head()


# In[409]:


obs_sheep_pivot.plot(kind = 'bar', stacked = True, figsize = (10,10), title = "Sheep observation by Park", fontsize = 14)
plt.tight_layout()
plt.xlabel('Scientific Name')
plt.savefig('Sheep_obs.png')


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[218]:


Baseline = .15
Min_Detec_Effect= 100.0 * (.05/.15)
print Min_Detec_Effect
sample_size = 510


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[231]:


wks_Bryce = sample_size/obs_by_park.iloc[0,1]
print "You would need {} weeks to observe enough sheep for an A/B experiment at Bryce National Park".format(wks_Bryce)


# In[229]:


wks_Yellowstone = sample_size/obs_by_park.iloc[2,1]
print "You would need {} week to observe enough sheep for an A/B experiment at Yellowstone National Park".format(wks_Yellowstone)

