from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ── DUMMY DATA ─────────────────────────────────────────────
DIVISIONS = [
    {"Div_ID": 1, "name": "Division A", "Max_Session": 8},
    {"Div_ID": 2, "name": "Division B", "Max_Session": 6},
    {"Div_ID": 3, "name": "Division C", "Max_Session": 6},
]

SESSIONS = [
    {"Sess_ID": 1, "Time_slot": "Morning",   "Duration": "09:00 – 10:30", "Capacity": 20},
    {"Sess_ID": 2, "Time_slot": "Midday",    "Duration": "11:00 – 12:30", "Capacity": 20},
    {"Sess_ID": 3, "Time_slot": "Afternoon", "Duration": "13:00 – 14:30", "Capacity": 20},
]

PARTICIPANTS = [
    {"Pat_ID": 1,  "Name": "Amara",    "Surname": "Dlamini",   "Email": "amara.d@derivco.com",    "Div_ID": 1},
    {"Pat_ID": 2,  "Name": "Bongani",  "Surname": "Khumalo",   "Email": "bongani.k@derivco.com",  "Div_ID": 1},
    {"Pat_ID": 3,  "Name": "Chloe",    "Surname": "Nkosi",     "Email": "chloe.n@derivco.com",    "Div_ID": 1},
    {"Pat_ID": 4,  "Name": "Dineo",    "Surname": "Mokoena",   "Email": "dineo.m@derivco.com",    "Div_ID": 1},
    {"Pat_ID": 5,  "Name": "Ethan",    "Surname": "Sithole",   "Email": "ethan.s@derivco.com",    "Div_ID": 1},
    {"Pat_ID": 6,  "Name": "Fatima",   "Surname": "Mahlangu",  "Email": "fatima.m@derivco.com",   "Div_ID": 1},
    {"Pat_ID": 7,  "Name": "Gareth",   "Surname": "Ndlovu",    "Email": "gareth.n@derivco.com",   "Div_ID": 1},
    {"Pat_ID": 8,  "Name": "Hlengiwe", "Surname": "Zulu",      "Email": "hlengiwe.z@derivco.com", "Div_ID": 1},
    {"Pat_ID": 9,  "Name": "Ivan",     "Surname": "Mthembu",   "Email": "ivan.m@derivco.com",     "Div_ID": 2},
    {"Pat_ID": 10, "Name": "Jade",     "Surname": "Shabalala", "Email": "jade.s@derivco.com",     "Div_ID": 2},
    {"Pat_ID": 11, "Name": "Kagiso",   "Surname": "Langa",     "Email": "kagiso.l@derivco.com",   "Div_ID": 2},
    {"Pat_ID": 12, "Name": "Lerato",   "Surname": "Cele",      "Email": "lerato.c@derivco.com",   "Div_ID": 2},
    {"Pat_ID": 13, "Name": "Mpho",     "Surname": "Mkhize",    "Email": "mpho.m@derivco.com",     "Div_ID": 2},
    {"Pat_ID": 14, "Name": "Naledi",   "Surname": "Buthelezi", "Email": "naledi.b@derivco.com",   "Div_ID": 2},
    {"Pat_ID": 15, "Name": "Oscar",    "Surname": "Mhlongo",   "Email": "oscar.m@derivco.com",    "Div_ID": 3},
    {"Pat_ID": 16, "Name": "Palesa",   "Surname": "Hadebe",    "Email": "palesa.h@derivco.com",   "Div_ID": 3},
    {"Pat_ID": 17, "Name": "Quinton",  "Surname": "Ntuli",     "Email": "quinton.n@derivco.com",  "Div_ID": 3},
    {"Pat_ID": 18, "Name": "Riana",    "Surname": "Mthethwa",  "Email": "riana.m@derivco.com",    "Div_ID": 3},
    {"Pat_ID": 19, "Name": "Sipho",    "Surname": "Gumede",    "Email": "sipho.g@derivco.com",    "Div_ID": 3},
    {"Pat_ID": 20, "Name": "Thandeka", "Surname": "Zungu",     "Email": "thandeka.z@derivco.com", "Div_ID": 3},
]

# In-memory allocations for testing
ALLOCATIONS = []
next_alloc_id = 1

# ── PAGES ──────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("dashboard.html")

# ── API ────────────────────────────────────────────────────
@app.route("/api/divisions")
def api_divisions():
    return jsonify(DIVISIONS)

@app.route("/api/sessions")
def api_sessions():
    return jsonify(SESSIONS)

@app.route("/api/participants")
def api_participants():
    return jsonify(PARTICIPANTS)

@app.route("/api/allocations")
def api_allocations():
    return jsonify(ALLOCATIONS)

@app.route("/api/allocations", methods=["POST"])
def api_create_allocation():
    global next_alloc_id
    data = request.get_json()

    pat_id  = data.get("Pat_ID")
    sess_id = data.get("Sess_ID")
    div_id  = data.get("Div_ID")

    # Guard: already allocated
    if any(a["Pat_ID"] == pat_id for a in ALLOCATIONS):
        return jsonify({"error": "Participant already allocated."}), 400

    # Guard: session capacity
    sess = next((s for s in SESSIONS if s["Sess_ID"] == sess_id), None)
    sess_count = sum(1 for a in ALLOCATIONS if a["Sess_ID"] == sess_id)
    if sess_count >= sess["Capacity"]:
        return jsonify({"error": "Session is full (20/20)."}), 400

    # Guard: division per-session limit
    div = next((d for d in DIVISIONS if d["Div_ID"] == div_id), None)
    div_sess_count = sum(1 for a in ALLOCATIONS if a["Sess_ID"] == sess_id and a["Div_ID"] == div_id)
    if div_sess_count >= div["Max_Session"]:
        return jsonify({"error": f"{div['name']} is full for this session ({div['Max_Session']}/{div['Max_Session']})."}), 400

    alloc = {"Alloc_ID": next_alloc_id, "Pat_ID": pat_id, "Sess_ID": sess_id, "Div_ID": div_id}
    ALLOCATIONS.append(alloc)
    next_alloc_id += 1
    return jsonify(alloc), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
