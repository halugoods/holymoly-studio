"""
Phonetic Sanitizer Engine for HolyMoly Studio (Gemini Native Audio TTS)
Ensures authentic Indonesian pronunciation of English/Tech loanwords in Gemini TTS.
Critical Rule: Subtitles remain grammatically correct; only TTS audio input is phonetically modified.
"""

import re

PHONETIC_DICTIONARY = [
    # Payment & Financial terms
    (r"\bQRIS\b", "Kris"),
    (r"\bqris\b", "kris"),
    (r"\bQris\b", "Kris"),
    (r"\btap\b", "tep"),
    (r"\bTap\b", "Tep"),
    (r"\bTAP\b", "Tep"),
    (r"\bscan\b", "sken"),
    (r"\bScan\b", "Sken"),
    (r"\bscanning\b", "skening"),
    (r"\bScanning\b", "Skening"),
    (r"\bcashless\b", "kesles"),
    (r"\bCashless\b", "Kesles"),
    (r"\bcheckout\b", "cek-out"),
    (r"\bCheckout\b", "Cek-out"),
    
    # Tech & Software terms
    (r"\brealtime\b", "ril-taim"),
    (r"\bRealtime\b", "Ril-taim"),
    (r"\breal-time\b", "ril-taim"),
    (r"\bReal-time\b", "Ril-taim"),
    (r"\bonline\b", "onlain"),
    (r"\bOnline\b", "Onlain"),
    (r"\boffline\b", "oflain"),
    (r"\bOffline\b", "Oflain"),
    (r"\bupdate\b", "apdet"),
    (r"\bUpdate\b", "Apdet"),
    (r"\bcloud\b", "klowd"),
    (r"\bCloud\b", "Klowd"),
    (r"\bserver\b", "server"),
    (r"\bdatabase\b", "detabes"),
    (r"\bDatabase\b", "Detabes"),
    (r"\bbackup\b", "bek-ap"),
    (r"\bBackup\b", "Bek-ap"),
    (r"\bsync\b", "sink"),
    (r"\bSync\b", "Sink"),
    (r"\bvoucher\b", "vowcer"),
    (r"\bVoucher\b", "Vowcer"),
    (r"\bgadget\b", "gejet"),
    (r"\bGadget\b", "Gejet"),
    (r"\bpreview\b", "privyu"),
    (r"\bPreview\b", "Privyu"),
    (r"\bscreen\b", "skrin"),
    (r"\bScreen\b", "Skrin"),
    (r"\bprinter\b", "printer"),
    (r"\bthermal\b", "termal"),
    (r"\bThermal\b", "Termal"),
    (r"\bbluetooth\b", "blutut"),
    (r"\bBluetooth\b", "Blutut"),
]

def sanitize_for_tts(text: str) -> str:
    """
    Replaces terms that Gemini TTS mispronounces with Indonesian phonetic spellings.
    Examples:
      'Bayar pakai QRIS, cukup tap di kasir realtime'
      -> 'Bayar pakai Kris, cukup tep di kasir ril-taim'
    """
    if not text:
        return ""
    
    sanitized = text
    for pattern, replacement in PHONETIC_DICTIONARY:
        sanitized = re.sub(pattern, replacement, sanitized)
    
    return sanitized

if __name__ == "__main__":
    test_phrase = "Pakai fitur QRIS dan cukup tap di HP untuk checkout realtime. Semua data sinkron ke cloud secara offline maupun online."
    print("Original :", test_phrase)
    print("Sanitized:", sanitize_for_tts(test_phrase))
