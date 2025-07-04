
import argparse
import matplotlib.pyplot as plt

# Constants
G = 32.174
INCHES_PER_FOOT = 12
MOA_INCH_100YDS = 1.047

# Velocity estimates by caliber, grain, and barrel length
VELOCITY_TABLE = {
    "5.56": {
        55: {10.5: 2700, 11.5: 2850, 12.5: 2950, 14.5: 3050, 16: 3165, 18: 3200, 20: 3250}
    },
    "9mm": {
        124: {4: 1150, 5: 1200, 8: 1250, 10: 1300, 16: 1350}
    },
    "10mm": {
        180: {4: 1150, 6: 1250, 10: 1350, 16: 1400}
    },
    "45acp": {
        230: {4: 850, 5: 875, 10: 950, 16: 1000}
    },
    "308": {
        147: {16: 2550, 18: 2650, 20: 2700}
    },
    "300blk": {
        110: {9: 2200, 16: 2350},
        220: {9: 1000, 16: 1050}
    }
}

DEFAULT_GRAINS = {
    "5.56": 55,
    "9mm": 124,
    "10mm": 180,
    "45acp": 230,
    "308": 147,
    "300blk": 220
}

def get_velocity(caliber, barrel_length, grain):
    try:
        return VELOCITY_TABLE[caliber][grain][barrel_length]
    except KeyError:
        raise ValueError(f"No velocity data for {caliber} {grain}gr with {barrel_length} barrel.")

def calc_drop_inches(zero_yd, true_yd, barrel_len, grain, caliber):
    velocity = get_velocity(caliber, barrel_len, grain)
    zero_ft = zero_yd * 3
    true_ft = true_yd * 3
    time = true_ft / velocity
    drop_ft = 0.5 * G * time**2
    drop_in = drop_ft * INCHES_PER_FOOT
    zero_time = zero_ft / velocity
    zero_drop_ft = 0.5 * G * zero_time**2
    zero_drop_in = zero_drop_ft * INCHES_PER_FOOT
    offset = drop_in - zero_drop_in
    return round(offset, 2)

def inches_per_moa(yards):
    return MOA_INCH_100YDS * (yards / 100.0)

def create_zeroing_target_auto(
    filename,
    title,
    zero_distance_yd,
    true_distance_yd,
    barrel_length,
    grain,
    caliber,
    page_size=(8.5, 11),
    grid=True,
    moa_labels=True
):
    poi_offset_inches = calc_drop_inches(zero_distance_yd, true_distance_yd, barrel_length, grain, caliber)
    fig, ax = plt.subplots(figsize=page_size)

    center_x = page_size[0] / 2
    center_y = page_size[1] / 2

    if grid:
        for y in range(0, int(page_size[1]) + 1):
            ax.axhline(y=y, color='lightgray', linewidth=0.8)
            if moa_labels:
                moa_val = (y - center_y) / inches_per_moa(true_distance_yd)
                if abs(moa_val) > 0.1:
                    ax.text(page_size[0] - 0.1, y, f"{-moa_val:.1f} MOA", va='center', ha='right', fontsize=7)

        for x in range(0, int(page_size[0]) + 1):
            ax.axvline(x=x, color='lightgray', linewidth=0.8)
            if moa_labels:
                moa_val = (x - center_x) / inches_per_moa(true_distance_yd)
                if abs(moa_val) > 0.1:
                    ax.text(x, page_size[1] - 0.2, f"{moa_val:.1f}", ha='center', fontsize=7)

    bull = plt.Circle((center_x, center_y), 0.15, color='black')
    ax.add_patch(bull)
    ax.text(center_x, center_y + 0.3, 'Point of Aim (POA)', ha='center', fontsize=9)

    poi_y = center_y - poi_offset_inches
    poi = plt.Circle((center_x, poi_y), 0.15, color='red')
    ax.add_patch(poi)
    ax.text(center_x, poi_y - 0.3, f'Expected POI at {true_distance_yd} yd (~{poi_offset_inches}" low)',
            ha='center', color='red', fontsize=8)

    note = f"Zero to {zero_distance_yd} yd • {barrel_length}\" barrel • {grain}gr • {caliber.upper()}"
    ax.text(center_x, center_y + (page_size[1] * 0.38), note, ha='center', fontsize=10, style='italic')

    ax.set_xlim(0, page_size[0])
    ax.set_ylim(0, page_size[1])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12, pad=12)

    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"✅ Target saved to: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a zeroing target with calculated POI offset.")
    parser.add_argument("--zero", type=float, required=True, help="Zero distance in yards (e.g. 36)")
    parser.add_argument("--actual", type=float, required=True, help="Actual shooting distance in yards (e.g. 25)")
    parser.add_argument("--barrel", type=float, required=True, help="Barrel length in inches (e.g. 11.5)")
    parser.add_argument("--caliber", type=str, required=True, choices=VELOCITY_TABLE.keys(), help="Caliber (e.g. 5.56, 9mm, 300blk)")
    parser.add_argument("--title", type=str, default="Custom Zeroing Target", help="Title for the target")
    parser.add_argument("--output", type=str, default="zero_target.pdf", help="Output PDF filename")

    args = parser.parse_args()
    grain = DEFAULT_GRAINS[args.caliber]

    create_zeroing_target_auto(
        filename=args.output,
        title=args.title,
        zero_distance_yd=args.zero,
        true_distance_yd=args.actual,
        barrel_length=args.barrel,
        grain=grain,
        caliber=args.caliber
    )
