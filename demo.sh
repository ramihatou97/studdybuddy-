#!/bin/bash
# Demo script for StudyBuddy
# Shows all the features in action

echo "========================================"
echo "  StudyBuddy Demo - Neurosurgical Study"
echo "========================================"
echo ""

export PYTHONPATH="/home/runner/work/studybuddy-/studybuddy-"
CLI="python3 /home/runner/work/studybuddy-/studybuddy-/cli/main.py"

echo "1. Creating study notes..."
$CLI notes add "Cerebral Aneurysm" "Most common location is anterior communicating artery (AComA), followed by posterior communicating artery (PComA)" --tags "vascular,aneurysm"
$CLI notes add "Brain Tumors" "Glioblastoma is the most common primary malignant brain tumor in adults. Median survival 12-15 months." --tags "oncology,tumors"
$CLI notes add "CSF Dynamics" "CSF produced by choroid plexus at 20-25 ml/hour. Total volume ~150ml. Reabsorbed by arachnoid granulations." --tags "physiology,csf"

echo ""
echo "2. Creating flashcards for spaced repetition..."
$CLI flashcards add "Name the layers of the scalp (SCALP mnemonic)" "Skin, Connective tissue, Aponeurosis, Loose connective tissue, Periosteum" --topic "Anatomy"
$CLI flashcards add "What is Cushing's triad?" "Hypertension, bradycardia, and irregular respiration - signs of increased ICP" --topic "Physiology"
$CLI flashcards add "Most common cause of subarachnoid hemorrhage?" "Ruptured cerebral aneurysm (85% of cases)" --topic "Pathology"

echo ""
echo "3. Listing all notes..."
$CLI notes list

echo ""
echo "4. Searching for 'aneurysm'..."
$CLI search "aneurysm"

echo ""
echo "5. Checking flashcard statistics..."
$CLI flashcards stats

echo ""
echo "6. Showing study statistics..."
$CLI study stats --days 7

echo ""
echo "========================================"
echo "  Demo Complete!"
echo "========================================"
echo ""
echo "Try these commands yourself:"
echo "  - Review flashcards: python3 cli/main.py flashcards review"
echo "  - Search all content: python3 cli/main.py search 'your query'"
echo "  - Add your own notes: python3 cli/main.py notes add 'Topic' 'Content'"
echo ""
