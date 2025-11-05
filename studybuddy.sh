#!/bin/bash
# StudyBuddy launcher script

# Set the Python path to include the studybuddy directory
export PYTHONPATH="/home/runner/work/studdybuddy-/studdybuddy-:$PYTHONPATH"

# Run the CLI with all arguments
python3 /home/runner/work/studdybuddy-/studdybuddy-/cli/main.py "$@"
