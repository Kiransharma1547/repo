import streamlit as st
import subprocess

# Streamlit App Config
st.set_page_config(page_title="Linux Command Center 🐧", page_icon="💻")
st.title("🐧 Linux Command Menu (50 Commands)")

# Linux Commands Database
commands = {
    "File Operations": {
        "ls": "List directory contents",
        "pwd": "Show current directory",
        "cd": "Change directory",
        "mkdir": "Create a new directory",
        "rmdir": "Remove an empty directory",
        "touch": "Create a new empty file",
        "cp": "Copy files or directories",
        "mv": "Move or rename files",
        "rm": "Remove files",
        "find": "Search for files in a directory"
    },
    "File Viewing & Editing": {
        "cat": "View file content",
        "less": "View file content (scrollable)",
        "more": "View file content (paged)",
        "head": "Show first lines of a file",
        "tail": "Show last lines of a file",
        "nano": "Edit file in nano editor",
        "vim": "Edit file in vim editor",
        "wc": "Count words, lines, and characters",
        "stat": "Show detailed file information",
        "file": "Determine file type"
    },
    "System Information": {
        "whoami": "Show current user",
        "uname -a": "Show system information",
        "hostname": "Show system hostname",
        "uptime": "Show system uptime",
        "df -h": "Show disk usage",
        "du -sh": "Show folder size",
        "top -n 1 -b": "Show running processes (snapshot)",
        "htop": "Interactive process viewer",
        "free -h": "Show memory usage",
        "ps aux": "Show all processes"
    },
    "Networking": {
        "ping -c 4 google.com": "Check network connectivity",
        "ifconfig": "Show network interfaces",
        "ip a": "Show IP addresses",
        "netstat -tuln": "Show listening ports",
        "curl example.com": "Fetch web content",
        "wget example.com": "Download a file",
        "ssh user@host": "SSH into another machine",
        "scp file user@host:/path": "Securely copy files",
        "traceroute google.com": "Trace route to a host",
        "dig google.com": "DNS lookup"
    },
    "User Management": {
        "who": "Show logged-in users",
        "id": "Show user ID and groups",
        "groups": "Show groups for a user",
        "adduser newuser": "Add a new user",
        "passwd": "Change user password",
        "usermod": "Modify a user account",
        "deluser username": "Delete a user",
        "chmod": "Change file permissions",
        "chown": "Change file ownership",
        "sudo": "Run command as superuser"
    }
}

# Sidebar Category & Command
category = st.sidebar.selectbox("📂 Select Category", list(commands.keys()))
command = st.selectbox("💻 Select Command", list(commands[category].keys()))

# Show description & command syntax
st.write(f"**📄 Description:** {commands[category][command]}")
st.code(command, language="bash")

# Auto-run and show output
try:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    st.subheader("📜 Output:")
    st.code(result.stdout if result.stdout else "No output", language="bash")

    if result.stderr:
        st.error(result.stderr)

except Exception as e:
    st.error(f"Error running command: {e}")

