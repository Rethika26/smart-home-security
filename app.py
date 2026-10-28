import ipaddress
import re
import subprocess
from html import escape
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="SMART RISKS | Connected Device Security",
    page_icon="\U0001f6e1",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design system CSS ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --bg:       #080D16;
  --s1:       #0F1B2D;
  --s2:       #152236;
  --s3:       #1A2B42;
  --b1:       #1E3048;
  --b2:       #2A4060;
  --teal:     #2DD4BF;
  --td:       rgba(45,212,191,.12);
  --tg:       rgba(45,212,191,.25);
  --tx:       #E2E8F0;
  --tx2:      #94A3B8;
  --tx3:      #64748B;
  --hi:       #F87171;
  --hid:      rgba(248,113,113,.12);
  --hib:      rgba(248,113,113,.30);
  --me:       #FBBF24;
  --med:      rgba(251,191,36,.12);
  --meb:      rgba(251,191,36,.30);
  --lo:       #34D399;
  --lod:      rgba(52,211,153,.10);
  --lob:      rgba(52,211,153,.28);
  --inf:      #60A5FA;
  --infd:     rgba(96,165,250,.10);
  --infb:     rgba(96,165,250,.28);
}

*,*::before,*::after{box-sizing:border-box}
html,body,[class*="css"]{
  font-family:'Inter',system-ui,sans-serif!important;
  color:var(--tx)!important;
  background:var(--bg)!important;
}

/* Kill Streamlit chrome */
#MainMenu,footer,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
[data-testid="stHeader"]{background:transparent!important;height:0!important;min-height:0!important;overflow:hidden!important}
.stApp{background:var(--bg)!important}
.block-container{max-width:100%!important;padding:0.9rem 1.5rem 2rem!important}

/* Headings */
h1,h2,h3,h4,h5,h6{color:var(--tx)!important;margin:0!important;font-weight:700!important}
p{color:var(--tx2)!important}
label,.stSelectbox label,.stNumberInput label,.stCheckbox label{
  color:var(--tx2)!important;font-size:.75rem!important;font-weight:600!important;
  text-transform:uppercase!important;letter-spacing:.04em!important}
code{color:var(--teal)!important;background:var(--s2)!important;border-radius:3px!important;padding:1px 4px!important}

/* Sidebar */
[data-testid="stSidebar"]{
  background:var(--s1)!important;
  border-right:1px solid var(--b1)!important;
  min-width:210px!important;max-width:210px!important}
[data-testid="stSidebar"]>div:first-child{padding:0!important}
[data-testid="stSidebar"] .stRadio>label{display:none!important}
[data-testid="stSidebar"] [role="radiogroup"]{gap:2px!important;padding:0 8px!important}
[data-testid="stSidebar"] [role="radiogroup"]>label{
  border-radius:6px!important;padding:9px 12px!important;margin:1px 0!important;
  border:1px solid transparent!important;background:transparent!important;
  cursor:pointer!important;transition:all .12s ease!important}
[data-testid="stSidebar"] [role="radiogroup"]>label>div:first-child{display:none!important}
[data-testid="stSidebar"] [role="radiogroup"]>label p{
  color:var(--tx2)!important;font-size:.8rem!important;font-weight:500!important;margin:0!important}
[data-testid="stSidebar"] [role="radiogroup"]>label:hover{
  background:var(--s2)!important;border-color:var(--b1)!important}
[data-testid="stSidebar"] [role="radiogroup"]>label:has(input:checked){
  background:var(--td)!important;border-color:rgba(45,212,191,.35)!important;
  border-left:3px solid var(--teal)!important}
[data-testid="stSidebar"] [role="radiogroup"]>label:has(input:checked) p{
  color:var(--tx)!important;font-weight:600!important}

/* Inputs */
input,textarea,.stTextInput input,.stNumberInput input{
  background:var(--s2)!important;border-color:var(--b1)!important;
  color:var(--tx)!important;border-radius:5px!important;font-size:.82rem!important}
input:focus,.stTextInput input:focus,.stNumberInput input:focus{
  border-color:var(--teal)!important;box-shadow:0 0 0 2px var(--td)!important;outline:none!important}
[data-baseweb="select"]>div{
  background:var(--s2)!important;border-color:var(--b1)!important;
  color:var(--tx)!important;border-radius:5px!important;font-size:.82rem!important}
[data-baseweb="select"]>div:focus-within{
  border-color:var(--teal)!important;box-shadow:0 0 0 2px var(--td)!important}
[data-baseweb="popover"],[data-baseweb="menu"]{
  background:var(--s2)!important;border-color:var(--b1)!important}
[data-baseweb="option"]{color:var(--tx)!important}
[data-baseweb="option"]:hover{background:var(--s3)!important}
[data-baseweb="tag"]{background:var(--s3)!important;color:var(--teal)!important;border-color:var(--b2)!important}

/* Buttons */
div.stButton>button,div.stDownloadButton>button,
div[data-testid="stFormSubmitButton"]>button{
  background:var(--s2)!important;border:1px solid var(--b2)!important;
  color:var(--tx)!important;border-radius:5px!important;
  font-size:.78rem!important;font-weight:600!important;
  letter-spacing:.02em!important;padding:.42rem .9rem!important;
  transition:all .12s ease!important;box-shadow:none!important}
div.stButton>button:hover,div.stDownloadButton>button:hover,
div[data-testid="stFormSubmitButton"]>button:hover{
  background:var(--s3)!important;border-color:var(--teal)!important;color:var(--tx)!important}
div.stButton>button[kind="primary"],
div[data-testid="stFormSubmitButton"]>button[kind="primary"],
button[data-testid="stBaseButton-primaryFormSubmit"]{
  background:var(--teal)!important;border-color:var(--teal)!important;
  color:#080D16!important;font-weight:700!important;box-shadow:0 2px 10px var(--tg)!important}
div.stButton>button[kind="primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover{
  background:#26B5A0!important;border-color:#26B5A0!important;box-shadow:0 4px 16px var(--tg)!important}

/* Dataframe */
[data-testid="stDataFrame"]{
  background:var(--s1)!important;border:1px solid var(--b1)!important;border-radius:6px!important}

/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--b2);border-radius:3px}

/* ─── Component classes ─── */

/* Sidebar brand */
.sb-brand{display:flex;align-items:center;gap:10px;
  padding:14px 16px 12px;border-bottom:1px solid var(--b1);margin-bottom:6px}
