"""
Step 1: Process Dataset - Deduplication & Weather Join
- Deduplicates on question_id
- Joins weather data by year-month and country
- Output: pro_datakind_dataset.parquet (or test_pro_datakind_dataset.parquet)
"""

import polars as pl
import os
from tqdm import tqdm
import argparse

# Configuration
CHUNK_SIZE = 100000  # Larger chunks


def get_weather_data():
    """Load weather data from existing CSV files"""
    print("\n" + "=" * 70)
    print("Step 1: Loading Weather Data")
    print("=" * 70)

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Load existing weather data files
    weather_dir = os.path.join(script_dir, "..", "..", "ibrahim-yucel", "weather-data")

    print("\nLoading weather files...")
    ken = pl.read_csv(f"{weather_dir}/KEN_weather_data.csv")
    uga = pl.read_csv(f"{weather_dir}/UGA_weather_data.csv")
    tza = pl.read_csv(f"{weather_dir}/TZA_weather_data.csv")

    # Add country codes
    ken = ken.with_columns(pl.lit('KE').alias('country'))
    uga = uga.with_columns(pl.lit('UG').alias('country'))
    tza = tza.with_columns(pl.lit('TZ').alias('country'))

    # Combine all countries
    weather = pl.concat([ken, uga, tza])

    print(f"  Kenya: {len(ken):,} months")
    print(f"  Uganda: {len(uga):,} months")
    print(f"  Tanzania: {len(tza):,} months")
    print(f"  Total: {len(weather):,} records")

    # Rename columns to match expected schema
    weather = weather.rename({
        'index': 'year_month',
        'avg_max_temp': 'temp_max_c',
        'avg_min_temp': 'temp_min_c',
        'precipitation': 'precipitation_mm'
    })

    # Calculate average temperature
    weather = weather.with_columns([
        ((pl.col('temp_max_c') + pl.col('temp_min_c')) / 2.0).alias('temp_avg_c')
    ])

    # Select relevant columns
    weather = weather.select([
        'year_month',
        'country',
        'temp_max_c',
        'temp_min_c',
        'temp_avg_c',
        'precipitation_mm',
        'relative_humidity'
    ])

    print(f"\n✓ Weather data loaded: {len(weather):,} records")
    print(f"   Date range: {weather['year_month'].min()} to {weather['year_month'].max()}")

    return weather


def process_chunk(df_chunk, weather_df):
    """Process chunk - add weather data only"""

    # Extract year-month from question_sent and normalize country code
    df_chunk = df_chunk.with_columns([
        # Extract YYYY-MM from the datetime string (first 7 characters)
        pl.col('question_sent').str.slice(0, 7).alias('year_month'),
        # Uppercase the country code to match weather data
        pl.col('question_user_country_code').str.to_uppercase().alias('country_upper')
    ])

    # Merge weather data (LEFT JOIN on year-month)
    df_chunk = df_chunk.join(
        weather_df,
        left_on=['year_month', 'country_upper'],
        right_on=['year_month', 'country'],
        how='left'
    )

    # Drop temp columns
    cols_to_drop = [col for col in ['year_month', 'country', 'country_upper'] if col in df_chunk.columns]
    if cols_to_drop:
        df_chunk = df_chunk.drop(cols_to_drop)

    return df_chunk


