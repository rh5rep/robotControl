import random

# Create a list of soccer trivia questions and answers
questions = [
    ("Who has won the most FIFA World Cups?", "Brazil"),
    ("Which country hosted the first ever World Cup?", "Uruguay"),
    ("Who is the all-time top scorer in the World Cup?", "Miroslav Klose"),
    ("Which team won the first ever European Championship?", "Spain"),
    ("Who has won the most UEFA Champions League titles?", "Real Madrid"),
    ("Who is the all-time top scorer in the English Premier League?", "Alan Shearer"),
    ("Who has won the most Ballon d'Or awards?", "Lionel Messi"),
    ("Which team has won the most Copa America titles?", "Argentina")
]

# Shuffle the questions
random.shuffle(questions)

# Start the game
score = 0
for question, answer in questions:
    # Print the question and ask for the answer
    user_answer = input(f"{question}: ")
    if user_answer.lower() == answer.lower():
        print("Correct!\n")
        score += 1
    else:
        print(f"Incorrect! The correct answer was: {answer}\n")

# Print the final score
print(f"You scored {score} points out of {len(questions)}.")