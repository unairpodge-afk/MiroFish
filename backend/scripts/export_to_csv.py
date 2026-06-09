import os
import json
import csv
import sys

def export_jsonl_to_csv(jsonl_path, csv_path):
    if not os.path.exists(jsonl_path):
        print(f"File not found: {jsonl_path}")
        return False
        
    print(f"Reading {jsonl_path}...")
    
    # We will collect all fields dynamically
    all_rows = []
    field_names = set()
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                
                # Flatten the 'action_args' dictionary if it exists
                if 'action_args' in data and isinstance(data['action_args'], dict):
                    args = data.pop('action_args')
                    for k, v in args.items():
                        data[f"arg_{k}"] = v
                        
                # Keep track of all fields
                for k in data.keys():
                    field_names.add(k)
                    
                all_rows.append(data)
            except json.JSONDecodeError:
                pass
                
    if not all_rows:
        print("No valid data found.")
        return False
        
    # Sort fields for consistent output: standard fields first, then args
    standard_fields = ['round', 'timestamp', 'agent_id', 'agent_name', 'action_type', 'event_type', 'platform', 'success']
    sorted_fields = []
    
    for f in standard_fields:
        if f in field_names:
            sorted_fields.append(f)
            field_names.remove(f)
            
    sorted_fields.extend(sorted(list(field_names)))
    
    print(f"Writing {len(all_rows)} rows to {csv_path}...")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=sorted_fields)
        writer.writeheader()
        for row in all_rows:
            # ensure all dict keys are present to avoid KeyError
            cleaned_row = {k: row.get(k, "") for k in sorted_fields}
            writer.writerow(cleaned_row)
            
    print(f"Successfully exported to {csv_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_to_csv.py <simulation_id>")
        sys.exit(1)
        
    sim_id = sys.argv[1]
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads', 'simulations', sim_id))
    
    if not os.path.exists(base_dir):
        print(f"Simulation directory not found: {base_dir}")
        sys.exit(1)
        
    twitter_log = os.path.join(base_dir, "twitter", "actions.jsonl")
    reddit_log = os.path.join(base_dir, "reddit", "actions.jsonl")
    
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads', 'exports'))
    os.makedirs(out_dir, exist_ok=True)
    
    twitter_out = os.path.join(out_dir, f"{sim_id}_twitter.csv")
    reddit_out = os.path.join(out_dir, f"{sim_id}_reddit.csv")
    
    export_jsonl_to_csv(twitter_log, twitter_out)
    export_jsonl_to_csv(reddit_log, reddit_out)
