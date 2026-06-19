import sqlite3
import os

# Path to the shared database file
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "central_server", "swarm_rescue.db")

def fetch_all_logs():
    """Helper function to fetch telemetry records directly from the DB."""
    if not os.path.exists(DB_PATH):
        print(f"❌ Database file not found at: {DB_PATH}")
        print("Run the central server and mock drone script first to generate data!")
        return []
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Query matching your models.py structure
    cursor.execute("SELECT drone_id, timestamp, coords, human_detected, fire_detected FROM telemetry_logs")
    rows = cursor.fetchall()
    conn.close()
    return rows

def build_network_graph():
    print("🔄 Fetching spatial paths from backend database...")
    logs = fetch_all_logs()
    
    if not logs:
        return

    print(f"📊 Successfully loaded {len(logs)} tracking packets.")
    print("--- Parsing Spatial Coordinates for Graph Matrix ---")
    
    for log in logs:
        drone_id, timestamp, coords_str, human, fire = log
        
        # Convert the string format "4.2,1.5,2.3" back into numerical math floats
        coords = [float(x) for x in coords_str.split(",")]
        
        print(f"[Drone {drone_id}] Node position parsed: X={coords[0]}, Y={coords[1]}, Z={coords[2]}")
        
        # TODO (MEMBER 2): Write the Adjacency Matrix & Shortest Path logic here.
        # Use 'coords' to calculate node distances and stitch the graph together.

if __name__ == "__main__":
    build_network_graph()