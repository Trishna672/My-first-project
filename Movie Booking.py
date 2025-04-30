import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import PhotoImage
import os

class TicketBookingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Ticket Booking System")
        self.geometry("800x600")
        self.configure(bg="white")

        self.event = tk.StringVar()
        self.date = tk.StringVar()
        self.num_tickets = tk.IntVar(value=1)
        self.selected_seats = []
        self.total_price = tk.IntVar(value=0)
        self.show_time = tk.StringVar()

        # Movie posters
        self.movies = {
            "Inception": "C:/Users/ADMIN/Desktop/Inception.gif",
            "Avengers": "C:/Users/ADMIN/Desktop/Avengers.gif",
            "Interstellar": "C:/Users/ADMIN/Desktop/Interstellar.gif"
        }

        self.show_times = ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM"]

        self.poster_image = None

        self.create_booking_page()

    def create_booking_page(self):
        self.clear_window()

        tk.Label(self, text="Book Your Movie Ticket", font=("Poppins", 20, "bold"), bg="white").pack(pady=20)

        tk.Label(self, text="Select Movie:", bg="white", font=("Poppins", 12)).pack(pady=(20, 5))
        movie_menu = ttk.Combobox(self, textvariable=self.event, values=list(self.movies.keys()), state="readonly")
        movie_menu.pack()
        movie_menu.bind("<<ComboboxSelected>>", self.update_poster)

        self.poster_label = tk.Label(self, bg="white")
        self.poster_label.pack(pady=10)

        tk.Label(self, text="Date (DD/MM/YYYY):", bg="white", font=("Poppins", 12)).pack(pady=5)
        tk.Entry(self, textvariable=self.date, font=("Poppins", 12)).pack()

        tk.Label(self, text="Number of Tickets:", bg="white", font=("Poppins", 12)).pack(pady=5)
        tk.Spinbox(self, from_=1, to=10, textvariable=self.num_tickets, font=("Poppins", 12)).pack()

        tk.Label(self, text="Select Show Time:", bg="white", font=("Poppins", 12)).pack(pady=5)
        show_time_menu = ttk.Combobox(self, textvariable=self.show_time, values=self.show_times, state="readonly")
        show_time_menu.pack()

        tk.Button(self, text="Select Seats", font=("Poppins", 12), bg="#007bff", fg="white",
                  command=self.show_seat_selection_page).pack(pady=20)

    def update_poster(self, event=None):
        movie = self.event.get()
        path = self.movies.get(movie, "")
        try:
            self.poster_image = tk.PhotoImage(file=path)
            self.poster_label.config(image=self.poster_image)
        except Exception as e:
            self.poster_label.config(text="Poster not found", image="", fg="gray", font=("Poppins", 10))

    def show_seat_selection_page(self):
        if not self.event.get() or not self.date.get() or not self.show_time.get():
            messagebox.showerror("Input Error", "Please fill all details.")
            return

        self.clear_window()
        tk.Label(self, text="Select Your Seats", font=("Poppins", 18, "bold"), bg="white").pack(pady=10)

        seat_frame = tk.Frame(self, bg="white")
        seat_frame.pack()

        self.seat_buttons = {}
        self.selected_seats.clear()
        self.total_price.set(0)

        tiers = {
            "Premium": {"rows": ['A', 'B', 'C'], "price": 300, "color": "#d9534f"},
            "Standard": {"rows": ['D', 'E', 'F', 'G'], "price": 200, "color": "#f0ad4e"},
            "Economy": {"rows": ['H', 'I', 'J'], "price": 150, "color": "#5cb85c"}
        }

        occupied_seats = ["A1", "B4", "D5", "E6", "F7"]

        for i, row_letter in enumerate("ABCDEFGHIJ"):
            for j in range(1, 11):
                seat_code = f"{row_letter}{j}"
                btn = tk.Checkbutton(seat_frame, text=seat_code, font=("Poppins", 9), bg="white",
                                     indicatoron=False, width=4, command=lambda s=seat_code: self.toggle_seat(s))
                btn.grid(row=i, column=j, padx=4, pady=4)
                self.seat_buttons[seat_code] = btn

                # Color seat based on tier
                for tier in tiers.values():
                    if row_letter in tier["rows"]:
                        btn.config(bg=tier["color"])
                        btn.tier_price = tier["price"]

                # Mark some seats as occupied
                if seat_code in occupied_seats:
                    btn.config(state="disabled", bg="gray")

        self.selected_label = tk.Label(self, text="Selected Seats: None", bg="white", font=("Poppins", 12))
        self.selected_label.pack(pady=10)

        self.total_label = tk.Label(self, text="Total Price: ₹0", bg="white", font=("Poppins", 12))
        self.total_label.pack()

        nav_frame = tk.Frame(self, bg="white")
        nav_frame.pack(pady=20)

        tk.Button(nav_frame, text="Cancel", font=("Poppins", 11), bg="red", fg="white",
                  command=self.create_booking_page).pack(side="left", padx=10)

        tk.Button(nav_frame, text="Book Tickets", font=("Poppins", 11), bg="green", fg="white",
                  command=self.show_print_ticket_page).pack(side="right", padx=10)

    def toggle_seat(self, seat):
        btn = self.seat_buttons[seat]
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            btn.deselect()
        else:
            if len(self.selected_seats) >= self.num_tickets.get():
                messagebox.showwarning("Limit Exceeded", "You can't select more seats than the number of tickets.")
                return
            self.selected_seats.append(seat)
            btn.select()

        self.update_total_price()

    def update_total_price(self):
        total = 0
        for seat in self.selected_seats:
            tier_price = self.seat_buttons[seat].tier_price
            total += tier_price
        self.total_price.set(total)
        self.selected_label.config(text=f"Selected Seats: {', '.join(self.selected_seats) or 'None'}")
        self.total_label.config(text=f"Total Price: ₹{total}")

    def show_print_ticket_page(self):
        if not self.selected_seats:
            messagebox.showerror("No Seats", "Please select at least one seat.")
            return

        self.clear_window()

        tk.Label(self, text="🎟 Ticket Details", font=("Poppins", 18, "bold"), bg="white").pack(pady=20)

        self.ticket_details = f"""Movie: {self.event.get()}
Date: {self.date.get()}
Show Time: {self.show_time.get()}
Tickets: {self.num_tickets.get()}
Seats: {', '.join(self.selected_seats)}
Total Amount: ₹{self.total_price.get()}"""

        tk.Label(self, text=self.ticket_details, bg="white", font=("Poppins", 12), justify="left").pack()

        tk.Button(self, text="Print Ticket", font=("Poppins", 12), bg="blue", fg="white",
                  command=lambda: messagebox.showinfo("Print", "Ticket printed successfully!")).pack(pady=10)

        tk.Button(self, text="Save Ticket", font=("Poppins", 12), bg="green", fg="white",
                  command=self.save_ticket_to_file).pack(pady=10)

        tk.Button(self, text="New Booking", font=("Poppins", 12), bg="gray", fg="white",
                  command=self.create_booking_page).pack(pady=10)

    def save_ticket_to_file(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title="Save Ticket As"
            )
            if not file_path:
                return  # User canceled

            with open(file_path, "w", encoding="utf-8") as file:
                file.write("==== MOVIE TICKET ====\n")
                file.write(f"Movie: {self.event.get()}\n")
                file.write(f"Date: {self.date.get()}\n")
                file.write(f"Show Time: {self.show_time.get()}\n")
                file.write(f"Seats: {', '.join(self.selected_seats)}\n")
                file.write(f"Total Price: ₹{self.total_price.get()}\n")
                file.write("\n======================\n")

            messagebox.showinfo("Success", f"Ticket saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save ticket.\n{e}")

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = TicketBookingApp()
    app.mainloop()




