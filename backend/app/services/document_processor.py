"""
Document processing service for ingesting and chunking book content.
"""
import os
import re
import hashlib
from typing import List, Dict, Tuple
from pathlib import Path
import markdown
from bs4 import BeautifulSoup


class DocumentChunk:
    """Represents a chunk of text from a document."""

    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        chunk_index: int,
        text: str,
        metadata: Dict
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.chunk_index = chunk_index
        self.text = text
        self.metadata = metadata


class DocumentProcessor:
    """Process markdown documents into chunks for embedding."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.md = markdown.Markdown(extensions=['meta', 'tables', 'fenced_code'])

    def extract_metadata_from_frontmatter(self, content: str) -> Tuple[Dict, str]:
        """Extract YAML frontmatter metadata from markdown."""
        frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(frontmatter_pattern, content, re.DOTALL)

        metadata = {}
        clean_content = content

        if match:
            frontmatter = match.group(1)
            clean_content = content[match.end():]

            # Parse simple YAML frontmatter
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

        return metadata, clean_content

    def markdown_to_text(self, md_content: str) -> str:
        """Convert markdown to plain text."""
        # Convert markdown to HTML
        html = self.md.convert(md_content)

        # Extract text from HTML
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def chunk_text(self, text: str, doc_id: str, metadata: Dict) -> List[DocumentChunk]:
        """Split text into overlapping chunks."""
        chunks = []
        words = text.split()

        chunk_index = 0
        start = 0

        while start < len(words):
            # Get chunk of words
            end = min(start + self.chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)

            # Create chunk ID
            chunk_hash = hashlib.md5(chunk_text.encode()).hexdigest()[:16]
            chunk_id = f"{doc_id}_chunk_{chunk_index}_{chunk_hash}"

            # Create chunk metadata
            chunk_metadata = {
                **metadata,
                'chunk_index': chunk_index,
                'start_word': start,
                'end_word': end,
                'total_words': len(words)
            }

            # Create chunk
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                chunk_index=chunk_index,
                text=chunk_text,
                metadata=chunk_metadata
            )
            chunks.append(chunk)

            # Move to next chunk with overlap
            start += (self.chunk_size - self.chunk_overlap)
            chunk_index += 1

            # Break if we've reached the end
            if end >= len(words):
                break

        return chunks

    def process_markdown_file(self, file_path: str, base_path: str = None) -> Tuple[str, str, Dict, List[DocumentChunk]]:
        """
        Process a single markdown file.

        Returns:
            Tuple of (doc_id, title, metadata, chunks)
        """
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter metadata
        frontmatter, clean_content = self.extract_metadata_from_frontmatter(content)

        # Convert to plain text
        text = self.markdown_to_text(clean_content)

        # Generate doc_id from file path
        if base_path:
            relative_path = os.path.relpath(file_path, base_path)
        else:
            relative_path = file_path

        doc_id = relative_path.replace('\\', '/').replace('/', '_').replace('.md', '')

        # Extract title
        title = frontmatter.get('title', frontmatter.get('id', doc_id))

        # Build metadata
        metadata = {
            'file_path': file_path,
            'relative_path': relative_path,
            'title': title,
            'chapter': self._extract_chapter(relative_path),
            'section': frontmatter.get('sidebar_label', ''),
            **frontmatter
        }

        # Chunk the text
        chunks = self.chunk_text(text, doc_id, metadata)

        return doc_id, title, metadata, chunks

    def _extract_chapter(self, file_path: str) -> str:
        """Extract chapter from file path."""
        # Match patterns like "chapter-01", "chapter-02", etc.
        match = re.search(r'chapter-(\d+)', file_path)
        if match:
            return f"Chapter {int(match.group(1))}"
        return ""

    def process_docs_directory(self, docs_dir: str) -> List[Tuple[str, str, Dict, List[DocumentChunk]]]:
        """
        Process all markdown files in docs directory.

        Returns:
            List of (doc_id, title, metadata, chunks) tuples
        """
        results = []
        docs_path = Path(docs_dir)

        # Find all markdown files
        md_files = list(docs_path.rglob("*.md"))

        for md_file in md_files:
            try:
                doc_id, title, metadata, chunks = self.process_markdown_file(
                    str(md_file),
                    base_path=docs_dir
                )
                results.append((doc_id, title, metadata, chunks))
                print(f"Processed: {title} ({len(chunks)} chunks)")
            except Exception as e:
                print(f"Error processing {md_file}: {e}")

        return results
