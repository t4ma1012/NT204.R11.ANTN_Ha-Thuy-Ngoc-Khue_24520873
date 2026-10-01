import os

def create_directory_structure():
    # Define the folder hierarchy relative to the current working directory
    structure = {
        "TEST/decoder": [
            "http_url",
            "html_entity",
            "smtp_mime",
            "invalid_bytes"
        ],
        "TEST/preprocessor": [
            "normalization",
            "missing_field"
        ],
        "TEST/flow": [
            "tcp_handshake",
            "bidirectional",
            "tcp_close",
            "udp",
            "concurrent",
            "timeout",
            "statistics",
            "malformed"
        ]
    }

    print("Starting directory creation inside IDS-Project...")
    
    for base_path, subdirs in structure.items():
        for subdir in subdirs:
            dir_path = os.path.join(base_path, subdir)
            # Create directories recursively; ignore if they already exist
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created: {dir_path}")

    print("\nSuccessfully created all test folders!")

if __name__ == "__main__":
    create_directory_structure()