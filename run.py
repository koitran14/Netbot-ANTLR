import os
import subprocess
import sys

antlr_jar = "lib/antlr4-4.9.2-complete.jar"
grammar_file = "src/grammar/Command.g4"
output_dir = "src/generated"

def generate_script():
    try:
        """Generate the parser script using ANTLR4."""
        if not os.path.isfile(antlr_jar):
            print(f"Error: ANTLR4 JAR not found at {antlr_jar}")
            sys.exit(1)
        if not os.path.isfile(grammar_file):
            print(f"Error: Grammar file not found at {grammar_file}")
            sys.exit(1)

        # Construct the ANTLR4 command
        command = [
            "java",
            "-jar",
            antlr_jar,
            "-Dlanguage=Python3",
            "-visitor",
            "-o",
            output_dir,
            grammar_file
        ]

        print("Generating script...")
        subprocess.run(command, check=True)
        print("Parser generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error generating parser: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Java executable not found. Ensure Java is installed and in PATH.")
        sys.exit(1)
        
def run_gui():
    """Run the GUI."""
    print("Running GUI...")
    
    # Add your GUI logic here
    try: 
        subprocess.run([sys.executable, "-m", "src.interfaces.gui"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing GUI: {e}")
        sys.exit(1)
    except ModuleNotFoundError:
        print("Error: GUI module not found in src.interfaces")
        sys.exit(1)

def run_cli():
    """Execute the CLI interface."""
    try:
        subprocess.run([sys.executable, "-m", "src.interfaces.cli"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing CLI: {e}")
        sys.exit(1)
    except ModuleNotFoundError:
        print("Error: CLI module not found in src.interfaces")
        sys.exit(1)

def main(args):
    """Process command-line arguments."""
    print("Starting the script...")
    if len(args) == 0: 
        print("Usage: python run.py [gen|gui|cli]")
        sys.exit(1)
        
    command = args[0].lower()
        
    if command == 'gen':
        generate_script()
    elif command == 'gui':
        run_gui()
    elif command == 'cli':
        run_cli()
    else: 
        print(f"Unknown command: {command}")
        print("Available commands: gen, gui, cli")
        sys.exit(1)
        

if __name__ == "__main__":
    main(sys.argv[1:])