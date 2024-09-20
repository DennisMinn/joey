import glob
from pathlib import Path
import pandas as pd

TRANSCRIPT_FPATH = "data/dialouge.tsv"
MUGGY_AUDIO_DIR = "data/old_world_blue/nvdlc03muggyvoicesinkmale"
OUTPUT_FPATH = "data/muggy.csv"

if __name__ == "__main__":
    transcript_df = pd.read_csv(TRANSCRIPT_FPATH, sep="\t", encoding="ISO-8859-1")
    transcript_df.columns = transcript_df.columns.str.lower().str.replace(" ", "_")

    prefix_length = len("FormID") + len(" ") + len("01")
    transcript_df["form_id"] = transcript_df["topic_info"].map(lambda topic_info: topic_info[prefix_length:].lstrip("0").lower())
    transcript_df = transcript_df[["response_index", "form_id", "response_text"]]

    muggy_dir = Path(MUGGY_AUDIO_DIR)
    muggy_audio_fpaths = [str(file_path) for file_path in muggy_dir.glob("*.ogg")]

    muggy_df = []
    for file_path in muggy_dir.glob("*.ogg"):
        file_name = file_path.stem
        form_id, response_index = file_name.split("_")[-2:]
        form_id = form_id.lstrip("0")
        response_index = int(response_index) - 1
        
        muggy_df.append((file_path, form_id, response_index))

    muggy_df = pd.DataFrame(muggy_df, columns=["file_path", "form_id", "response_index"])
    muggy_df = pd.merge(muggy_df, transcript_df, on=["form_id", "response_index"], how="left")

    muggy_df.to_csv(OUTPUT_FPATH)