.sb-icon{width:32px;height:32px;border-radius:7px;flex-shrink:0;
  background:linear-gradient(135deg,rgba(45,212,191,.22),rgba(45,212,191,.04));
  border:1px solid rgba(45,212,191,.35);display:flex;align-items:center;
  justify-content:center;font-size:15px;line-height:1}
.sb-name{font-size:.82rem;font-weight:800;letter-spacing:.1em;
  color:var(--tx)!important;line-height:1.2;display:block}
.sb-sub{font-size:.6rem;color:var(--tx3)!important;font-weight:500;
  letter-spacing:.04em;margin-top:1px;display:block}
.sb-sec{font-size:.6rem;font-weight:700;letter-spacing:.12em;
  color:var(--tx3)!important;text-transform:uppercase;padding:8px 12px 3px}
.sb-mode{margin:10px 8px 6px;background:var(--s2);border:1px solid var(--b1);
  border-radius:6px;padding:9px 12px}
.sb-mode-hd{font-size:.6rem;font-weight:700;letter-spacing:.1em;
  color:var(--tx3)!important;text-transform:uppercase;
  display:flex;justify-content:space-between;align-items:center}
.sb-mode-val{font-size:.72rem;font-weight:600;color:var(--lo)!important;
  display:flex;align-items:center;gap:5px;margin-top:5px}
.sb-mode-desc{font-size:.6rem;color:var(--tx3)!important;line-height:1.35;margin-top:3px}
.pdot{width:6px;height:6px;border-radius:50%;background:var(--lo);box-shadow:0 0 6px var(--lo);flex-shrink:0}

/* Page header */
.ph{display:flex;align-items:center;justify-content:space-between;
  padding:10px 14px;background:var(--s1);border:1px solid var(--b1);
  border-radius:7px;margin-bottom:12px;gap:12px}
.ph-l{display:flex;flex-direction:column;gap:2px}
.ph-eye{font-size:.6rem;font-weight:700;letter-spacing:.14em;color:var(--teal)!important;
  text-transform:uppercase;display:flex;align-items:center;gap:5px}
.ph-eye::before{content:"";width:4px;height:4px;border-radius:50%;
  background:var(--teal);box-shadow:0 0 6px var(--teal);flex-shrink:0}
.ph-title{font-size:1.15rem!important;font-weight:800!important;
  color:var(--tx)!important;letter-spacing:-.02em;line-height:1.2!important}
.ph-sub{font-size:.72rem;color:var(--tx2)!important;margin-top:1px}
.ph-r{display:flex;align-items:center;gap:8px;flex-shrink:0}

/* Tags */
.tag{display:inline-flex;align-items:center;gap:4px;padding:3px 8px;
  border-radius:4px;font-size:.62rem;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;white-space:nowrap;border:1px solid}
.tag-teal{color:var(--teal)!important;border-color:rgba(45,212,191,.3);background:var(--td)}
.tag-green{color:var(--lo)!important;border-color:var(--lob);background:var(--lod)}
.tag-neutral{color:var(--tx2)!important;border-color:var(--b1);background:var(--s2)}
.tdot{width:5px;height:5px;border-radius:50%;background:currentColor;box-shadow:0 0 5px currentColor}

/* KPI */
.kpi-row{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:12px}
.kpi-med::after{background:var(--me);box-shadow:0 0 8px var(--me)}
.kpi-low::after{background:var(--lo);box-shadow:0 0 8px var(--lo)}
.kpi{background:var(--s1);border:1px solid var(--b1);border-radius:7px;
  padding:12px 14px 10px;position:relative;overflow:hidden;display:flex;flex-direction:column;gap:5px}
.kpi::after{content:"";position:absolute;top:0;left:0;right:0;height:2px;background:var(--b1)}
.kpi-teal::after{background:var(--teal);box-shadow:0 0 8px var(--teal)}
.kpi-hi::after{background:var(--hi);box-shadow:0 0 8px var(--hi)}
.kpi-inf::after{background:var(--inf);box-shadow:0 0 8px var(--inf)}
.kpi-lbl{font-size:.65rem;font-weight:600;color:var(--tx2)!important;
  letter-spacing:.04em;text-transform:uppercase}
.kpi-value{font-size:1.6rem;font-weight:800;color:var(--tx)!important;
  font-family:'JetBrains Mono',monospace;line-height:1;letter-spacing:-.02em}
.kpi-value-sm{font-size:1.22rem}
.kpi-unit{font-size:.72rem;color:var(--tx3)!important;font-weight:500}
.kpi-ft{font-size:.62rem;color:var(--tx3)!important;display:flex;align-items:center;gap:4px}

/* Panel */
.panel{background:var(--s1);border:1px solid var(--b1);border-radius:7px;
  padding:12px 14px;margin-bottom:10px}
.panel-hd{display:flex;align-items:center;justify-content:space-between;
  margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid var(--b1)}
.panel-t{font-size:.72rem;font-weight:700;color:var(--tx)!important;
  text-transform:uppercase;letter-spacing:.07em}
.panel-s{font-size:.65rem;color:var(--tx3)!important;margin-top:2px}

/* Dist bars */
.dr{display:grid;grid-template-columns:54px 1fr 26px;align-items:center;gap:8px;padding:4px 0}
.dr-lbl{font-size:.72rem;font-weight:600;color:var(--tx2)!important}
.dr-track{height:5px;background:var(--s2);border-radius:3px;overflow:hidden;border:1px solid var(--b1)}
.dr-fill{height:100%;border-radius:2px}
.dr-n{font-size:.7rem;font-weight:700;font-family:'JetBrains Mono',monospace;
  color:var(--tx)!important;text-align:right}

/* Badge */
.bdg{display:inline-flex;align-items:center;gap:3px;padding:2px 7px;border-radius:4px;
  font-size:.62rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  white-space:nowrap;border:1px solid}
.bdg-high{color:var(--hi)!important;background:var(--hid);border-color:var(--hib)}
.bdg-medium,.bdg-med{color:var(--me)!important;background:var(--med);border-color:var(--meb)}
.bdg-low{color:var(--lo)!important;background:var(--lod);border-color:var(--lob)}
.bdg-info{color:var(--inf)!important;background:var(--infd);border-color:var(--infb)}
.bdg-neutral{color:var(--tx2)!important;background:var(--s2);border-color:var(--b1)}

/* Posture row */
.pr{display:flex;align-items:center;justify-content:space-between;
  padding:5px 0;border-bottom:1px solid var(--b1);font-size:.73rem}
.pr:last-child{border-bottom:none}
.pr-lbl{color:var(--tx2)!important}

