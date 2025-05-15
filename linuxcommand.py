import subprocess
import re
from transformers import pipeline, AutoTokenizer

print("⏳ Loading AI  model (first time only)...")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
print("✅ Model loaded successfully.")

def lin_command():
    while True:
        cmd = input("📦 Enter a Linux command to explain: ").strip()

        try:
            # Get man page
            result = subprocess.run(['man', cmd], capture_output=True, text=True, check=True)
            content = result.stdout

            # Extract DESCRIPTION and OPTIONS sections
            lines = content.splitlines()
            description_lines = []
            options_lines = []
            capturing = None

            for line in lines:
                lower_line = line.strip().lower()

                if lower_line == "description":
                    capturing = "description"
                    continue
                if lower_line in ("options", "synopsis"):
                    capturing = "options"
                    continue
                if re.match(r'^[A-Z ]+$', line.strip()) and len(line.strip()) < 40:
                    capturing = None

                if capturing == "description":
                    description_lines.append(line)
                elif capturing == "options":
                    options_lines.append(line)

            combined_text = "\n".join(description_lines + options_lines).strip()

            if not combined_text:
                print("❌ No DESCRIPTION or OPTIONS found to summarize.")
                continue

            print("📄 Splitting long man page content into chunks...")

            # Tokenize into 1024-token chunks
            tokens = tokenizer(combined_text, return_tensors="pt", truncation=False).input_ids[0]
            token_chunks = [tokens[i:i + 1023] for i in range(0, len(tokens), 1023)]

            print(f"🧠 Found {len(token_chunks)} chunk(s). Summarizing each...")

            partial_summaries = []

            for i, chunk in enumerate(token_chunks):
                # Enforce strict 1024-token length by truncating and skipping any overflow
                safe_chunk = chunk[:1023]  # Explicitly enforce no more than 1024 tokens

                chunk_text = tokenizer.decode(safe_chunk, skip_special_tokens=True)

                # Check if the decoded text is still within the model's token limit
                reencoded = tokenizer(chunk_text, return_tensors="pt", truncation=True, max_length=1023)
                trimmed_text = tokenizer.decode(reencoded.input_ids[0], skip_special_tokens=True)

                try:
                    # Summarize the chunk
                    summary = summarizer(trimmed_text, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
                    print(f"✅ Chunk {i+1} summarized.")
                    partial_summaries.append(summary)
                except Exception as e:
                    print(f"❌ Failed to summarize chunk {i+1}: {e}")

            # Combine all summaries into the final condensed summary
            final_summary = " ".join(partial_summaries)
            print("\n🧠 Final condensed summary:")
            print(final_summary)

        except subprocess.CalledProcessError:
            print(f"❌ Man page for '{cmd}' not found. Is the command installed?")

        # Ask if user wants to continue
        choicee = input("\n🔁 Continue? (y/n): ").strip().lower()
        if choicee == "n":
            print("👋 Exiting Linux command explainer.")
            break

if __name__ == "__main__":
    lin_command()
