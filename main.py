import linuxcommand
import scripts
import json
import methodologies
import subprocess
import datetime
import os
import re
from transformers import pipeline, AutoTokenizer
def main():
    print("-" * 70)
    print("\t\t Welcome to Litrix ^_^")
    print("-" * 70)
    print("I can help you with a few things related to cybersecurity.")
    print("-" * 70)

    while True:
        print("\nMain Menu:")
        print("1. Linux Command Help")
        print("2. Script Writing Automation")
        print("3. Hacking Methodology Explanation")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            linuxcommand.lin_command()
        elif choice == "2":
            scripts.script_automation()
        elif choice == "3":
            methodologies.methodology()
        elif choice == "4":
            print("Exiting... Thank you for using Litrix!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
