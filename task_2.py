import re
import aiohttp
import matplotlib.pyplot as plt
import asyncio
from functools import reduce


async def fetch_text(url):
    """Asynchronously fetch text from the specified URL."""
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status == 200:
            return await response.text()
        else:
            print(f"Failed to retrieve the text from the URL. Status: {
                  response.status}")
            return ""


async def map_reduce(text_chunk):
    """Map function to count word occurrences in a given text chunk."""
    words = re.findall(r'\b\w+\b', text_chunk.lower())
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count


def reduce_word_counts(word_counts1, word_counts2):
    """Reduce function to merge two dictionaries of word counts."""
    for word, count in word_counts2.items():
        word_counts1[word] = word_counts1.get(word, 0) + count
    return word_counts1


def visualize_top_words(word_freq, top_n=10):
    """Visualize the top N most frequently used words."""
    top_words = sorted(word_freq.items(),
                       key=lambda x: x[1], reverse=True)[:top_n]
    words, counts = zip(*top_words)  # Unpacking words and counts

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequently Used Words')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


async def main(url):
    """Main function to fetch, process, and visualize word frequency from a URL."""
    text = await fetch_text(url)
    if text:
        chunk_size = len(text) // 10
        chunks = [text[i:i + chunk_size]
                  for i in range(0, len(text), chunk_size)]

        mapped_results = await asyncio.gather(*(map_reduce(chunk) for chunk in chunks))
        reduced_result = reduce(reduce_word_counts, mapped_results)
        visualize_top_words(reduced_result)
    else:
        print("No text retrieved from the URL.")

if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    asyncio.run(main(url))
