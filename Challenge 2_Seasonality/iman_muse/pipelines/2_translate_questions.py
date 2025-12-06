"""
Step 2: Translate Questions
- Reads processed dataset from Step 1
- Translates question_content to English (smart translation - only unique texts)
- Output: translated_datakind_dataset.parquet (or test_translated_datakind_dataset.parquet)
"""

import polars as pl
import os
from tqdm import tqdm
from deep_translator import GoogleTranslator
import time
from multiprocessing import Pool, cpu_count
from functools import partial
import argparse

# Configuration
NUM_WORKERS = min(8, cpu_count())
CHUNK_SIZE = 100000  # Larger chunks

LANGUAGE_MAP = {
    'eng': 'en',
    'swa': 'sw',
    'nyn': 'lg',
    'lug': 'lg',
}


def translate_single_text(text, source_lang):
    """Translate single text"""
    try:
        if not text or not str(text).strip():
            return text
        translator = GoogleTranslator(source=source_lang, target='en')
        result = translator.translate(str(text)[:5000])
        time.sleep(0.05)
        return result
    except:
        return text


def translate_texts_parallel(texts, source_lang_code):
    """Parallel translation with progress bar"""
    source_lang = LANGUAGE_MAP.get(source_lang_code, 'auto')

    if source_lang_code == 'eng' or len(texts) == 0:
        return texts

    with Pool(NUM_WORKERS) as pool:
        translate_func = partial(translate_single_text, source_lang=source_lang)
        # Use tqdm to show progress
        results = list(tqdm(
            pool.imap(translate_func, texts),
            total=len(texts),
            desc=f"      Translating {source_lang_code}",
            unit="text",
            ncols=100
        ))

    return results


def translate_unique_texts(df_full):
    """
    SMART TRANSLATION:
    1. Extract unique texts per language
    2. Translate only unique texts
    3. Map translations back
    = MUCH faster! (thousands of translations vs millions)
    """
    print("\n" + "=" * 70)
    print("Step 1: Building Translation Maps")
    print("=" * 70)
    print("\n🚀 Smart Translation: Translating only UNIQUE questions and responses")

    # Get unique question texts per language
    unique_questions = (
        df_full
        .select(['question_language', 'question_content'])
        .unique()
        .filter(pl.col('question_content').is_not_null())
    )

    # Get unique response texts per language
    unique_responses = (
        df_full
        .select(['response_language', 'response_content'])
        .unique()
        .filter(pl.col('response_content').is_not_null())
    )

    q_total = len(unique_questions)
    r_total = len(unique_responses)

    print(f"  Unique question texts: {q_total:,}")
    print(f"  Unique response texts: {r_total:,}")
    print(f"  Total: {q_total + r_total:,}")

    # Create translation dictionaries
    question_translations = {}
    response_translations = {}

    # Translate unique questions
    print("\n  Translating unique questions...")
    for lang in unique_questions['question_language'].unique():
        if not lang or lang == 'eng':
            continue

        texts = unique_questions.filter(pl.col('question_language') == lang)['question_content'].to_list()
        print(f"    {lang}: {len(texts):,} unique texts")

        translated = translate_texts_parallel(texts, lang)

        # Build translation map
        for original, trans in zip(texts, translated):
            question_translations[(lang, original)] = trans

    # Translate unique responses
    print("\n  Translating unique responses...")
    for lang in unique_responses['response_language'].unique():
        if not lang or lang == 'eng':
            continue

        texts = unique_responses.filter(pl.col('response_language') == lang)['response_content'].to_list()
        print(f"    {lang}: {len(texts):,} unique texts")

        translated = translate_texts_parallel(texts, lang)

        # Build translation map
        for original, trans in zip(texts, translated):
            response_translations[(lang, original)] = trans

    print(f"\n✓ Translation maps created!")
    print(f"  Questions: {len(question_translations):,} entries")
    print(f"  Responses: {len(response_translations):,} entries")
    return question_translations, response_translations


