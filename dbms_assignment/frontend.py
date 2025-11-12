import streamlit as st
import pandas as pd
from connection import get_connection

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="🚌 Bus Reservation System", layout="wide")

st.markdown("""
<style>
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        height: 40px;
        width: 150px;
    }
    .stButton>button:hover {
        background-color: #004999;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚌 Online Bus Reservation System")

# -------------------- MENU --------------------
menu = ["Home", "View Buses", "Book Ticket", "View My Bookings", "Admin Panel"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------- HOME --------------------
if choice == "Home":
    st.header("Welcome to the Online Bus Reservation System")
    st.write("""
        This system allows passengers to:
        - View available bus schedules  
        - Book and cancel tickets  
        - Check fares and routes  

        Admins can manage buses, routes, and schedules.
    """)

# -------------------- VIEW BUSES --------------------
elif choice == "View Buses":
    conn = get_connection()
    query = """
        SELECT s.schedule_id, b.bus_name, b.bus_type, r.source, r.destination,
               s.departure_time, s.arrival_time, s.fare
        FROM schedules s
        JOIN buses b ON s.bus_id = b.bus_id
        JOIN routes r ON s.route_id = r.route_id;
    """
    df = pd.read_sql(query, conn)
    st.subheader("Available Bus Schedules")
    st.dataframe(df)

# -------------------- BOOK TICKET --------------------
elif choice == "Book Ticket":
    st.subheader("🎫 Book Your Ticket")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    schedule_id = st.number_input("Enter Schedule ID", min_value=1, step=1)
    seat_no = st.number_input("Seat Number", min_value=1, step=1)

    if st.button("Book Now"):
        conn = get_connection()
        cur = conn.cursor()
        # Add passenger
        cur.execute("INSERT INTO passengers (name, email, phone) VALUES (%s, %s, %s)", 
                    (name, email, phone))
        passenger_id = cur.lastrowid
        # Add ticket
        cur.execute(
            "INSERT INTO tickets (schedule_id, passenger_id, seat_no) VALUES (%s, %s, %s)",
            (schedule_id, passenger_id, seat_no),
        )
        conn.commit()
        st.success(f"✅ Ticket booked successfully! Passenger ID: {passenger_id}")
        cur.close()

# -------------------- VIEW MY BOOKINGS --------------------
elif choice == "View My Bookings":
    st.subheader("🔍 View or Cancel Your Bookings")
    email = st.text_input("Enter your email to find your bookings")

    if st.button("Search"):
        conn = get_connection()
        query = """
            SELECT t.ticket_id, p.name, p.email, b.bus_name, r.source, r.destination,
                   s.departure_time, s.arrival_time, s.fare, t.seat_no, t.status
            FROM tickets t
            JOIN passengers p ON t.passenger_id = p.passenger_id
            JOIN schedules s ON t.schedule_id = s.schedule_id
            JOIN buses b ON s.bus_id = b.bus_id
            JOIN routes r ON s.route_id = r.route_id
            WHERE p.email = %s;
        """
        df = pd.read_sql(query, conn, params=[email])

        if not df.empty:
            st.dataframe(df)
            cancel_id = st.number_input("Enter Ticket ID to Cancel", min_value=1, step=1)
            if st.button("Cancel Ticket"):
                cur = conn.cursor()
                cur.execute("UPDATE tickets SET status='cancelled' WHERE ticket_id=%s", (cancel_id,))
                conn.commit()
                st.success(f"❌ Ticket ID {cancel_id} cancelled successfully!")
        else:
            st.warning("No bookings found for this email.")

# -------------------- ADMIN PANEL --------------------
elif choice == "Admin Panel":
    st.subheader("🛠️ Admin Panel")
    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":
        st.success("Access Granted!")
        admin_choice = st.radio("Choose Action", ["Add Bus", "Add Route", "Add Schedule", "View All Tickets"])

        # Add Bus
        if admin_choice == "Add Bus":
            bus_name = st.text_input("Bus Name")
            bus_type = st.selectbox("Bus Type", ["AC", "Non-AC", "Sleeper"])
            total_seats = st.number_input("Total Seats", min_value=10, step=1)
            if st.button("Add Bus"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO buses (bus_name, bus_type, total_seats) VALUES (%s, %s, %s)", 
                            (bus_name, bus_type, total_seats))
                conn.commit()
                st.success("✅ Bus added successfully!")

        # Add Route
        elif admin_choice == "Add Route":
            source = st.text_input("Source")
            destination = st.text_input("Destination")
            distance = st.number_input("Distance (km)", min_value=1, step=1)
            if st.button("Add Route"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO routes (source, destination, distance) VALUES (%s, %s, %s)", 
                            (source, destination, distance))
                conn.commit()
                st.success("✅ Route added successfully!")

        # Add Schedule
        elif admin_choice == "Add Schedule":
            bus_id = st.number_input("Bus ID", min_value=1, step=1)
            route_id = st.number_input("Route ID", min_value=1, step=1)
            departure = st.text_input("Departure Time (YYYY-MM-DD HH:MM:SS)")
            arrival = st.text_input("Arrival Time (YYYY-MM-DD HH:MM:SS)")
            fare = st.number_input("Fare", min_value=1.0, step=0.5)
            if st.button("Add Schedule"):
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO schedules (bus_id, route_id, departure_time, arrival_time, fare) VALUES (%s, %s, %s, %s, %s)",
                    (bus_id, route_id, departure, arrival, fare),
                )
                conn.commit()
                st.success("✅ Schedule added successfully!")

        # View All Tickets (Admin)
        elif admin_choice == "View All Tickets":
            conn = get_connection()
            df = pd.read_sql("""
                SELECT t.ticket_id, p.name, p.email, b.bus_name, r.source, r.destination, 
                       s.departure_time, s.arrival_time, s.fare, t.seat_no, t.status
                FROM tickets t
                JOIN passengers p ON t.passenger_id = p.passenger_id
                JOIN schedules s ON t.schedule_id = s.schedule_id
                JOIN buses b ON s.bus_id = b.bus_id
                JOIN routes r ON s.route_id = r.route_id;
            """, conn)
            st.dataframe(df)
    else:
        if password:
            st.error("❌ Incorrect password")

