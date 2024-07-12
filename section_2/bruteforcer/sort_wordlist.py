# Open the input file and read the contents
with open('wordlist.txt', 'r') as file:
    words = file.readlines()

# Remove any leading/trailing whitespace characters from each line
words = [word.strip() for word in words]

# Sort the list of words lexicographically
sorted_words = sorted(words)

# Open the output file and write the sorted words
with open('sorted_wordlist.txt', 'w') as file:
    for word in sorted_words:
        file.write(word + '\n')

print("The words have been sorted and written to 'sorted_wordlist.txt'.")
