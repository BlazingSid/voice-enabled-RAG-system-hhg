from huggingface_hub import hf_hub_url
import pyarrow.parquet as pq
import fsspec


REPO_ID = "ai4bharat/MSMARCO-XI"
FILE_PATH = "train/martrain.parquet"


def main():
    print("Connecting to MSMARCO-XI...")

    url = hf_hub_url(
        repo_id=REPO_ID,
        filename=FILE_PATH,
        repo_type="dataset"
    )

    with fsspec.open(url, "rb") as f:
        parquet_file = pq.ParquetFile(f)

        print(f"Rows: {parquet_file.metadata.num_rows}")

        print("\nReading first 3 records...\n")

        table = parquet_file.read_row_group(
            0,
            columns=[
                "source_lang",
                "target_lang",
                "query_id",
                "query_type",
                "query",
                "Eng_Query",
                "Answer",
                "Eng_Answer",
                "passages",
            ]
        )

        df = table.to_pandas()

        for index, row in df.head(3).iterrows():
            print("=" * 80)
            print(f"RECORD {index}")
            print("=" * 80)

            print("\nSource language:")
            print(row["source_lang"])

            print("\nTarget language:")
            print(row["target_lang"])

            print("\nQuery ID:")
            print(row["query_id"])

            print("\nQuery type:")
            print(row["query_type"])

            print("\nEnglish query:")
            print(row["Eng_Query"])

            print("\nTranslated query:")
            print(row["query"])

            print("\nEnglish answer:")
            print(row["Eng_Answer"])

            print("\nTranslated answer:")
            print(row["Answer"])

            print("\nPassages:")
            print(row["passages"])


if __name__ == "__main__":
    main()