def process_dataset(weather_df, input_file, output_file, mode='full'):
    """Process dataset using Polars streaming"""
    print("\n" + "=" * 70)
    print("Step 2: Drop Duplicates & Join Weather Data")
    print("=" * 70)

    # FIRST: Drop duplicates on question_id AND response_id
    print("\nDropping duplicates (subset: question_id, response_id)...")

    # Get script directory for relative paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    temp_deduped_file = os.path.join(data_dir, 'datakind_dataset_deduped.csv')

    # Read dataset (limited rows in test mode)
    if mode == 'test':
        print("🧪 TEST MODE: Reading only first 500 rows")
        df = pl.read_csv(input_file, n_rows=500)
    else:
        print("📖 Reading full dataset...")
        df = pl.read_csv(input_file, low_memory=True)
    original_count = len(df)
    print(f"  Original rows: {original_count:,}")

    # Drop duplicates on question_id AND response_id
    print("  Deduplicating...")
    df_deduped = df.unique(subset=['question_id', 'response_id'], keep='first')
    deduped_count = len(df_deduped)
    duplicates_removed = original_count - deduped_count

    print(f"  After dedup: {deduped_count:,}")
    print(f"  Removed: {duplicates_removed:,} duplicates ({duplicates_removed/original_count*100:.1f}%)")

    # Save deduplicated dataset
    print(f"  Saving to: {temp_deduped_file}")
    df_deduped.write_csv(temp_deduped_file)
    print(f"  ✓ Saved")

    # Now process the deduplicated file
    input_file = temp_deduped_file

    print(f"\nChunk size: {CHUNK_SIZE:,} rows")

    # Estimate chunks based on deduplicated file
    file_size = os.path.getsize(input_file)
    estimated_chunks = int(file_size / (CHUNK_SIZE * 350))

    # Progress bar
    pbar = tqdm(total=estimated_chunks,
                desc="Processing chunks",
                unit="chunk",
                bar_format='{desc}: {percentage:3.0f}%|{bar}| {n}/{total} [{elapsed}<{remaining}]',
                ncols=100)

    chunks_processed = 0
    total_rows = 0

    try:
        # Read entire deduped file (it's already small after dedup)
        df_full = pl.read_csv(input_file, low_memory=True)
        total_rows_to_process = len(df_full)

        print(f"  Total rows to process: {total_rows_to_process:,}")

        # Update progress bar total
        pbar.total = (total_rows_to_process + CHUNK_SIZE - 1) // CHUNK_SIZE
        pbar.refresh()

        first_chunk = True
        row_offset = 0

        while row_offset < total_rows_to_process:
            try:
                # Get chunk slice
                chunk_end = min(row_offset + CHUNK_SIZE, total_rows_to_process)
                batch = df_full.slice(row_offset, chunk_end - row_offset)

                if len(batch) == 0:
                    break

                # Process chunk - add weather data
                processed = process_chunk(batch, weather_df)

                # Write to Parquet
                if first_chunk:
                    processed.write_parquet(output_file, compression='snappy')
                    first_chunk = False
                else:
                    # Append mode
                    existing = pl.read_parquet(output_file)
                    combined = pl.concat([existing, processed])
                    combined.write_parquet(output_file, compression='snappy')

                chunks_processed += 1
                total_rows += len(processed)
                row_offset = chunk_end

                pbar.update(1)
                pbar.set_postfix_str(f"{total_rows:,} rows")

            except Exception as e:
                tqdm.write(f"⚠️  Chunk {chunks_processed + 1} error: {str(e)[:100]}")
                row_offset += CHUNK_SIZE
                continue

    except Exception as e:
        print(f"Error: {e}")
    finally:
        pbar.close()

    print(f"\n✓ Complete! {total_rows:,} rows processed")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="full", choices=["full", "test"], help="Run full or test mode")
    args = parser.parse_args()

    # Get script directory for absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    root_dir = os.path.join(script_dir, "..", "..", "..")

    # Create data directory if needed
    os.makedirs(data_dir, exist_ok=True)

    if args.mode == "test":
        input_file = os.path.join(root_dir, "datakind_dataset.csv")
        output_file = os.path.join(data_dir, "test_pro_datakind_dataset.parquet")
        print("\n🧪 TEST MODE: Processing first 500 rows only")
    else:
        input_file = os.path.join(root_dir, "datakind_dataset.csv")
        output_file = os.path.join(data_dir, "pro_datakind_dataset.parquet")

    # Step 1: Weather
    weather_df = get_weather_data()
    if weather_df is None:
        return

    # Step 2: Process
    process_dataset(weather_df, input_file, output_file, mode=args.mode)

    print("\n" + "=" * 70)
    print("✓ Step 1 Complete!")
    print("=" * 70)
    print(f"\nOutput: {output_file}")
    print(f"\nNext step: Run translation with:")
    print(f"  python 2_translate_questions.py --mode {args.mode}")


if __name__ == "__main__":
    main()
