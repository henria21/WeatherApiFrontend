import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title
        title_label = ttk.Label(root, text="Weather Forecast", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        # City selection frame
        frame = ttk.Frame(root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # City label
        city_label = ttk.Label(frame, text="Select City:", font=("Arial", 12))
        city_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Dropdown for cities
        self.cities = ["New York", "London", "Tokyo", "Paris"]
        self.city_var = tk.StringVar(value=self.cities[0])
        self.dropdown = ttk.Combobox(
            frame, 
            textvariable=self.city_var, 
            values=self.cities,
            state="readonly",
            width=30
        )
        self.dropdown.pack(anchor=tk.W, pady=(0, 20))
        
        # Submit button
        self.submit_btn = ttk.Button(frame, text="Get Weather", command=self.fetch_weather)
        self.submit_btn.pack(pady=10)
        
        # Result text area
        result_label = ttk.Label(frame, text="Weather Info:", font=("Arial", 10))
        result_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.result_text = tk.Text(frame, height=10, width=50, wrap=tk.WORD)
        self.result_text.pack(pady=(0, 10))
        
        # Scrollbar for text area
        scrollbar = ttk.Scrollbar(self.result_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
        
        # Status label
        self.status_label = ttk.Label(frame, text="", foreground="gray")
        self.status_label.pack(anchor=tk.W, pady=(10, 0))
    
    def fetch_weather(self):
        """Fetch weather data from backend API"""
        city = self.city_var.get()
        
        # Disable button during request
        self.submit_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Loading...", foreground="blue")
        self.root.update()
        
        # Run API call in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._api_call, args=(city,))
        thread.start()
    
    def _api_call(self, city):
        """Make API call to backend"""
        try:
            # Backend API running on localhost:8000
            api_url = "http://127.0.0.1:8000/weather"
            params = {"location": city, "include_extra": True}
            
            response = requests.get(api_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self._display_result(data)
                self.status_label.config(text="✓ Data loaded successfully", foreground="green")
            else:
                self.status_label.config(text=f"✗ Error: {response.status_code}", foreground="red")
                messagebox.showerror("Error", f"API Error: {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            self.status_label.config(text="✗ Cannot connect to backend", foreground="red")
            messagebox.showerror("Connection Error", 
                               "Cannot connect to backend API.\nMake sure backend is running on http://127.0.0.1:8000")
        except requests.exceptions.Timeout:
            self.status_label.config(text="✗ Request timeout", foreground="red")
            messagebox.showerror("Timeout", "Request timed out")
        except Exception as e:
            self.status_label.config(text=f"✗ Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.submit_btn.config(state=tk.NORMAL)
    
    def _display_result(self, data):
        """Display weather data in the text area"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Format the response data
        if isinstance(data, dict):
            for key, value in data.items():
                self.result_text.insert(tk.END, f"{key}: {value}\n")
        else:
            self.result_text.insert(tk.END, str(data))
        
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
