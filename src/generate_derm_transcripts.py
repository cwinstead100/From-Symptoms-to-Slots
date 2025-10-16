#Generate synthetic data
import csv
import random
import argparse
from typing import List

def clamp_int(x, lo, hi):
    return max(lo, min(hi, int(round(x))))

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic dermatology patient transcripts (short 2–3 sentences).")
    parser.add_argument("--n", type=int, default=10000, help="Number of records to generate (default: 10000)")
    parser.add_argument("--out", type=str, default="short_derm_transcripts_10k.csv", help="Output CSV path")
    parser.add_argument("--seed", type=int, default=7, help="Random seed for reproducibility (default: 7)")
    args = parser.parse_args()

    random.seed(args.seed)

    conditions: List[str] = [
        "acne", "atopic_dermatitis", "psoriasis", "rosacea", "tinea_corporis",
        "tinea_pedis", "onychomycosis", "impetigo", "folliculitis", "contact_dermatitis",
        "urticaria", "scabies", "shingles", "cellulitis", "molluscum", "warts",
        "vitiligo", "cold_sore", "actinic_keratosis", "basal_cell_carcinoma",
        "squamous_cell_carcinoma", "melanoma"
    ]

    body_sites = [
        "face", "forehead", "cheeks", "nose", "chin", "neck", "scalp", "upper back", "lower back",
        "chest", "abdomen", "shoulders", "upper arm", "forearm", "wrist", "hand", "fingers",
        "thigh", "calf", "ankle", "foot", "toes", "groin", "buttock", "armpit"
    ]

    durations = [
        "today", "yesterday", "two days", "three days", "about a week", "ten days",
        "two weeks", "about a month", "six weeks", "two months", "three months",
        "about a year", "several years"
    ]

    itch_words = ["itchy", "super itchy", "maddening itch", "itch that comes and goes"]
    pain_words = ["tender", "sore", "stinging", "burning"]
    discharge_words = ["oozing", "weeping", "crusty", "bleeding"]
    color_words = ["red", "pink", "flesh-colored", "brown", "dark brown", "black", "pearly", "waxy", "purple", "white"]
    size_words = ["tiny", "small", "pea-sized", "quarter-sized", "bigger than a pencil eraser", "about 1 cm", "about 2 cm"]
    texture_words = ["rough", "scaly", "flaky", "raised", "flat", "bumpy", "nodular"]
    self_treatments = ["over-the-counter hydrocortisone", "antifungal cream", "benzoyl peroxide wash", "salicylic acid pads", "tea tree oil", "antihistamines", "ice", "aloe", "nothing yet", "antibiotic ointment"]

    condition_cues = {
        "acne": ["whiteheads", "blackheads", "pimples", "cystic bumps"],
        "atopic_dermatitis": ["itchy patches", "behind knees", "elbow creases", "worse with soaps"],
        "psoriasis": ["thick scaly plaques", "elbows", "knees", "silvery scale"],
        "rosacea": ["facial flushing", "visible blood vessels", "triggers by heat or wine"],
        "tinea_corporis": ["ring-shaped", "central clearing", "itchy rash"],
        "tinea_pedis": ["athlete's foot", "between toes", "peeling"],
        "onychomycosis": ["yellow thick toenail", "crumbly nail"],
        "impetigo": ["honey-colored crust", "around nose and mouth"],
        "folliculitis": ["pimple-like bumps around hairs", "after shaving"],
        "contact_dermatitis": ["after new soap", "after nickel jewelry", "after poison ivy"],
        "urticaria": ["hives", "welts", "move around"],
        "scabies": ["worse at night", "burrows", "between fingers"],
        "shingles": ["band of blisters", "on one side", "burning pain"],
        "cellulitis": ["warm red area", "spreading", "fever"],
        "molluscum": ["small pearly bumps", "center dimple"],
        "warts": ["rough bumps", "on fingers or feet"],
        "vitiligo": ["white patches", "loss of pigment"],
        "cold_sore": ["tingling lip blister", "recurrent"],
        "actinic_keratosis": ["scaly rough spot", "sun exposed", "precancer"],
        "basal_cell_carcinoma": ["pearly bump", "bleeds easily", "non-healing"],
        "squamous_cell_carcinoma": ["scaly sore", "thick crust", "sun exposed"],
        "melanoma": ["asymmetry", "irregular border", "color variegation", "new dark mole"]
    }

    def make_short_transcript(cond, site, dur, itch, pain, discharge, color, size, texture, self_tx):
        # 2–3 concise sentences; avoid newlines within cells
        s1 = f"I noticed a {size} {color} {texture} spot on my {site} {dur} ago."
        s2_bits = [f"It feels {itch}"]
        if random.random() < 0.5:
            s2_bits.append(f"sometimes {pain}")
        if random.random() < 0.35:
            s2_bits.append(f"with a bit of {discharge}")
        s2 = ", ".join(s2_bits) + "."
        s3_options = []
        if cond in condition_cues and random.random() < 0.7:
            s3_options.append("I also noticed " + random.choice(condition_cues[cond]) + ".")
        if random.random() < 0.7:
            s3_options.append(f"I tried {self_tx} with limited relief.")
        s3 = random.choice(s3_options) if s3_options else "It hasn't really changed much."
        return f"{s1} {s2} {s3}" if random.random() < 0.55 else f"{s1} {s2}"

    # Prepare CSV
    fieldnames = ["id", "transcript", "suspected_condition_label", "red_flags", "severity_0_10"]
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, args.n + 1):
            cond = random.choice(conditions)
            site = random.choice(body_sites)
            dur = random.choice(durations)
            sev = clamp_int(random.gauss(5, 2), 0, 10)
            itch = random.choice(itch_words)
            pain = random.choice(pain_words)
            discharge = random.choice(discharge_words)
            color = random.choice(color_words)
            size = random.choice(size_words)
            texture = random.choice(texture_words)
            self_tx = random.choice(self_treatments)

            red_flags = []
            if cond in ["melanoma", "basal_cell_carcinoma", "squamous_cell_carcinoma"] and random.random() < 0.7:
                red_flags.append("non_healing")
            if cond == "melanoma" and random.random() < 0.8:
                red_flags.extend(["asymmetry", "irregular_border", "color_variegation", "evolving"])
            if cond == "cellulitis" and random.random() < 0.6:
                red_flags.append("fever_reported")

            transcript = make_short_transcript(cond, site, dur, itch, pain, discharge, color, size, texture, self_tx)
            writer.writerow({
                "id": i,
                "transcript": transcript,
                "suspected_condition_label": cond,
                "red_flags": ";".join(red_flags) if red_flags else "",
                "severity_0_10": sev
            })

    print(f"Wrote {args.n} records to {args.out}")

if __name__ == "__main__":
    main()
