#!/bin/bash

# Ensure you have 7zip, base64, base32, and xxd installed
if ! command -v 7z &> /dev/null; then
    echo "7z could not be found, please install it."
    exit 1
fi

if ! command -v base64 &> /dev/null; then
    echo "base64 could not be found, please install it."
    exit 1
fi

if ! command -v base32 &> /dev/null; then
    echo "base32 could not be found, please install it."
    exit 1
fi

if ! command -v xxd &> /dev/null; then
    echo "xxd could not be found, please install it."
    exit 1
fi

# Initialize variables
input_file="chall.7z"  # The initial zip file you start with
output_dir="output"  # Directory to store extracted files

# Create output directory if it doesn't exist
mkdir -p $output_dir

# Function to decode password
decode_password() {
    local encoded_password=$1

    # Try base64 decoding
    decoded_password=$(echo "$encoded_password" | base64 --decode 2> /dev/null)
    if [ $? -eq 0 ]; then
        echo "$decoded_password"
        return
    fi

    # Try base32 decoding
    decoded_password=$(echo "$encoded_password" | base32 --decode 2> /dev/null)
    if [ $? -eq 0 ]; then
        echo "$decoded_password"
        return
    fi

    # Try hex decoding
    decoded_password=$(echo "$encoded_password" | xxd -r -p 2> /dev/null)
    if [ $? -eq 0 ]; then
        echo "$decoded_password"
        return
    fi

    # If no decoding worked, return the original encoded_password
    echo "$encoded_password"
}

# Function to extract zip file
extract_zip() {
    local zip_file=$1
    local password=$2

    if [ -z "$password" ]; then
        7z x "$zip_file" -o"$output_dir" > /dev/null 2>&1
    else
        7z x "$zip_file" -o"$output_dir" -p"$password" > /dev/null 2>&1
    fi

    if [ $? -ne 0 ]; then
        echo "Extraction failed, possibly incorrect password or corrupted zip."
        echo "Zip file: $zip_file"
        echo "Password: $password"
        exit 1
    fi
}

# Loop to extract files until we find the flag
while true; do
    # Extract the zip file
    extract_zip "$input_file" "$password"

    # Check for the flag in the extracted files
    flag_file=$(find "$output_dir" -name "flag{*.txt}")
    if [ -n "$flag_file" ]; then
        echo "Flag found: $(cat "$flag_file")"
        break
    fi

    # Find the new zip file and password file
    new_zip_file=$(find "$output_dir" -name "*.zip" -o -name "*.7z" | head -n 1)
    password_file=$(find "$output_dir" -type f -not -name "*.zip" -not -name "*.7z" | head -n 1)

    # Read the password
    encoded_password=$(cat "$password_file")

    # Decode the password
    password=$(decode_password "$encoded_password")

    # Print debug information
    echo "New zip file: $new_zip_file"
    echo "Password file: $password_file"
    echo "Encoded password: $encoded_password"
    echo "Decoded password: $password"

    # Prepare for the next iteration
    input_file="$new_zip_file"
    rm -rf "$output_dir"
    mkdir -p $output_dir
done