/* Inventory table */
.itbl{width:100%;border-collapse:collapse}
.itbl thead tr{background:var(--s2);border-bottom:1px solid var(--b1)}
.itbl thead th{padding:7px 10px;font-size:.62rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.08em;color:var(--tx2)!important;text-align:left;white-space:nowrap}
.itbl tbody tr{background:var(--s1);border-bottom:1px solid var(--b1);transition:background .1s}
.itbl tbody tr:last-child{border-bottom:none}
.itbl tbody tr:hover{background:var(--s2)}
.itbl td{padding:7px 10px;font-size:.74rem;color:var(--tx)!important;vertical-align:middle}
.dn{font-weight:600;color:var(--tx)!important}
.dt{font-size:.63rem;color:var(--tx2)!important;margin-top:1px}
.mono{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--tx2)!important}
.sw{display:flex;align-items:center;gap:6px}
.st{flex:1;height:4px;background:var(--s3);border-radius:2px;overflow:hidden;min-width:44px}
.sf{height:100%;border-radius:2px}
.sn{font-family:'JetBrains Mono',monospace;font-size:.7rem;color:var(--tx)!important;white-space:nowrap}

/* Priority items */
.pi{padding:7px 0;border-bottom:1px solid var(--b1);display:flex;flex-direction:column;gap:3px}
.pi:last-child{border-bottom:none}
.pi-top{display:flex;align-items:center;justify-content:space-between;gap:6px}
.pi-name{font-size:.76rem;font-weight:600;color:var(--tx)!important}
.pi-sub{font-size:.69rem;color:var(--tx2)!important;line-height:1.35}

/* Activity */
.ar{display:grid;grid-template-columns:1fr auto auto;align-items:center;
  gap:8px;padding:6px 0;border-bottom:1px solid var(--b1);font-size:.72rem}
.ar:last-child{border-bottom:none}
.at{font-family:'JetBrains Mono',monospace;font-size:.68rem;color:var(--tx)!important}
.ab{display:flex;gap:4px}

/* Device banner */
.dbn{display:flex;align-items:center;justify-content:space-between;
  background:var(--s1);border:1px solid var(--b1);border-radius:7px;
  padding:10px 14px;margin-bottom:12px;gap:12px}
.dbn-name{font-size:.92rem;font-weight:700;color:var(--tx)!important}
.dbn-sub{font-size:.68rem;color:var(--tx2)!important;margin-top:2px}

/* Assessment */
.ac{background:var(--s1);border:1px solid var(--b1);border-radius:7px;
  padding:14px;margin-bottom:10px}
.ac-score{font-size:2.4rem;font-weight:800;font-family:'JetBrains Mono',monospace;
  color:var(--tx)!important;line-height:1}
.ac-denom{font-size:.85rem;color:var(--tx3)!important}
.rm{height:6px;background:var(--s2);border-radius:4px;overflow:hidden;
  border:1px solid var(--b1);margin:10px 0}
.rm-fill{height:100%;border-radius:4px}

/* Finding cards */
.fc{background:var(--s1);border:1px solid var(--b1);border-left:3px solid var(--b1);
  border-radius:6px;padding:10px 13px;margin-bottom:8px;
  display:flex;flex-direction:column;gap:5px}
