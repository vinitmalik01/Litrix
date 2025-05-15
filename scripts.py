
def call_schedule_task():
    print("\n🔧 Let's schedule a recurring task step-by-step!")

    # 1. Ask for the command to run
    command = input("\n📌 What command should be run? (e.g., `python3 script.py`): ").strip()
    if not command:
        print("❌ You must enter a command.")
        return

    # 2. Ask how often to repeat
    print("\n⏱️ How often should this task repeat?")
    print("   1 → Every N minutes")
    print("   2 → Every N hours")
    print("   3 → Every day at a specific time")
    print("   4 → Every week on a specific day and time")
    print("   5 → Every month on a specific date and time")
    print("   6 → Custom cron format (advanced users)")
    
    choice = input("👉 Enter the number of your choice (1-6): ").strip()

    cron = None

    if choice == "1":
        minutes = input("🔁 Repeat every how many minutes? (e.g., 15): ").strip()
        if not minutes.isdigit() or int(minutes) < 1 or int(minutes) > 59:
            print("❌ Invalid minute value.")
            return
        cron = f"*/{minutes} * * * *"

    elif choice == "2":
        hours = input("🔁 Repeat every how many hours? (e.g., 3): ").strip()
        if not hours.isdigit() or int(hours) < 1 or int(hours) > 23:
            print("❌ Invalid hour value.")
            return
        cron = f"0 */{hours} * * *"

    elif choice == "3":
        time = input("🕒 At what time each day? (24-hour format, e.g., 09:30): ").strip()
        try:
            hour, minute = map(int, time.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
            cron = f"{minute} {hour} * * *"
        except:
            print("❌ Invalid time format.")
            return

    elif choice == "4":
        days = {
            "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "0"
        }
        print("\n📅 Choose a day:")
        print("   1 → Monday")
        print("   2 → Tuesday")
        print("   3 → Wednesday")
        print("   4 → Thursday")
        print("   5 → Friday")
        print("   6 → Saturday")
        print("   7 → Sunday")
        day_choice = input("📌 Day (1-7): ").strip()
        time = input("🕒 At what time? (24-hour format, e.g., 14:00): ").strip()
        try:
            hour, minute = map(int, time.split(":"))
            if day_choice not in days or not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
            cron = f"{minute} {hour} * * {days[day_choice]}"
        except:
            print("❌ Invalid input.")
            return

    elif choice == "5":
        day = input("📆 On which day of the month? (1-31): ").strip()
        time = input("🕒 At what time? (24-hour format, e.g., 08:00): ").strip()
        try:
            day = int(day)
            hour, minute = map(int, time.split(":"))
            if not (1 <= day <= 31 and 0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
            cron = f"{minute} {hour} {day} * *"
        except:
            print("❌ Invalid input.")
            return

    elif choice == "6":
        cron = input("🛠️ Enter custom cron expression (e.g., `30 14 * * 1-5`): ").strip()
    else:
        print("❌ Invalid option.")
        return

    cron_line = f"{cron} {command}"
    print(f"\n📋 Your scheduled task will be:\n{cron_line}")

    confirm = input("✅ Save this task? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Task not saved.")
        return

    try:
        os.system("crontab -l > mycron_temp 2>/dev/null")
        with open("mycron_temp", "a") as file:
            file.write(f"\n{cron_line}\n")
        os.system("crontab mycron_temp")
        os.remove("mycron_temp")
        print("✅ Task scheduled successfully!")
    except Exception as e:
        print(f"❌ Failed to schedule task: {e}")

def call_nmap_automation():
    print("\n🛰️  Nmap Automation Suite")
    print("-" * 60)
    print("This tool helps you automate Nmap scans with ease.\n")

    # Step 1: Get the target
    target = input("🔹 Enter target IP/domain: ").strip()
    if not target:
        print("❌ Target cannot be empty.")
        return

    # Step 2: Scan Presets
    print("\n📦 Choose a scan profile:")
    print("1. Quick scan            => -T4 -F             (Fast scan, common ports only)")
    print("2. Service/version scan  => -sV                (Detect service versions)")
    print("3. OS detection          => -O                 (Try to identify OS)")
    print("4. Full TCP scan         => -p-                (All 65535 ports)")
    print("5. Aggressive scan       => -A                 (All info: OS, versions, scripts)")
    print("6. Stealth scan (SYN)    => -sS                (Avoids logging)")
    print("7. Custom flags          => You choose flags manually")
    scan_choice = input("🔹 Your choice (1-7): ").strip()

    # Step 3: Define flags
    flag_options = {
        "1": "-T4 -F",
        "2": "-sV",
        "3": "-O",
        "4": "-p-",
        "5": "-A",
        "6": "-sS"
    }

    if scan_choice in flag_options:
        scan_flags = flag_options[scan_choice]
    elif scan_choice == "7":
        scan_flags = input("🔹 Enter your custom Nmap flags: ").strip()
        if not scan_flags:
            print("❌ Custom flags cannot be empty.")
            return
    else:
        print("❌ Invalid choice.")
        return

    print("\n🚀 Executing:")
    print(f"nmap {scan_flags} {target}")
    print("-" * 60)

    try:
        # Run and capture output
        result = subprocess.run(
            ["nmap"] + scan_flags.split() + [target],
            capture_output=True, text=True, check=True
        )
        
        # Beautify output
        print("\n📄 Scan Results:")
        print("=" * 60)
        for line in result.stdout.splitlines():
            if "Nmap scan report" in line or "PORT" in line:
                print(f"\033[96m{line}\033[0m")  # Cyan highlight
            elif "open" in line:
                print(f"\033[92m{line}\033[0m")  # Green highlight
            elif "closed" in line or "filtered" in line:
                print(f"\033[91m{line}\033[0m")  # Red highlight
            else:
                print(line)
        print("=" * 60)
        print("✅ Scan complete.")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Nmap failed:\n{e}")




def call_ffuf_automation():
    print("\n🔐 FFUF Advanced Automation Tool")
    print("-" * 60)
    print("This tool helps you automate fuzzing with FFUF (Fuzz Faster U Fool)")
    print("Common use: directory brute-forcing, file discovery, header fuzzing, etc.")
    print("-" * 60)

    # 🚀 Required inputs
    url = input("🔹 Enter target URL (use 'FUZZ' as placeholder): ").strip()
    if "FUZZ" not in url:
        print("❌ Error: You must include 'FUZZ' in the URL to indicate fuzzing position.")
        return

    wordlist = input("📂 Enter path to wordlist: ").strip()
    if not wordlist:
        print("❌ Error: Wordlist path is required.")
        return

    # 🔧 Optional customizations
    extensions = input("📎 File extensions (comma-separated, e.g. php,html) or leave blank: ").strip()
    status_codes = input("📄 Match status codes (e.g. 200,204,301) or leave blank: ").strip()
    threads = input("⚙️  Number of threads (default 40): ").strip() or "40"
    delay = input("⏱️  Delay between requests in ms (optional): ").strip()
    timeout = input("⏳ Request timeout in seconds (optional): ").strip()
    follow_redirects = input("🔁 Follow redirects? (y/n, default n): ").lower() == 'y'
    headers = input("🧾 Add headers (e.g. 'Host: example.com\\nUser-Agent: fuzz'): ").strip()

    # 🛡️ Filtering
    filter_size = input("🔎 Filter by size (e.g. 0,4242) or leave blank: ").strip()
    filter_word = input("🪄 Filter by word count (e.g. 0,15): ").strip()
    filter_line = input("📐 Filter by line count (e.g. 0,30): ").strip()

    # 🌍 Build full ffuf command dynamically
    cmd = [
        "ffuf",
        "-u", url,
        "-w", wordlist,
        "-t", threads
    ]

    if extensions:
        cmd += ["-e", extensions]
    if status_codes:
        cmd += ["-mc", status_codes]
    if delay:
        cmd += ["-p", delay]
    if timeout:
        cmd += ["-timeout", timeout]
    if follow_redirects:
        cmd.append("-r")
    if headers:
        for h in headers.split("\\n"):
            cmd += ["-H:", h]
    if filter_size:
        cmd += ["-fs", filter_size]
    if filter_word:
        cmd += ["-fw", filter_word]
    if filter_line:
        cmd += ["-fl", filter_line]

    # 🖥️ Show command
    print("\n🚀 Running FFUF with command:")
    print(" ".join(cmd))
    print("-" * 60)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout

        print("\n📄 FFUF Results (highlighting matches):")
        print("=" * 60)
        for line in output.splitlines():
            if "Status:" in line and "Size:" in line:
                print(f"\033[92m{line}\033[0m")
            elif "[INFO]" in line:
                print(f"\033[96m{line}\033[0m")
            else:
                print(line)
        print("=" * 60)
        print("✅ Done!")

    except subprocess.CalledProcessError as e:
        print("❌ FFUF execution failed.")
        print(e.stderr)
def call_summary_module():
    print("• Summarize results from a tool output using AI.")
    data=input("Enter the Output Result: ")
    

    if not data:
        print("❌ No input received.")
        return

    # Token length check
    tokens = tokenizer(data, return_tensors="pt", truncation=False).input_ids[0]
    token_chunks = [tokens[i:i+1024] for i in range(0, len(tokens), 1024)]

    print(f"🧠 Found {len(token_chunks)} chunk(s). Processing...")

    partial_summaries = []
    for i, chunk in enumerate(token_chunks):
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        summary = summarizer(chunk_text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
        print(f"✅ Chunk {i+1} summarized.")
        partial_summaries.append(summary)


def script_automation():
    print("-" * 60)
    print("🛠️  Script Automation Suite")
    print("-" * 60)
    print("This tool can help you automate repetitive tasks like:")
    print("1. 🕓 Setting up cron jobs for repeated command execution.")
    print("2. 🔍 Running common tools like nmap, ffuf, etc., with predefined flags.")
    print("-" * 60)
    print("Examples you could ask this tool to do:")
    print("• nmap scan.")
    print("• Run ffuf on a given URL with a custom wordlist.")
    print("• Scheduling a process.")
    print("• Summarize results from a tool output using AI.")
    print("-" * 60)

    while True:
        choice = input("✍️  Write keywords from the example or type 'exit' to go back: ").strip().lower()

        if "nmap" in choice:
            print("🛰️ Running Nmap automation module...")
            call_nmap_automation()
        elif "ffuf" in choice:
            print("🔎 Starting ffuf automation...")
            call_ffuf_automation()
        elif "schedule" in choice or "cron" in choice:
            print("⏱️ Scheduling task using cron...")
            call_schedule_task()
        elif "summarize" in choice:
            print("📄 Summarizing tool output using AI...")
            call_summary_module()
        elif choice == "exit":
            print("👋 Exiting script automation.")
            break
        else:
            print("⚠️ No valid option selected. Try again.")
if __name__ == "__main__":
    script_automation()