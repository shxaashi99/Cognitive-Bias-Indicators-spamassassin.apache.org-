import os
import tarfile
import pandas as pd
import email

def extract_and_load():
    data = []
    # Define directories based on your file list
    # Note: Manually extract your .tar.bz2 files into folders first
    folders = ['easy_ham', 'hard_ham', 'spam']
    
    for label_type in folders:
        # Assuming you extracted the .tar.bz2 into folders named exactly like this
        path = os.path.join(os.getcwd(), label_type)
        if not os.path.exists(path): continue
            
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            with open(file_path, 'r', encoding='latin-1') as f:
                msg = email.message_from_file(f)
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode('latin-1', errors='ignore')
                else:
                    body = msg.get_payload(decode=True).decode('latin-1', errors='ignore')
                
                data.append({'text': body, 'label': 1 if label_type == 'spam' else 0})
    
    return pd.DataFrame(data)

# Run the loader
df = extract_and_load()
print(f"Loaded {len(df)} emails.")
# Now you can run the 'run_full_study(df)' function from the previous step