.fc.high{border-left-color:var(--hi)}
.fc.medium,.fc.med{border-left-color:var(--me)}
.fc.low{border-left-color:var(--lo)}
.fc.info{border-left-color:var(--teal)}
.fc-hd{display:flex;align-items:center;justify-content:space-between;gap:8px}
.fc-title{font-size:.82rem;font-weight:700;color:var(--tx)!important}
.fc-dev{font-size:.69rem;color:var(--tx2)!important}
.fc-reason{font-size:.73rem;color:#CBD5E1!important;line-height:1.4}
.fc-reco{background:rgba(45,212,191,.05);border:1px solid rgba(45,212,191,.18);
  border-radius:4px;padding:6px 9px;font-size:.71rem;color:#99F6E4!important}

/* Alerts */
.al{display:flex;align-items:flex-start;gap:8px;padding:9px 12px;
  border-radius:6px;border:1px solid;font-size:.74rem;margin-bottom:10px;line-height:1.4}
.al-warn{background:rgba(251,191,36,.07);border-color:var(--meb);color:#FDE68A!important}
.al-info{background:rgba(96,165,250,.07);border-color:var(--infb);color:#BAE6FD!important}
.al-ok{background:rgba(52,211,153,.07);border-color:var(--lob);color:#A7F3D0!important}

.grp-title{font-size:.7rem;font-weight:700;color:var(--tx)!important;
  text-transform:uppercase;letter-spacing:.07em;margin:8px 0 5px;
  padding-bottom:4px;border-bottom:1px solid var(--b1)}

@media(max-width:1100px){.kpi-row{grid-template-columns:repeat(2,1fr)}}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────
def get_local_network_snapshot():
    try:
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return [], "Could not read the ARP cache."
        entries, seen = [], set()
        for line in result.stdout.splitlines():
            ip_m  = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)
            mac_m = re.search(r"\b(?:[0-9a-fA-F]{2}-){5}[0-9a-fA-F]{2}\b", line)
            if not ip_m or not mac_m:
                continue
            ip  = ip_m.group(0)
            mac = mac_m.group(0).lower()
            octets = [int(p) for p in ip.split(".")]
            try:
                addr = ipaddress.IPv4Address(ip)
            except ipaddress.AddressValueError:
                continue
            if octets[0] == 0 or octets[0] >= 224 or addr == ipaddress.IPv4Address("255.255.255.255"):
                continue
            if (ip, mac) not in seen:
                seen.add((ip, mac))
                entries.append({"IP Address": ip, "MAC Address": mac, "Source": "Windows ARP cache"})
        return entries, None
    except FileNotFoundError:
        return [], "This feature currently requires Windows ARP."
    except subprocess.TimeoutExpired:
        return [], "The ARP command timed out."
    except OSError as exc:
        return [], f"Unable to run Windows ARP: {exc}"
    except UnicodeError as exc:
        return [], f"Unable to decode ARP cache output: {exc}"


# ── Sample devices ─────────────────────────────────────────
DEFAULT_DEVICES = [
    {"id": 1, "name": "Living Room CCTV",  "type": "Camera",     "ip": "192.168.1.10",
     "password": "Weak",   "firmware": "Outdated", "remote": "Enabled",
     "encryption": "Enabled",  "firewall": "Enabled",  "mfa": "Disabled",
     "failed_logins": 6,  "open_ports": 4, "unknown": False, "auto_lock": "Enabled"},
    {"id": 2, "name": "Home Wi-Fi Router", "type": "Router",     "ip": "192.168.1.1",
     "password": "Strong", "firmware": "Updated",  "remote": "Disabled",
     "encryption": "Enabled",  "firewall": "Enabled",  "mfa": "Enabled",
     "failed_logins": 0,  "open_ports": 2, "unknown": False, "auto_lock": "Enabled"},
    {"id": 3, "name": "Smart TV",          "type": "Television", "ip": "192.168.1.20",
     "password": "Strong", "firmware": "Outdated", "remote": "Enabled",
     "encryption": "Disabled", "firewall": "Enabled",  "mfa": "Disabled",
     "failed_logins": 1,  "open_ports": 4, "unknown": False, "auto_lock": "Disabled"},
    {"id": 4, "name": "Smart Door Lock",   "type": "Smart Lock", "ip": "192.168.1.30",
     "password": "Strong", "firmware": "Updated",  "remote": "Disabled",
     "encryption": "Enabled",  "firewall": "Enabled",  "mfa": "Enabled",
     "failed_logins": 0,  "open_ports": 1, "unknown": False, "auto_lock": "Enabled"},
    {"id": 5, "name": "Unknown IoT Device","type": "Other",      "ip": "192.168.1.45",
     "password": "Weak",   "firmware": "Unknown",  "remote": "Enabled",
     "encryption": "Disabled", "firewall": "Disabled", "mfa": "Disabled",
     "failed_logins": 2,  "open_ports": 5, "unknown": True,  "auto_lock": "Disabled"},
]


def initialise():
    if "devices"               not in st.session_state:
        st.session_state.devices = [dict(d) for d in DEFAULT_DEVICES]
    if "latest_results"        not in st.session_state:
        st.session_state.latest_results = []
    if "scan_history"          not in st.session_state:
        st.session_state.scan_history = []
    if "next_id"               not in st.session_state:
        st.session_state.next_id = 6
    if "settings_saved_notice" not in st.session_state:
        st.session_state.settings_saved_notice = False


initialise()


# ── Rule engine ────────────────────────────────────────────
def analyse_device(d):
    findings = []

    def add(rule, severity, points, reason, recommendation):
        findings.append({"Device": d["name"], "Rule": rule, "Severity": severity,
                         "Points": points, "Reason": reason, "Recommendation": recommendation})

    if d["password"] == "Weak":
        add("Weak password policy", "High", 30,
            "The device is configured with a weak password policy.",
            "Configure a strong, unique password.")
    if d["firmware"] in ["Outdated", "Unknown"]:
        add("Firmware review",
            "High" if d["firmware"] == "Outdated" else "Medium",
            25 if d["firmware"] == "Outdated" else 15,
            f"Firmware status is marked {d['firmware'].lower()}.",
            "Verify the installed version and check official vendor updates.")
    if d["remote"] == "Enabled":
        add("Remote access enabled", "Medium", 15,
            "Remote access is enabled in this sample configuration.",
            "Confirm it is needed and restrict access to trusted users.")
    if d["encryption"] == "Disabled":
        add("Encryption disabled", "High", 25,
            "Encryption is marked disabled in this simulation.",
            "Enable supported encryption and secure communication.")
    if d["firewall"] == "Disabled":
        add("Firewall disabled", "High", 25,
            "Firewall protection is marked disabled.",
            "Enable the supported firewall or network protection.")
    if d["mfa"] == "Disabled":
        add("MFA not enabled", "Medium", 10,
            "Multi-factor authentication is not enabled in the sample settings.",
            "Enable MFA if the device or its management account supports it.")
    if d["failed_logins"] >= 5:
        add("Repeated failed logins", "High", 25,
            f"{d['failed_logins']} failed login attempts are recorded in the sample data.",
            "Review authentication logs and verify legitimate access.")
    if d["open_ports"] >= 4:
        add("Open port review", "Medium", 15,
            f"{d['open_ports']} open ports are recorded in the simulation.",
            "Verify which services require these ports and close unnecessary ones.")
    if d["unknown"]:
        add("Unknown device", "High", 30,
            "This device is marked as not yet identified or approved.",
            "Verify the device owner and approve it only if recognised.")
    if d["auto_lock"] == "Disabled":
        add("Auto-lock disabled", "Medium", 10,
            "Automatic locking is marked disabled.",
            "Enable automatic locking if supported and appropriate.")

    score = min(sum(f["Points"] for f in findings), 100)
    level = "High" if score >= 60 else ("Medium" if score >= 30 else "Low")

    if not findings:
        findings = [{"Device": d["name"], "Rule": "No configured rules triggered",
                     "Severity": "Info", "Points": 0,
                     "Reason": "The sample settings did not trigger the configured rules.",
                     "Recommendation": "Continue routine security checks."}]

    cfg_keys = ("password", "firmware", "remote", "encryption", "firewall",
                "mfa", "failed_logins", "open_ports", "unknown", "auto_lock")
    scanned_config = {k: (int(d[k]) if k in ("failed_logins", "open_ports") else
                          (bool(d[k]) if k == "unknown" else d[k])) for k in cfg_keys}

    return {"id": d["id"], "Device": d["name"], "Type": d["type"], "Demo IP": d["ip"],
            "Risk Score": score, "Risk Level": level,
            "Finding Count": sum(f["Severity"] != "Info" for f in findings),
            "Findings": findings, "scanned_config": scanned_config}


def scan_all():
    results = [analyse_device(d) for d in st.session_state.devices]
    now = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    st.session_state.latest_results = results
    st.session_state.scan_history.append({
        "Scan Time": now, "Devices Scanned": len(results),
        "High":   sum(r["Risk Level"] == "High"   for r in results),
        "Medium": sum(r["Risk Level"] == "Medium" for r in results),
        "Low":    sum(r["Risk Level"] == "Low"    for r in results),
        "Findings": sum(r["Finding Count"] for r in results),
    })


def get_current_results():
    latest_by_id = {r["id"]: r for r in st.session_state.latest_results}
    return [latest_by_id.get(d["id"]) or analyse_device(d) for d in st.session_state.devices]


# ── Micro helpers ──────────────────────────────────────────
def bdg(text, cls):
    return f'<span class="bdg bdg-{cls}">{escape(str(text)).upper()}</span>'

def tag(text, cls="neutral"):
    dot = '<span class="tdot"></span>' if cls in ("teal", "green") else ""
    return f'<span class="tag tag-{cls}">{dot}{escape(str(text))}</span>'

def rc(level):
    return {"high": "var(--hi)", "medium": "var(--me)",
            "low": "var(--lo)", "info": "var(--teal)"}.get(level.lower(), "var(--tx3)")

def sbar(score, color):
    return (f'<div class="sw"><div class="st"><div class="sf" style="width:{score}%;'
            f'background:{color};"></div></div><span class="sn">{score}/100</span></div>')


# ── Sidebar ────────────────────────────────────────────────
st.sidebar.markdown("""
<div class="sb-brand">
  <div class="sb-icon">&#x1F6E1;</div>
  <div>
    <span class="sb-name">SMART RISKS</span>
    <span class="sb-sub">Connected Device Security</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sb-sec">Operations</div>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Device Simulator", "Security Findings", "Event History", "Local Network Snapshot"],
    format_func=lambda x: {
        "Overview":               "\u2302  Overview",
        "Device Simulator":       "\u25a6  Device Simulator",
        "Security Findings":      "\u25c8  Security Findings",
        "Event History":          "\u25f7  Event History",
        "Local Network Snapshot": "\u2609  Network Snapshot",
    }[x],
    label_visibility="collapsed",
)

st.sidebar.markdown("""
<div class="sb-mode">
  <div class="sb-mode-hd">
    <span>Operating Mode</span>
    <span style="color:var(--teal);font-size:.62rem;">v2.4</span>
  </div>
  <div class="sb-mode-val"><span class="pdot"></span>Simulation Active</div>
  <div class="sb-mode-desc">Heuristic policy engine. Non-destructive offline assessment.</div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  OVERVIEW
# ═══════════════════════════════════════════════════════════
if page == "Overview":
    results       = get_current_results()
    high          = sum(r["Risk Level"] == "High"   for r in results)
    medium        = sum(r["Risk Level"] == "Medium" for r in results)
    low           = sum(r["Risk Level"] == "Low"    for r in results)
    finding_count = sum(r["Finding Count"]          for r in results)
    avg_score     = sum(r["Risk Score"] for r in results) / max(len(results), 1)
    scan_history  = st.session_state.scan_history
    latest_scan   = scan_history[-1] if scan_history else None

    hdr_l, hdr_r = st.columns([3, 1], gap="small")
    with hdr_l:
        last_t = (f'<span class="tag tag-teal"><span class="tdot"></span>LAST SCAN: '
                  f'{escape(str(latest_scan["Scan Time"]))}</span>' if latest_scan else "")
        st.markdown(f"""
        <div class="ph">
          <div class="ph-l">
            <div class="ph-eye">Security Operations Center &middot; Fleet Intelligence</div>
            <div class="ph-title">Security Overview</div>
            <div class="ph-sub">Connected device risk monitoring and heuristic security assessment.</div>
          </div>
          <div class="ph-r">
            {tag("Engine Active","green")}
            {last_t}
          </div>
        </div>""", unsafe_allow_html=True)
    with hdr_r:
        if st.button("Run assessment", type="primary", use_container_width=True):
            scan_all()
            st.rerun()

    # KPI strip
    kpi_html = (
        f'<div class="kpi-row">'
        f'<div class="kpi kpi-teal"><div class="kpi-lbl">Devices monitored</div><div class="kpi-value">{len(st.session_state.devices)}</div><div class="kpi-ft">100% evaluated</div></div>'
        f'<div class="kpi kpi-hi"><div class="kpi-lbl">High-risk devices</div><div class="kpi-value">{high}</div><div class="kpi-ft">Requires priority remediation</div></div>'
        f'<div class="kpi kpi-med"><div class="kpi-lbl">Medium-risk devices</div><div class="kpi-value">{medium}</div><div class="kpi-ft">Policy review required</div></div>'
        f'<div class="kpi kpi-low"><div class="kpi-lbl">Low-risk devices</div><div class="kpi-value">{low}</div><div class="kpi-ft">Meets security baseline</div></div>'
        f'<div class="kpi kpi-inf"><div class="kpi-lbl">Active findings</div><div class="kpi-value">{finding_count}</div><div class="kpi-ft">Actionable rule items</div></div>'
        f'<div class="kpi kpi-teal"><div class="kpi-lbl">Average risk score</div><div class="kpi-value kpi-value-sm">{avg_score:.1f}<span class="kpi-unit"> / 100</span></div><div class="kpi-ft">Composite fleet risk</div></div>'
        f'</div>'
    )
    st.markdown(kpi_html, unsafe_allow_html=True)

    ranked = sorted(results, key=lambda r: r["Risk Score"], reverse=True)
    col_l, col_r = st.columns([1.4, 1.0], gap="medium")

    # LEFT
    with col_l:
        inv = ""
        for r in ranked:
            rl = r["Risk Level"].lower()
            inv += f"""<tr>
              <td><div class="dn">{escape(r["Device"])}</div><div class="dt">{escape(r["Type"])}</div></td>
              <td><span class="mono">{escape(r["Demo IP"])}</span></td>
              <td>{sbar(r["Risk Score"], rc(rl))}</td>
              <td>{bdg(r["Risk Level"], rl)}</td>
              <td style="text-align:center;font-family:'JetBrains Mono',monospace;font-size:.72rem;">{r["Finding Count"]}</td>
            </tr>"""
        st.markdown(f"""
        <div class="panel">
          <div class="panel-hd">
            <div><div class="panel-t">Device Inventory</div>
              <div class="panel-s">Simulated endpoints &mdash; risk scores &amp; finding counts</div></div>
            {tag(f'{len(results)} Devices')}
          </div>
          <table class="itbl">
            <thead><tr><th>Device / Class</th><th>Simulated IP</th><th>Risk Score</th><th>Severity</th><th>Findings</th></tr></thead>
            <tbody>{inv}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)

        # Remediation Queue
        all_f = [(res, f) for res in results for f in res["Findings"]
                 if f["Severity"] in ("High", "Medium")]
        all_f.sort(key=lambda x: ({"High": 0, "Medium": 1}[x[1]["Severity"]], -x[1]["Points"]))
        pq = ""
        for res, f in all_f[:4]:
            fc = f["Severity"].lower()
            pq += f"""<div class="pi">
              <div class="pi-top"><span class="pi-name">{escape(f["Rule"])}</span>
                {bdg(f'{f["Severity"]} · +{f["Points"]} pts', fc)}</div>
              <div class="pi-sub"><strong style="color:var(--tx);">{escape(res["Device"])}:</strong> {escape(f["Recommendation"])}</div>
            </div>"""
        if not pq:
            pq = '<div class="panel-s" style="padding:6px 0;">No active high or medium findings.</div>'
        st.markdown(f"""
        <div class="panel">
          <div class="panel-hd">
            <div><div class="panel-t">Prioritized Remediation Queue</div>
              <div class="panel-s">Recommended fixes ranked by rule impact</div></div>
          </div>{pq}
        </div>""", unsafe_allow_html=True)

    # RIGHT
    with col_r:
        total = max(len(results), 1)
        dist = ""
        for name, count, color_v in [("High", high, "var(--hi)"), ("Medium", medium, "var(--me)"), ("Low", low, "var(--lo)")]:
            pct = (count / total) * 100
            dist += f"""<div class="dr">
              <span class="dr-lbl">{name}</span>
              <div class="dr-track"><div class="dr-fill" style="width:{pct:.1f}%;background:{color_v};"></div></div>
              <span class="dr-n">{count}</span>
            </div>"""

        devices = st.session_state.devices
        n = len(devices)
        wp  = sum(d["password"] == "Weak"                  for d in devices)
        of  = sum(d["firmware"] in ("Outdated","Unknown")  for d in devices)
        ro  = sum(d["remote"] == "Enabled"                 for d in devices)
        eo  = sum(d["encryption"] == "Disabled"            for d in devices)
        posture = [
            ("Password Policy",   f"{n-wp}/{n} Compliant", "high" if wp > 0 else "low"),
            ("Firmware Currency", f"{n-of}/{n} Updated",   "med"  if of > 0 else "low"),
            ("Network Exposure",  f"{ro} Exposed",          "med"  if ro > 0 else "low"),
            ("Data Encryption",   f"{n-eo}/{n} Enforced",  "high" if eo > 0 else "low"),
        ]
        ps = "".join(
            f'<div class="pr"><span class="pr-lbl">{lbl}</span>{bdg(val, bk)}</div>'
            for lbl, val, bk in posture)
        st.markdown(f"""
        <div class="panel">
          <div class="panel-hd">
            <div><div class="panel-t">Risk Distribution &amp; Posture</div>
              <div class="panel-s">Assessments by severity and rule hygiene</div></div>
            {tag(f'{len(results)} Monitored')}
          </div>
          {dist}
          <div style="margin-top:8px;padding-top:8px;border-top:1px solid var(--b1);">{ps}</div>
        </div>""", unsafe_allow_html=True)

        rk = ""
        for r in ranked[:3]:
            rl = r["Risk Level"].lower()
            rk += f"""<div class="pi">
              <div class="pi-top"><span class="pi-name">{escape(r["Device"])}</span>
                {bdg(f'{r["Risk Level"]} · {r["Risk Score"]}/100', rl)}</div>
              <div class="pi-sub">{escape(r["Type"])} &nbsp;&middot;&nbsp;
                <span class="mono" style="font-size:.65rem;">{escape(r["Demo IP"])}</span>
                &nbsp;&middot;&nbsp; {r["Finding Count"]} finding(s)</div>
            </div>"""
        st.markdown(f"""
        <div class="panel">
          <div class="panel-hd">
            <div><div class="panel-t">Highest Risk Devices</div>
              <div class="panel-s">Priority endpoints ranked by threat score</div></div>
          </div>{rk}
        </div>""", unsafe_allow_html=True)

        act = ""
        for event in reversed(scan_history[-4:]):
            act += f"""<div class="ar">
              <span class="at">{escape(str(event["Scan Time"]))}</span>
              <span class="panel-s">{event["Devices Scanned"]} dev</span>
              <div class="ab">{bdg(f'{event["High"]}H',"high")}{bdg(f'{event["Medium"]}M',"med")}{bdg(f'{event["Low"]}L',"low")}</div>
            </div>"""
        if not act:
            act = '<div class="panel-s" style="padding:6px 0;">No scan events yet. Click &ldquo;Run assessment&rdquo; to begin.</div>'
        st.markdown(f"""
        <div class="panel">
          <div class="panel-hd">
            <div><div class="panel-t">Recent Scan Activity</div>
              <div class="panel-s">Session history &middot; scan timestamps</div></div>
            {tag(f'{len(scan_history)} Scans')}
          </div>{act}
        </div>""", unsafe_allow_html=True)

    st.caption("Simulation only. Risk scores are illustrative rule-based assessments, not verified vulnerabilities or a professional security audit.")


# ═══════════════════════════════════════════════════════════
#  DEVICE SIMULATOR
# ═══════════════════════════════════════════════════════════
elif page == "Device Simulator":
    st.markdown("""
    <div class="ph">
      <div class="ph-l">
        <div class="ph-eye">Simulation Workspace &middot; Configuration Lab</div>
        <div class="ph-title">Device Simulator</div>
        <div class="ph-sub">Configure sample controls and review the rule-based assessment. No real vulnerability scanning is performed.</div>
      </div>
    </div>""", unsafe_allow_html=True)

    names = [d["name"] for d in st.session_state.devices]
    selected_name = st.selectbox("Select simulated device", names)
    device = next(d for d in st.session_state.devices if d["name"] == selected_name)

    st.markdown(f"""
    <div class="dbn">
      <div>
        <div class="dbn-name">{escape(device["name"])}</div>
        <div class="dbn-sub">Category: {escape(device["type"])} &nbsp;&middot;&nbsp; Simulated IP: <span class="mono">{escape(device["ip"])}</span></div>
      </div>
      {tag("Simulated Device","teal")}
    </div>""", unsafe_allow_html=True)

    config_col, assess_col = st.columns([1.3, 1.0], gap="medium")

    with config_col:
        with st.form("device_settings"):
            fl, fr = st.columns(2, gap="medium")
            with fl:
                st.markdown('<div class="grp-title">Authentication</div>', unsafe_allow_html=True)
                password      = st.selectbox("Password policy", ["Weak","Strong"],
                                              index=["Weak","Strong"].index(device["password"]),
                                              help="Tests the password-policy rule; never enter a real password.")
                mfa           = st.selectbox("Multi-factor auth", ["Enabled","Disabled"],
                                              index=["Enabled","Disabled"].index(device["mfa"]))
                failed_logins = st.number_input("Failed logins (sample)", min_value=0, max_value=100,
                                                 value=int(device["failed_logins"]))
                st.markdown('<div class="grp-title">Network Exposure</div>', unsafe_allow_html=True)
                remote        = st.selectbox("Remote access", ["Disabled","Enabled"],
                                              index=["Disabled","Enabled"].index(device["remote"]))
                open_ports    = st.number_input("Open ports (sample)", min_value=0, max_value=100,
                                                 value=int(device["open_ports"]))
            with fr:
                st.markdown('<div class="grp-title">Firmware &amp; Maintenance</div>', unsafe_allow_html=True)
                firmware      = st.selectbox("Firmware status", ["Updated","Outdated","Unknown"],
                                              index=["Updated","Outdated","Unknown"].index(device["firmware"]))
                auto_lock     = st.selectbox("Automatic locking", ["Enabled","Disabled"],
                                              index=["Enabled","Disabled"].index(device["auto_lock"]))
                st.markdown('<div class="grp-title">Security Controls</div>', unsafe_allow_html=True)
                encryption    = st.selectbox("Encryption", ["Enabled","Disabled"],
                                              index=["Enabled","Disabled"].index(device["encryption"]))
                firewall      = st.selectbox("Firewall", ["Enabled","Disabled"],
                                              index=["Enabled","Disabled"].index(device["firewall"]))
                st.markdown('<div class="grp-title">Device Identity</div>', unsafe_allow_html=True)
                unknown       = st.checkbox("Unidentified / not yet approved", value=bool(device["unknown"]))
            saved = st.form_submit_button("Save Settings", type="primary", use_container_width=True)

    if saved:
        device.update({
            "password": password, "firmware": firmware, "remote": remote,
            "encryption": encryption, "firewall": firewall, "mfa": mfa,
            "failed_logins": int(failed_logins), "open_ports": int(open_ports),
            "unknown": unknown, "auto_lock": auto_lock,
        })
        st.session_state.latest_results = []
        st.session_state.settings_saved_notice = True
        st.rerun()

    if st.session_state.pop("settings_saved_notice", False):
        st.markdown('<div class="al al-ok">&#10003;&nbsp; Settings saved. Previous results cleared &mdash; run an assessment to see updated findings.</div>',
                    unsafe_allow_html=True)

    with assess_col:
        st.markdown('<div class="grp-title" style="margin-top:0;">Assessment Telemetry</div>', unsafe_allow_html=True)
        if st.button("Scan Selected Device", type="primary", use_container_width=True):
            result = analyse_device(device)
            st.session_state.latest_results = [
                r for r in st.session_state.latest_results if r["id"] != result["id"]
            ] + [result]
            st.session_state.scan_history.append({
                "Scan Time": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
                "Devices Scanned": 1,
                "High":   int(result["Risk Level"] == "High"),
                "Medium": int(result["Risk Level"] == "Medium"),
                "Low":    int(result["Risk Level"] == "Low"),
                "Findings": result["Finding Count"],
            })
            st.rerun()

        latest = next((r for r in st.session_state.latest_results if r["id"] == device["id"]), None)

        cfg_keys = ("password","firmware","remote","encryption","firewall",
                    "mfa","failed_logins","open_ports","unknown","auto_lock")
        current_cfg = {k: (int(device[k]) if k in ("failed_logins","open_ports") else
                           (bool(device[k]) if k == "unknown" else device[k])) for k in cfg_keys}
        is_outdated = (latest is not None
                       and latest.get("scanned_config") is not None
                       and latest.get("scanned_config") != current_cfg)

        if is_outdated:
            st.markdown("""<div class="al al-warn">
              <span>&#9888;</span>
              <div><strong>Settings Changed:</strong> Configuration modified since last scan. Assessment may be <strong>outdated</strong>. Run &ldquo;Scan Selected Device&rdquo; to re-evaluate.</div>
            </div>""", unsafe_allow_html=True)

        if latest:
            rl    = latest["Risk Level"].lower()
            color = rc(rl)
            bl    = "OUTDATED ASSESSMENT" if is_outdated else f'{latest["Risk Level"].upper()} RISK'
            bc    = "med" if is_outdated else rl
            st.markdown(f"""
            <div class="ac">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:.62rem;font-weight:700;letter-spacing:.1em;color:var(--teal);text-transform:uppercase;">
                  {'&#9888; OUTDATED ASSESSMENT' if is_outdated else 'VERIFIED ASSESSMENT SCORE'}
                </span>
                {bdg(bl, bc)}
              </div>
              <div style="display:flex;align-items:baseline;gap:5px;margin-top:8px;">
                <span class="ac-score">{latest["Risk Score"]}</span>
                <span class="ac-denom">/ 100</span>
              </div>
              <div class="rm"><div class="rm-fill" style="width:{latest["Risk Score"]}%;background:{color};"></div></div>
              <div style="display:flex;justify-content:space-between;font-size:.71rem;color:var(--tx2);">
                <span>Rule findings: <strong style="color:var(--tx);">{latest["Finding Count"]}</strong></span>
                <span>{'Outdated &mdash; rescan needed' if is_outdated else 'Verified current'}</span>
              </div>
            </div>""", unsafe_allow_html=True)

            st.caption("Results apply to the last saved settings.")
            st.markdown('<div class="grp-title">Findings &amp; Recommended Actions</div>', unsafe_allow_html=True)
            for f in latest["Findings"]:
                fc = f["Severity"].lower()
                st.markdown(f"""
                <div class="fc {fc}">
                  <div class="fc-hd">
                    <span class="fc-title">{escape(f["Rule"])}</span>
                    {bdg(f'{f["Severity"]} · +{f["Points"]} pts', fc)}
                  </div>
                  <div class="fc-reason">{escape(f["Reason"])}</div>
                  <div class="fc-reco"><strong>Recommended action:</strong> {escape(f["Recommendation"])}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="panel" style="margin-top:8px;">
              <div class="panel-hd"><div class="panel-t">Assessment Pending</div></div>
              <div class="panel-s">No current assessment for this device. Click <strong>&ldquo;Scan Selected Device&rdquo;</strong> to evaluate rule-based posture.</div>
            </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  SECURITY FINDINGS
# ═══════════════════════════════════════════════════════════
elif page == "Security Findings":
    st.markdown("""
    <div class="ph">
      <div class="ph-l">
        <div class="ph-eye">Threat Intelligence &middot; Rule-Based Findings</div>
        <div class="ph-title">Security Findings</div>
        <div class="ph-sub">Rule-based findings for simulated device configurations. Not verified vulnerabilities.</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.devices:
        all_findings = []
        for result in get_current_results():
            for f in result["Findings"]:
                all_findings.append({
                    "Device": result["Device"], "Device Risk": result["Risk Level"],
                    "Risk Score": result["Risk Score"], "Finding": f["Rule"],
                    "Severity": f["Severity"], "Points": f["Points"],
                    "Reason": f["Reason"], "Recommendation": f["Recommendation"],
                })

        findings_df = pd.DataFrame(all_findings)
        f1, f2, f3  = st.columns([1, 2, 1.2], gap="small", vertical_alignment="bottom")
        severity_filter = f1.multiselect("Severity", ["High","Medium","Low","Info"],
                                          default=["High","Medium","Low","Info"])
        device_filter   = f2.multiselect("Simulated device",
                                          [d["name"] for d in st.session_state.devices],
                                          default=[d["name"] for d in st.session_state.devices])

        filtered = findings_df[
            findings_df["Severity"].isin(severity_filter) &
            findings_df["Device"].isin(device_filter)
        ]
        f3.markdown(
            f'<div style="padding-bottom:4px;">{tag(f"{len(filtered)} / {len(findings_df)} findings", "teal")}</div>',
            unsafe_allow_html=True)

        sev_ord = {"High": 0, "Medium": 1, "Low": 2, "Info": 3}
        filtered = (filtered.assign(_o=filtered["Severity"].map(sev_ord))
                    .sort_values(["_o","Risk Score"], ascending=[True,False])
                    .drop(columns="_o"))

        if filtered.empty:
            st.markdown('<div class="al al-info">&#9432;&nbsp; No findings match the selected filters.</div>',
                        unsafe_allow_html=True)
        else:
            for _, f in filtered.iterrows():
                fc = str(f["Severity"]).lower()
                dr = str(f["Device Risk"]).lower()
                st.markdown(f"""
                <div class="fc {fc}">
                  <div class="fc-hd">
                    <span class="fc-title">{escape(str(f["Finding"]))}</span>
                    {bdg(f'{f["Severity"]} · +{f["Points"]} pts', fc)}
                  </div>
                  <div class="fc-dev">
                    Endpoint: <strong style="color:var(--tx);">{escape(str(f["Device"]))}</strong>
                    &nbsp;&middot;&nbsp; Device Risk: {bdg(f["Device Risk"], dr)}
                    &nbsp;&middot;&nbsp; Score: <strong>{f["Risk Score"]}/100</strong>
                  </div>
                  <div class="fc-reason">{escape(str(f["Reason"]))}</div>
                  <div class="fc-reco"><strong>Recommended remediation:</strong> {escape(str(f["Recommendation"]))}</div>
                </div>""", unsafe_allow_html=True)

        st.write("")
        st.download_button("Download Findings CSV",
                           data=filtered.to_csv(index=False).encode("utf-8"),
                           file_name="smart_risks_findings.csv", mime="text/csv")
    else:
        st.markdown('<div class="al al-info">&#9432;&nbsp; No simulated devices are available to assess.</div>',
                    unsafe_allow_html=True)
        empty_df = pd.DataFrame(columns=["Device","Device Risk","Risk Score","Finding",
                                          "Severity","Points","Reason","Recommendation"])
        st.download_button("Download Findings CSV",
                           data=empty_df.to_csv(index=False).encode("utf-8"),
                           file_name="smart_risks_findings.csv", mime="text/csv")


# ═══════════════════════════════════════════════════════════
#  EVENT HISTORY
# ═══════════════════════════════════════════════════════════
elif page == "Event History":
    st.markdown("""
    <div class="ph">
      <div class="ph-l">
        <div class="ph-eye">Session Audit Trail &middot; Scan Logs</div>
        <div class="ph-title">Event History</div>
        <div class="ph-sub">Scan summaries from this session. History resets on reload.</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="al al-info">
      <span>&#9432;</span>
      <div><strong>Volatile Audit Trail:</strong> Scan events are preserved in active memory only and will reset upon application reload.</div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.scan_history:
        history = pd.DataFrame(st.session_state.scan_history[::-1])
        st.dataframe(history, use_container_width=True, hide_index=True)

        dl_col, clr_col, _ = st.columns([1.2, 1.2, 4], gap="small")
        with dl_col:
            st.download_button("Download Event History CSV",
                               data=history.to_csv(index=False).encode("utf-8"),
                               file_name="smart_risks_event_history.csv",
                               mime="text/csv", use_container_width=True)
        with clr_col:
            if st.button("Clear Event History", use_container_width=True):
                st.session_state.scan_history = []
                st.rerun()
    else:
        st.markdown('<div class="al al-info">&#9432;&nbsp; No scan events yet. Run a scan to begin.</div>',
                    unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  LOCAL NETWORK SNAPSHOT
# ═══════════════════════════════════════════════════════════
elif page == "Local Network Snapshot":
    st.markdown("""
    <div class="ph">
      <div class="ph-l">
        <div class="ph-eye">Observed Network Data &middot; ARP Layer</div>
        <div class="ph-title">Local Network Snapshot</div>
        <div class="ph-sub">Displays entries currently in the Windows ARP cache only. Not a network scan.</div>
      </div>
      <div class="ph-r">""" + tag("Passive OS Read","teal") + """</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="panel">
      <div class="panel-hd">
        <div><div class="panel-t">Layer-2 Cache Diagnostics</div>
          <div class="panel-s">ARP hardware-neighbour mappings from the OS network stack</div></div>
      </div>
      <div style="font-size:.74rem;color:var(--tx2);line-height:1.5;">
        This feature reads local host ARP mappings (<code>arp -a</code>) on Windows.
        These are cached hardware neighbour mappings in the OS network stack,
        strictly distinct from simulated IoT device profiles. No network packets are injected.
      </div>
    </div>""", unsafe_allow_html=True)

    if st.button("Read Windows ARP Cache", type="primary"):
        entries, error = get_local_network_snapshot()
        st.session_state.network_snapshot       = entries
        st.session_state.network_snapshot_error = error

    if "network_snapshot" not in st.session_state:
        st.markdown('<div class="al al-info">&#9432;&nbsp; Read the local ARP cache to view observed entries.</div>',
                    unsafe_allow_html=True)
    elif st.session_state.get("network_snapshot_error"):
        st.error(st.session_state.network_snapshot_error)
    elif st.session_state.network_snapshot:
        st.dataframe(pd.DataFrame(st.session_state.network_snapshot),
                     use_container_width=True, hide_index=True)
        st.caption("Source: Windows ARP cache. Entries are separate from simulated devices.")
    else:
        st.markdown('<div class="al al-info">&#9432;&nbsp; No qualifying IP/MAC entries were present in the Windows ARP cache.</div>',
                    unsafe_allow_html=True)
