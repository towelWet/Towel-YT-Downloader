#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import threading


class YTDlpGUI(tk.Tk):
    """
    A tkinter-based GUI for downloading videos using yt-dlp.
    """

    def __init__(self):
        super().__init__()
        self.title("Towel YT Downloader")

        # Increase the window size and allow resizing
        self.geometry("650x400")
        self.resizable(True, True)

        # Configure a grid layout with some space
        self.columnconfigure(1, weight=1)  # Let column 1 expand
        self.rowconfigure(4, weight=1)    # Let the text area row expand

        # URL Label and Entry
        self.url_label = ttk.Label(self, text="Video URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self, textvariable=self.url_var, width=60)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Format Label and Dropdown
        self.format_label = ttk.Label(self, text="Format:")
        self.format_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.format_var = tk.StringVar(value="best")
        self.format_combobox = ttk.Combobox(
            self,
            textvariable=self.format_var,
            values=["best", "worst", "bestvideo", "bestaudio", "mp4", "webm"],
            state="readonly"
        )
        self.format_combobox.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Download Folder Label and Entry
        self.folder_label = ttk.Label(self, text="Download Folder:")
        self.folder_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.download_dir_var = tk.StringVar()
        self.folder_entry = ttk.Entry(self, textvariable=self.download_dir_var, width=40)
        self.folder_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.folder_button = ttk.Button(self, text="Browse...", command=self.choose_folder)
        self.folder_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Download Button
        self.download_button = ttk.Button(self, text="Download", command=self.start_download)
        self.download_button.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Text Area for output
        self.output_text = tk.Text(self, wrap="word")
        self.output_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Scrollbar for output
        self.scrollbar = ttk.Scrollbar(self, command=self.output_text.yview)
        self.scrollbar.grid(row=4, column=3, sticky="ns")
        self.output_text.config(yscrollcommand=self.scrollbar.set)

    def choose_folder(self):
        """Prompt the user to choose a download folder."""
        folder = filedialog.askdirectory()
        if folder:
            self.download_dir_var.set(folder)

    def start_download(self):
        """
        Start a new thread to run the download process
        so that the GUI remains responsive.
        """
        url = self.url_var.get().strip()
        fmt = self.format_var.get().strip()
        download_folder = self.download_dir_var.get().strip()

        if not url:
            self.output_text.insert(tk.END, "Please enter a valid URL.\n")
            return

        # Disable the button during download
        self.download_button.config(state=tk.DISABLED)
        self.output_text.delete("1.0", tk.END)

        download_thread = threading.Thread(
            target=self.download_video,
            args=(url, fmt, download_folder),
            daemon=True
        )
        download_thread.start()

    def download_video(self, url, fmt, folder):
        """
        Download the video using yt-dlp and capture the output.
        """
        # If a download folder is chosen, pass it via --paths
        command = ["yt-dlp", "-f", fmt]
        if folder:
            command += ["--paths", folder]
        command.append(url)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            self.output_text.insert(tk.END, line)
            self.output_text.see(tk.END)

        process.wait()
        self.download_button.config(state=tk.NORMAL)


def main():
    app = YTDlpGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
