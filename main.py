import time

# Pre-defined master chemical fingerprint of the physical key (Simulated Wavelength Wavenumbers)
MASTER_CHEMICAL_PROFILE = [405.0, 520.0, 680.0]

# Rolling memory buffer to store only the last 4 consecutive scans 
SCAN_HISTORY = []
MAX_HISTORY_LENGTH = 4

def calculate_spectral_match(current_scan, master_profile):
    """
    Compares the incoming key data against the master profile.
    Returns a decimal percentage match accuracy.
    """
    total_error = 0
    for i in range(len(master_profile)):
        total_error += abs(current_scan[i] - master_profile[i]) / master_profile[i]
    return 1.0 - (total_error / len(master_profile))

def verify_scan(incoming_scan_data):
    """
    Core security validation logic running on the Raspberry Pi Pico brain.
    """
    global SCAN_HISTORY
    print(f"\n[SYSTEM] Scanning key... Analyzing wave pattern: {incoming_scan_data}")
    time.sleep(0.8) # Simulate hardware processing delay

    # STEP 1: Anti-Replay Detection (Zero-Entropy Variance check)
    # In nature, two analog scans are NEVER 100.00% perfectly identical due to micro-noise.
    if incoming_scan_data in SCAN_HISTORY:
        print("\n!!! CRITICAL SECURITY ALERT !!!")
        print("[ALERT]: Zero-Entropy Variance Detected!")
        print("[ALERT]: Incoming digital stream is 100.00% perfectly identical to a prior scan.")
        print("[ACTION]: Digital injection/replay attack confirmed. System Lockdown Initialized.")
        return False

    # STEP 2: Chemical Fingerprint Validation
    match_accuracy = calculate_spectral_match(incoming_scan_data, MASTER_CHEMICAL_PROFILE)
    print(f"[ANALYSIS]: Spectrometry match accuracy verified at: {match_accuracy * 100:.2f}%")

    if match_accuracy >= 0.99:
        print("\n[SUCCESS]: Physical Presence & Chemical Identity Authenticated.")
        print("[ACTION]: Sending 5V logic signal to MOSFET switch -> 12V Solenoid Deadbolt OPEN.")
        
        # Keep track of this scan to prevent it from being used again immediately
        SCAN_HISTORY.append(incoming_scan_data)
        
        # Strictly maintain the rolling history window by removing the oldest scan data
        if len(SCAN_HISTORY) > MAX_HISTORY_LENGTH:
            SCAN_HISTORY.pop(0)
            
        print(f"[DATA INTEGRITY]: Volatile memory purged. Active history limited to last {len(SCAN_HISTORY)} entries.")
        return True
    else:
        print("\n[ACCESS DENIED]: Invalid Chemical Wavelength Profile.")
        return False

# ==========================================================
# SIMULATED SYSTEM TEST VECTORS
# ==========================================================
if __name__ == "__main__":
    print("--- STARTING SPECTRO-SECURE TERMINAL OPERATIONAL RUN ---")
    
    # Run 1: Legitimate user scans the physical key. 
    # It has natural physical micro-variations (405.02 instead of 405.0) due to analog noise.
    real_user_scan = [405.02, 520.01, 679.98]
    print("\n>>> Scenario A: Valid User Access Attempt")
    verify_scan(real_user_scan)
    
    # Run 2: An intruder plays back the EXACT digital signature captured by a probe.
    # It arrives with 100.00% absolute mathematical perfection.
    intruder_replay_packet = [405.02, 520.01, 679.98]
    print("\n>>> Scenario B: Intruder Replay Hacking Attempt")
    verify_scan(intruder_replay_packet)
