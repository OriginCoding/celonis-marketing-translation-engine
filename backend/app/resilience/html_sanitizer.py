import re

class HTMLSanitizer:
    """
    100% Free & Open-Source HTML XSS Security Sanitizer.
    Strips dangerous executable elements (<script>, <iframe>, <object>, <embed>) 
    and inline event handlers (onload=, onerror=, onclick=) while preserving 
    semantic HTML tags (<h1>, <p>, <a>, <strong>, <em>, <ul>, <li>, <div>, <span>).
    """

    DANGEROUS_TAGS = [r"<script.*?>.*?</script>", r"<iframe.*?>.*?</iframe>", r"<object.*?>.*?</object>", r"<embed.*?>.*?</embed>"]
    DANGEROUS_ATTRIBUTES = [r"\s+on\w+\s*=\s*['\"].*?['\"]", r"javascript\s*:\s*"]

    @classmethod
    def sanitize(cls, html_content: str) -> str:
        """Sanitizes HTML content to prevent XSS injection attacks."""
        sanitized = html_content
        
        # Strip executable tags
        for tag_pattern in cls.DANGEROUS_TAGS:
            sanitized = re.sub(tag_pattern, "", sanitized, flags=re.IGNORECASE | re.DOTALL)
            
        # Strip inline event handlers and javascript: URIs
        for attr_pattern in cls.DANGEROUS_ATTRIBUTES:
            sanitized = re.sub(attr_pattern, "", sanitized, flags=re.IGNORECASE)
            
        return sanitized.strip()
