#!/usr/bin/env python3
"""
Generate a ZIP archive whose flag is hidden in an unusual location.

The archive contains several mundane corporate documents. The flag itself is
NOT in any of the files — it is base64-encoded and stored in the archive's
end-of-central-directory comment field, preceded by a label that looks like
a version or build string to reduce suspicion.

Players who open the archive normally see only the decoy files. The flag is
discovered via:
  - hex editor inspection of the end of the ZIP
  - Python: zipfile.ZipFile('challenge.zip').comment
  - CLI: zipnote challenge.zip  (or  unzip -z challenge.zip)
  - xxd / strings: looking for the EOCD comment at offset -22
"""
import base64
import io
import os
import zipfile

DECOY_FILES = {
    'meeting_notes_q3.txt': (
        b'Q3 Planning Session - Internal Notes\n'
        b'=====================================\n'
        b'Attendees: A. Johnson, B. Smith, C. Williams, D. Brown\n\n'
        b'Action items:\n'
        b'  - AJ: finalise budget forecast by EOW\n'
        b'  - BS: update backend API docs\n'
        b'  - CW: complete UI prototype\n'
        b'  - DB: review infra DR plan\n\n'
        b'Next sync: Thursday 10:00 AEDT\n'
    ),
    'team_roster.csv': (
        b'name,role,team,start_date\n'
        b'Alice Johnson,Lead Engineer,Backend,2021-03-15\n'
        b'Bob Smith,Senior Developer,Backend,2020-09-01\n'
        b'Carol Williams,Frontend Developer,Web,2022-01-10\n'
        b'David Brown,DevOps Engineer,Infra,2019-06-20\n'
        b'Eve Davis,Product Manager,Product,2023-02-28\n'
    ),
    'budget_summary.txt': (
        b'FY 2025 Budget Summary\n'
        b'======================\n'
        b'Engineering:  $620,000\n'
        b'Marketing:    $350,000\n'
        b'Operations:   $180,000\n'
        b'Total:      $1,150,000\n\n'
        b'Status: Approved - pending CFO sign-off\n'
    ),
    'patch_log.txt': (
        b'Patch Log\n'
        b'---------\n'
        b'2025-10-01  Updated authentication middleware\n'
        b'2025-09-22  Rotated TLS certificates\n'
        b'2025-09-15  Deployed security hotfix v1.2.3\n'
        b'2025-08-30  Upgraded dependencies\n'
    ),
}


def main():
    flag = os.environ.get('FLAG', 'CSEC{placeholder_change_me}')
    out  = os.environ.get('OUTPUT', '/data/challenge.zip')
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)

    # Encode flag as base64 and embed in a comment that looks like metadata
    b64_flag    = base64.b64encode(flag.encode()).decode()
    archive_comment = f'INTERNAL // BUILD: 20251015 // REV: {b64_flag}'.encode()

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.comment = archive_comment
        for name, content in DECOY_FILES.items():
            zf.writestr(name, content)

    buf.seek(0)
    with open(out, 'wb') as f:
        f.write(buf.read())

    print(f'Generated {out}  ({len(DECOY_FILES)} decoy files, comment length {len(archive_comment)})')
    print(f'Flag is base64-encoded in the archive comment after "REV: "')


if __name__ == '__main__':
    main()
