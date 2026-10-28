#!/usr/bin/env python3
"""
Holymoly Studio - Antigravity Project Binder
(by Halu Goods Indonesia)

Ensures all project chat sessions initiated from Holymoly Studio
are strictly grouped under the '📁 holymoly_studio' project folder
in Antigravity Desktop rather than floating in general Conversations.
"""

import sqlite3
import json
from pathlib import Path

HOLYMOLY_PROJECT_ID = "4869d63a-9382-4289-ae85-0da46b2f354c"
HOLYMOLY_WORKSPACE_URI = "file:///c%3A/Users/ertyui/ZCodeProject/holymoly_studio"
DB_PATH = Path(r"C:\Users\ertyui\.gemini\antigravity\conversation_summaries.db")

def encode_varint(val: int) -> bytes:
    res = bytearray()
    while val >= 0x80:
        res.append((val & 0x7f) | 0x80)
        val >>= 7
    res.append(val)
    return bytes(res)

def decode_varint(b: bytes, i: int):
    val = 0
    shift = 0
    while True:
        byte = b[i]
        i += 1
        val |= (byte & 0x7f) << shift
        shift += 7
        if not (byte & 0x80):
            break
    return val, i

def patch_raw_summary(blob: bytes, project_id: str, ws_uri: str) -> bytes:
    """Patches protobuf raw_summary blob so Field 17 contains Field 18 (project_id)."""
    if not blob:
        return blob

    i = 0
    fields = []
    try:
        while i < len(blob):
            key, i = decode_varint(blob, i)
            field_num = key >> 3
            wire_type = key & 0x7
            if wire_type == 0:
                start = i
                _, i = decode_varint(blob, i)
                fields.append((field_num, wire_type, blob[start:i]))
            elif wire_type == 2:
                length, i = decode_varint(blob, i)
                val_bytes = blob[i:i+length]
                i += length
                fields.append((field_num, wire_type, val_bytes))
            elif wire_type == 1:
                val_bytes = blob[i:i+8]
                i += 8
                fields.append((field_num, wire_type, val_bytes))
            elif wire_type == 5:
                val_bytes = blob[i:i+4]
                i += 4
                fields.append((field_num, wire_type, val_bytes))
            else:
                break
    except Exception:
        return blob

    out = bytearray()
    for fnum, wtype, val in fields:
        if fnum == 17 and wtype == 2:
            # Modify Field 17 (Cascade Trajectory Summary)
            f17_i = 0
            subfields = []
            try:
                while f17_i < len(val):
                    skey, f17_i = decode_varint(val, f17_i)
                    sf_num = skey >> 3
                    sf_wtype = skey & 0x7
                    if sf_wtype == 0:
                        s_start = f17_i
                        _, f17_i = decode_varint(val, f17_i)
                        subfields.append((sf_num, sf_wtype, val[s_start:f17_i]))
                    elif sf_wtype == 2:
                        slen, f17_i = decode_varint(val, f17_i)
                        sval = val[f17_i:f17_i+slen]
                        f17_i += slen
                        if sf_num == 18:
                            continue  # Replace existing project_id
                        if sf_num == 7 and ws_uri:
                            sval = ws_uri.encode("utf-8")
                        subfields.append((sf_num, sf_wtype, sval))
                    elif sf_wtype == 1:
                        sval = val[f17_i:f17_i+8]
                        f17_i += 8
                        subfields.append((sf_num, sf_wtype, sval))
                    elif sf_wtype == 5:
                        sval = val[f17_i:f17_i+4]
                        f17_i += 4
                        subfields.append((sf_num, sf_wtype, sval))
                    else:
                        break
            except Exception:
                pass

            # Inject project_id into Field 18
            subfields.append((18, 2, project_id.encode("utf-8")))

            # Re-encode Field 17
            f17_out = bytearray()
            for sf_num, sf_wtype, sval in subfields:
                skey = (sf_num << 3) | sf_wtype
                f17_out.extend(encode_varint(skey))
                if sf_wtype == 2:
                    f17_out.extend(encode_varint(len(sval)))
                    f17_out.extend(sval)
                else:
                    f17_out.extend(sval)

            top_key = (17 << 3) | 2
            out.extend(encode_varint(top_key))
            out.extend(encode_varint(len(f17_out)))
            out.extend(f17_out)
        else:
            top_key = (fnum << 3) | wtype
            out.extend(encode_varint(top_key))
            if wtype == 2:
                out.extend(encode_varint(len(val)))
                out.extend(val)
            else:
                out.extend(val)

    return bytes(out)

def bind_conversation(cascade_id: str, title: str = None, project_id: str = HOLYMOLY_PROJECT_ID, ws_uri: str = HOLYMOLY_WORKSPACE_URI) -> bool:
    """Binds a conversation in conversation_summaries.db to holymoly_studio project folder."""
    if not DB_PATH.exists():
        return False

    import time
    for attempt in range(6):
        try:
            conn = sqlite3.connect(str(DB_PATH), timeout=10)
            c = conn.cursor()
            c.execute("SELECT title, raw_summary FROM conversation_summaries WHERE conversation_id = ?", (cascade_id,))
            row = c.fetchone()
            if not row:
                conn.close()
                if attempt < 5:
                    time.sleep(0.3)
                    continue
                return False

            existing_title, raw_summary = row
            new_title = title if title else existing_title
            patched_blob = patch_raw_summary(raw_summary, project_id, ws_uri) if raw_summary else None

            c.execute("""
                UPDATE conversation_summaries
                SET project_id = ?,
                    workspace_uris = ?,
                    title = ?,
                    raw_summary = COALESCE(?, raw_summary)
                WHERE conversation_id = ?
            """, (project_id, json.dumps([ws_uri]), new_title, patched_blob, cascade_id))
            conn.commit()
            conn.close()
            print(f"[ProjectBinder] Successfully bound conversation {cascade_id} to project '{project_id}' (attempt {attempt+1})")
            return True
        except Exception as e:
            if attempt < 5:
                time.sleep(0.3)
                continue
            print(f"[ProjectBinder] Error binding conversation {cascade_id}: {e}")
            return False
    return False

def cleanup_orphaned_test_summaries():
    """Removes orphan / temporary test conversations from conversation_summaries.db."""
    test_ids = [
        "e1a4b6b1-d306-4388-941f-31c075e5e468",
        "c49113c1-cc4e-4f96-ba7a-f52f04bffe84",
        "6c45230a-9413-4f85-b061-ffdc90e7e83d",
        "189ac9d5-7a63-466e-88f6-bdf21fd9bf26",
        "a8d6680c-848b-413b-8a7a-366877e0be40",
    ]
    if not DB_PATH.exists():
        return

    try:
        conn = sqlite3.connect(str(DB_PATH), timeout=10)
        c = conn.cursor()
        for tid in test_ids:
            c.execute("DELETE FROM conversation_summaries WHERE conversation_id = ?", (tid,))
        conn.commit()
        conn.close()
        print(f"[ProjectBinder] Cleaned up orphaned test summaries.")
    except Exception as e:
        print(f"[ProjectBinder] Cleanup error: {e}")

if __name__ == "__main__":
    cleanup_orphaned_test_summaries()
    # Ensure current project 'tes' session (f0ec8678-b188-47ef-8a25-c7671e2a17bc) is bound
    bind_conversation("f0ec8678-b188-47ef-8a25-c7671e2a17bc", title="Tes: Commercial Video Plan")
