
# Zeroing Target Generator CLI

This script generates printable PDF targets for coarse zeroing at constrained distances.
It calculates the expected Point of Impact (POI) offset from your Point of Aim (POA) based on your firearm's zero configuration and barrel length.

---

##  Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

##  Usage

```bash
python zero_target_cli_flex.py --zero <zero_yd> --actual <actual_yd> --barrel <barrel_length> --caliber <caliber> --title "<your title>" --output <file.pdf>
```

###  Required Flags

- `--zero`: Intended zero distance in yards.
- `--actual`: Actual distance you'll shoot at (yardage available).
- `--barrel`: Barrel length in inches.
- `--caliber`: One of: `5.56`, `9mm`, `10mm`, `45acp`, `308`, `300blk`.

 Default grain values are assumed for each caliber.

---

##  Examples

###  9mm – POA = POI at 15 Yards (Standard Pistol Zero)

```bash
python zero_target_cli_flex.py \
  --zero 15 \
  --actual 15 \
  --barrel 4 \
  --caliber 9mm \
  --title "9mm Pistol Zero @ 15 yd" \
  --output 9mm_zero_target.pdf
```

---

###  5.56 – 36 yd Zero @ 25 yd (SBR)

```bash
python zero_target_cli_flex.py \
  --zero 36 \
  --actual 25 \
  --barrel 11.5 \
  --caliber 5.56 \
  --title "SBR 36 yd Zero @ 25 yd" \
  --output sbr_36yd_zero_25yd.pdf
```

---

###  5.56 – 50 yd Zero @ 20 yd (Rifle)

```bash
python zero_target_cli_flex.py \
  --zero 50 \
  --actual 20 \
  --barrel 16 \
  --caliber 5.56 \
  --title "Rifle 50 yd Zero @ 20 yd" \
  --output rifle_50yd_zero_20yd.pdf
```

---

###  .300 Blackout – 50 yd Zero @ 20 yd

```bash
python zero_target_cli_flex.py \
  --zero 50 \
  --actual 20 \
  --barrel 9 \
  --caliber 300blk \
  --title ".300 BLK 50 yd Zero @ 20 yd" \
  --output 300blk_50yd_zero_20yd.pdf
```

---

##  Notes

- Target includes grid, labeled MOA values, POA and POI points.
- Default grain values are hardcoded for simplicity. Override support may be added later.


---

## Disclaimer

This tool is provided as-is with no warranty or guarantee of accuracy. Use at your own risk.

**Bearded Giant** makes no representations or warranties regarding ballistic performance, sighting outcomes, or print accuracy.

Always confirm zero at your intended distance with live fire in a safe, controlled environment.

Stay safe and double-check your setup.

---


MIT License.
