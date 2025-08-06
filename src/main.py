from collections import Counter
import re
import nltk
nltk.download('words')
from nltk.corpus import words


# write your code here

def main():
    """Main function to run the program."""
    print("🛸 NASA Signal Decoder - Deciphering Messages from Planet Dyslexia 🛸")
    
    # Your code logic goes here -- feel free to add functions or classes as needed

    #NOTE: Explanation of the steps taken in the code:
    '''
    1. read data
    2. Extract all candidate segments
    3. Build translation map based on frequency
    4. Apply substitution in the candidate segments
    5. use scoring functions to rank candidates
    6. Process and rank all segments
    7. Sort candidates based on score
    8. Print the first 9 words of the top candidate
    9. Use nltk library to check against English words
    10. Use regex to find bigrams and calculate scores
    11. Calculate space density score
    12. Combine scores for final ranking
    '''

    # Load English word list
    english_words = set(words.words())

    # variables
    target_length = 721
    expected_freq_order = ['E', 'A', 'T', 'O', 'I', 'R', 'S', 'N', 'H', 'U']

    # Read the file
    with open('../signal.txt', 'r') as file:
        content = file.read()

    
    segments = [content[i:i + target_length] for i in range(len(content) - target_length + 1)]


    def build_translation_map(segment):
        filtered = segment.replace(' ', '')
        freq_order = [char for char, _ in Counter(filtered).most_common(10)]
        return {encoded: decoded for encoded, decoded in zip(freq_order, expected_freq_order)}


    def apply_substitution(segment, translation_map):
        return ''.join(translation_map.get(char, char) for char in segment)


    def word_match_score(text):
        tokens = re.findall(r'\b[A-Z]{2,}\b', text.upper())
        return sum(1 for token in tokens if token in english_words)

    common_bigrams = {'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ND', 'ON', 'EN', 'AT'}
    def bigram_score(text):
        text = text.upper().replace(' ', '')
        return sum(1 for i in range(len(text)-1) if text[i:i+2] in common_bigrams)

    def space_density_score(text):
        return text.count(' ') / len(text)

    def combined_score(text):
        return (
            word_match_score(text) * 3 +
            bigram_score(text) * 1.5 +
            space_density_score(text) * 10
        )

    ranked_candidates = []
    for segment in segments:
        translation_map = build_translation_map(segment)
        decoded = apply_substitution(segment, translation_map)
        score = combined_score(decoded)
        ranked_candidates.append((score, decoded))

    # Sort by score
    ranked_candidates.sort(reverse=True)

    # Show first 9 words of the top candidate
    print('First 9 words: ',ranked_candidates[0][1].split(' ')[:9])
print("Searching for 721-character encrypted message...")


if __name__ == "__main__":
    main() 
