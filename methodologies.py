import json
import os

def enterprise():
    try:
        with open('./enterprise-attack.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: 'enterprise-attack.json' not found in the current directory.")
        return None

def mobile():
    try:
        with open('./mobile-attack.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: 'mobile-attack.json' not found in the current directory.")
        return None

def ics():
    try:
        with open('./ics-attack.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: 'ics-attack.json' not found in the current directory.")
        return None

def methodology():
    print("This program focuses on cyber attack techniques based on the MITRE ATT&CK framework.")
    print("This program supports 3 categories of attack datasets.")
    
    choice = input("Specify the Category (Enterprise, Mobile, or ICS): ").lower().strip()
    
    if choice == "enterprise":
        data = enterprise()
    elif choice == "mobile":
        data = mobile()
    elif choice == "ics":
        data = ics()
    else:
        print("Invalid choice.")
        return

    if data is None:
        print("No data loaded. Exiting.")
        return
    technique_names = set()
    for obj in data.get('objects', []):
        if obj['type'] == 'attack-pattern':
            name = obj.get('name', '').strip()
            if name:
                technique_names.add(name)

    print("\nAvailable Techniques:")
    sorted_techniques = sorted(list(technique_names))
    for i, name in enumerate(sorted_techniques, 1):
        print(f"{i:3}. {name}")

    # Step 1: Ask for search term
        # Allow search by number or text
    search_term = input("\nEnter a technique number or part of a tactic/technique name (blank = show all): ").strip()

    # If input is a number, try to map to a specific technique name
    if search_term.isdigit():
        selected_index = int(search_term) - 1
        if 0 <= selected_index < len(sorted_techniques):
            search_term = sorted_techniques[selected_index].lower()
            print(f"🔍 Searching for: {search_term}")
        else:
            print("Invalid technique number. Showing all.")
            search_term = ""
    else:
        search_term = search_term.lower()

    # Step 2: Map tactic IDs to names
    tactic_lookup = {}
    for obj in data.get('objects', []):
        if obj['type'] == 'x-mitre-tactic':
            tactic_lookup[obj['external_references'][0]['external_id']] = obj['name']

    # Step 3: Group techniques by tactic
    tactic_technique_map = {}
    for obj in data.get('objects', []):
        if obj['type'] == 'attack-pattern' and 'kill_chain_phases' in obj:
            for phase in obj['kill_chain_phases']:
                tactic_name = phase['phase_name']
                tactic_technique_map.setdefault(tactic_name, []).append(obj)

    # Step 4: Filter and print results
    matches_found = False
    for tactic, techniques in sorted(tactic_technique_map.items()):
        tactic_display = tactic_lookup.get(tactic, tactic)
        if search_term and not any(search_term in tech.get('name', '').lower() or search_term in tech.get('description', '').lower()for tech in techniques):
            

            # Skip tactics that don't match the search
            continue

        filtered_techniques = []
        for tech in techniques:
            name = tech.get('name', '').lower()
            desc = tech.get('description', '').lower()
            if (not search_term) or (search_term in name or search_term in desc):
                filtered_techniques.append(tech)

        if filtered_techniques:
            matches_found = True
            print(f"\n=== Tactic: {tactic_display.upper()} ===")
            for tech in filtered_techniques:
                name = tech.get('name')
                desc = tech.get('description', 'No description available.').replace('\n', ' ').strip()

                external_id = ""
                for ref in tech.get("external_references", []):
                    if "external_id" in ref:
                        external_id = ref["external_id"]
                        break
                print(f"→ [{external_id}] {name}\n   {desc.strip().replace('\\n', ' ')}\n")

    if not matches_found:
        print("No techniques found matching your search.")
    
if __name__ == "__main__":
    while True:
        methodology()
        choice=input("Continue? (Y/N)")
        if "n" in choice.lower():
            break
