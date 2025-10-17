from datetime import datetime
import hashlib
import os

def verify_license():
    # Fixed path to the license file
    license_path = r"C:\ProgramData\license\WT_license.key"

    if not os.path.exists(license_path):
        return False, f"❌ License file not found at:\n{license_path}"

    try:
        with open(license_path, "r") as f:
            lines = f.read().splitlines()
            if len(lines) < 3:
                return False, "❌ Invalid license file format."

            user = lines[0].strip()
            license_code = lines[1].strip()
            expiry_str = lines[2].strip()
    except:
        return False, "❌ Failed to read license file."

    # Check expiration date
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        if today > expiry_date:
            return False, f"❌ License expired on {expiry_date}."
    except:
        return False, "❌ Invalid expiration date format."

    # Validate license code
    secret = "okapi"  # Must match the generator
    expected_code = hashlib.sha256(f"{user}{secret}".encode()).hexdigest()[:16]

    if license_code != expected_code:
        return False, "❌error code:0x00000001."

    return True, f"✅ License verified: {user}, valid until {expiry_date}."