def apply_translation_to_chunk(df_chunk, q_trans_map, r_trans_map):
    """Apply translation map to chunk"""

    # Convert to pandas for apply operation
    df_pandas = df_chunk.to_pandas()

    # Map question translations
    def map_question(row):
        if row['question_language'] == 'eng':
            return row['question_content']
        key = (row['question_language'], row['question_content'])
        return q_trans_map.get(key, row['question_content'])

    # Map response translations
    def map_response(row):
        if row['response_language'] == 'eng':
            return row['response_content']
        key = (row['response_language'], row['response_content'])
        return r_trans_map.get(key, row['response_content'])

    df_pandas['eng_question_content'] = df_pandas.apply(map_question, axis=1)
    df_pandas['eng_response_content'] = df_pandas.apply(map_response, axis=1)

    return pl.from_pandas(df_pandas)


def translate_dataset(input_file, output_file):
    """Translate dataset using pre-built translation map"""
    print("\n" + "=" * 70)
    print("Step 2: Applying Translations")
    print("=" * 70)

    # Read full dataset to build translation map
    print("\n📖 Reading dataset to build translation map...")
    df = pl.read_parquet(input_file)
    print(f"  Rows: {len(df):,}")

    # Build translation maps from unique texts
    q_trans_map, r_trans_map = translate_unique_texts(df)

    print(f"\n  Now processing chunks will be INSTANT (just lookup, no API calls!)")
    print(f"\nChunk size: {CHUNK_SIZE:,} rows")

    # Calculate number of chunks
    total_chunks = (len(df) + CHUNK_SIZE - 1) // CHUNK_SIZE

    # Progress bar
    pbar = tqdm(total=total_chunks,
                desc="Applying translations",
                unit="chunk",
                bar_format='{desc}: {percentage:3.0f}%|{bar}| {n}/{total} [{elapsed}<{remaining}]',
                ncols=100)

    chunks_processed = 0
    total_rows = 0

    try:
        first_chunk = True

        for i in range(0, len(df), CHUNK_SIZE):
            try:
                # Get chunk
                chunk = df.slice(i, CHUNK_SIZE)

                # Apply translations
                processed = apply_translation_to_chunk(chunk, q_trans_map, r_trans_map)

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

                pbar.update(1)
                pbar.set_postfix_str(f"{total_rows:,} rows")

            except Exception as e:
                tqdm.write(f"⚠️  Chunk {chunks_processed + 1} error: {str(e)[:100]}")
                continue

    except Exception as e:
        print(f"Error: {e}")
    finally:
        pbar.close()

    print(f"\n✓ Complete! {total_rows:,} rows translated")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="full", choices=["full", "test"], help="Run full or test mode")
    args = parser.parse_args()

    # Get script directory for absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")

    if args.mode == "test":
        input_file = os.path.join(data_dir, "test_pro_datakind_dataset.parquet")
        output_file = os.path.join(data_dir, "test_translated_datakind_dataset.parquet")
        print("\n🧪 TEST MODE: Translating test dataset")
    else:
        input_file = os.path.join(data_dir, "pro_datakind_dataset.parquet")
        output_file = os.path.join(data_dir, "translated_datakind_dataset.parquet")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"\n❌ Error: Input file not found: {input_file}")
        print(f"\nPlease run Step 1 first:")
        print(f"  python 1_process_dataset.py --mode {args.mode}")
        return

    print(f"\nInput: {input_file}")
    print(f"Output: {output_file}")
    print(f"Workers: {NUM_WORKERS}")

    # Translate dataset
    translate_dataset(input_file, output_file)

    print("\n" + "=" * 70)
    print("✓ Step 2 Complete!")
    print("=" * 70)
    print(f"\nOutput: {output_file}")
    print(f"\nTo load in Python:")
    print(f"  import polars as pl")
    print(f"  df = pl.read_parquet('{output_file}')")


if __name__ == "__main__":
    main()
