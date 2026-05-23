"""
Document processing utilities
Handles PDF, Excel, CSV, and other document formats
"""
import logging
from typing import List, Dict, Any, Optional
import pandas as pd
import openpyxl
from pathlib import Path

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process various document formats"""
    
    @staticmethod
    def process_pdf(file_path: str) -> Dict[str, Any]:
        """
        Process PDF document
        """
        try:
            from pypdf import PdfReader

            logger.info(f"Processing PDF: {file_path}")
            reader = PdfReader(file_path)
            texts: List[str] = []
            for page in reader.pages:
                try:
                    texts.append(page.extract_text() or "")
                except Exception:
                    texts.append("")

            content = "\n\n".join(texts)
            return {
                "content": content,
                "metadata": {},
                "pages": len(reader.pages)
            }
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            raise
    
    @staticmethod
    def process_excel(file_path: str) -> Dict[str, Any]:
        """
        Process Excel document
        """
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Processing Excel: {file_path}")
            
            return {
                "content": df.to_string(),
                "data": df.to_dict(orient="records"),
                "shape": df.shape,
                "columns": list(df.columns),
                "metadata": {
                    "rows": len(df),
                    "columns": len(df.columns)
                }
            }
        except Exception as e:
            logger.error(f"Error processing Excel: {e}")
            raise
    
    @staticmethod
    def process_csv(file_path: str) -> Dict[str, Any]:
        """
        Process CSV document
        """
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Processing CSV: {file_path}")
            
            return {
                "content": df.to_string(),
                "data": df.to_dict(orient="records"),
                "shape": df.shape,
                "columns": list(df.columns),
                "metadata": {
                    "rows": len(df),
                    "columns": len(df.columns)
                }
            }
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            raise
    
    @staticmethod
    def process_text(file_path: str) -> Dict[str, Any]:
        """
        Process plain text document
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"Processing text file: {file_path}")
            
            return {
                "content": content,
                "metadata": {
                    "lines": len(content.split('\n')),
                    "characters": len(content)
                }
            }
        except Exception as e:
            logger.error(f"Error processing text file: {e}")
            raise
    
    @staticmethod
    def process_json(file_path: str) -> Dict[str, Any]:
        """
        Process JSON document
        """
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Processing JSON: {file_path}")
            
            return {
                "content": json.dumps(data, indent=2),
                "data": data,
                "metadata": {
                    "type": type(data).__name__
                }
            }
        except Exception as e:
            logger.error(f"Error processing JSON: {e}")
            raise
    
    @staticmethod
    def detect_file_type(file_path: str) -> str:
        """
        Detect file type by extension
        """
        ext = Path(file_path).suffix.lower()
        
        extension_map = {
            '.pdf': 'pdf',
            '.xlsx': 'excel',
            '.xls': 'excel',
            '.csv': 'csv',
            '.txt': 'text',
            '.json': 'json',
            '.docx': 'docx'
        }
        
        return extension_map.get(ext, 'unknown')
    
    @staticmethod
    def process_document(file_path: str) -> Dict[str, Any]:
        """
        Process document by detecting its type
        """
        file_type = DocumentProcessor.detect_file_type(file_path)
        
        if file_type == 'pdf':
            return DocumentProcessor.process_pdf(file_path)
        elif file_type == 'excel':
            return DocumentProcessor.process_excel(file_path)
        elif file_type == 'csv':
            return DocumentProcessor.process_csv(file_path)
        elif file_type == 'text':
            return DocumentProcessor.process_text(file_path)
        elif file_type == 'json':
            return DocumentProcessor.process_json(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_type}")
            raise ValueError(f"Unsupported file type: {file_type}")
