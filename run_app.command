#!/bin/bash
cd "$(dirname "$0")"

if ! command -v streamlit &> /dev/null
then
    echo "Streamlit not found. Checking for pip..."
    if ! command -v pip &> /dev/null
    then
        echo
        echo "ERROR: pip is not installed. Please install Python and pip first."
        exit 1
    fi
    echo "Installing requirements..."
    pip install -r requirements.txt
fi

echo "Launching the Dataset Comparison App..."
# Start Streamlit in the background
streamlit run dataset_comparison_app.py &
STREAMLIT_PID=$!

echo
echo "Type exit and press Enter to close the app, or just close this window."
while true; do
    read -r input
    if [[ "$input" == "exit" ]]; then
        echo "Shutting down Streamlit..."
        kill $STREAMLIT_PID
        break
    fi
done