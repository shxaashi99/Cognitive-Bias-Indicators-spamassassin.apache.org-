import os
import pandas as pd
import email

def extract_and_load():
    data = []
    # Full set of folders from the SpamAssassin corpus
    folders = ['easy_ham', 'easy_ham_2', 'hard_ham', 'spam', 'spam_2']
    
    for label_type in folders:
        path = os.path.join(os.getcwd(), label_type)
        if not os.path.exists(path):
            print(f"Warning: Folder '{label_type}' not found, skipping.")
            continue
            
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    msg = email.message_from_file(f)
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode('latin-1', errors='ignore')
                    else:
                        body = msg.get_payload(decode=True).decode('latin-1', errors='ignore')
                    
                    # spam, spam_2 = 1; all ham folders = 0
                    label = 1 if 'spam' in label_type else 0
                    data.append({'text': body, 'label': label})
            except Exception as e:
                continue
    
    return pd.DataFrame(data)

# Run the loader
df = extract_and_load()
print(f"Loaded {len(df)} emails.")
