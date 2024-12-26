import re
from decimal import Decimal

def simplify_numbers(raw_text: str) -> str:
    """
    Simplifies numbers in text according to specified rules:
    1. Rounds large numbers
    2. Converts percentages to simple comparisons
    3. Uses simple descriptions for quantities
    4. Adds contextual explanations (not implemented in basic version)
    5. Uses figurative comparisons (not implemented in basic version)
    
    Args:
        raw_text (str): Input text containing numbers to simplify
        
    Returns:
        str: Text with simplified numbers
    """
    
    def convert_german_number(number_str: str) -> float:
        """Convert German number format (1.234,56) to float."""
        # Remove thousand separators and replace comma with dot
        clean_num = number_str.replace('.', '').replace(',', '.')
        return float(clean_num)
    
    def format_german_number(number: int, is_count: bool = True) -> str:
        """Format number with German thousands separator for numbers >= 1000."""
        # Don't use separators for years or when is_count is False
        if not is_count:
            return str(number)
        if number >= 1000:
            return f"{number:,}".replace(',', '.')
        return str(number)
    
    def round_to_significant(number: float) -> int:
        """Round to nearest significant number for simplification."""
        if number < 100:
            return round(number)
            
        # Convert to string to analyze digits
        num_str = f"{number:,.0f}".replace(',', '')
        num_length = len(num_str)
        
        if number >= 100000:
            # For numbers like 324620, we want to keep first 3 digits and round
            magnitude = 10 ** (num_length - 3)
            return round(number / magnitude) * magnitude
        elif number >= 1000:
            # For numbers in thousands, round to nearest thousand
            return round(number / 1000) * 1000
        else:
            # For numbers between 100 and 999, round to nearest hundred
            return round(number / 100) * 100
    
    def simplify_percentage(match):
        """Convert percentage to descriptive text."""
        number = float(match.group(1).replace(',', '.'))
        
        if number == 25:
            return "jeder Vierte"
        elif number == 50:
            return "die Hälfte"
        elif number == 75:
            return "drei von vier"
        elif number >= 90:
            return "fast alle"
        elif number > 50:
            return "mehr als die Hälfte"
        elif number <= 15:
            return "wenige"
        else:
            return f"etwa {round(number)} Prozent"
    
    def looks_like_year(text: str, pos: int, number: int) -> bool:
        """
        Determine if a number is likely to be a year based on context and value.
        """
        # Get the text before the number
        before_text = text[:pos].strip()
        
        # If it's preceded by "Jahr" or "Jahre", it's not a count
        if before_text.endswith(("Jahr ", "Jahre ")):
            return False
            
        # If it's a 4-digit number between 1900 and 2100, it might be a year
        if 1900 <= number <= 2100:
            return True
            
        return False

    def simplify_regular_number(match, text_pos):
        """Simplify regular numbers."""
        number_str = match.group(1)
        try:
            number = convert_german_number(number_str)
            rounded = round_to_significant(number)
            # Ensure we keep a space between number and currency/unit
            suffix = match.group(2) if len(match.groups()) > 1 else ""
            
            # Check if this looks like a year
            is_count = not looks_like_year(text, text_pos, round(number))
            
            # Format accordingly
            return f"etwa {format_german_number(rounded, is_count)}" + (" " + suffix if suffix else "")
                
        except ValueError:
            return number_str

    def is_part_of_date(text, pos):
        """Check if number at position is part of a date"""
        # Check for day.month format
        if pos > 0 and text[pos-2:pos].isspace() and re.match(r'\d+\.', text[pos:pos+4]):
            return True
            
        # Look ahead for month names
        next_words = text[pos:pos+50].split()
        if not next_words:
            return False
            
        months = ["Januar", "Februar", "März", "April", "Mai", "Juni", 
                 "Juli", "August", "September", "Oktober", "November", "Dezember"]
        
        # If next word is a month, this is part of a date
        return next_words[0] in months or (
            len(next_words) > 1 and next_words[1] in months
        )
    
    def is_year(text, pos):
        """Check if number at position appears to be a year"""
        # Get the full context before the number
        before_text = text[:pos].strip()
        # Get the number itself
        number_match = re.match(r'\d+', text[pos:])
        if not number_match:
            return False
            
        number = number_match.group()
        
        # It's a year if:
        # 1. It's explicitly marked as a year ("Jahr YYYY")
        # 2. It's a 4-digit number in a date context (after a month name)
        if before_text.endswith("Jahr"):
            return True
            
        if len(number) == 4 and number.startswith(('19', '20')):
            months = ["Januar", "Februar", "März", "April", "Mai", "Juni", 
                     "Juli", "August", "September", "Oktober", "November", "Dezember"]
            before_words = before_text.split()
            # Check if the number follows a month name
            return any(month in before_words[-1] for month in months)
            
        return False
    
    # Process text in steps
    text = raw_text
    
    # Replace percentages first
    text = re.sub(r'(\d+(?:,\d+)?)\s*Prozent', simplify_percentage, text)
    
    # Find and process regular numbers while preserving dates
    pattern = r'(\d+(?:\.\d+)*(?:,\d+)?)\s*((?:Euro|[A-Za-zÄäÖöÜüß]+)?)'
    
    # Process each match individually to handle date/year preservation
    result = ""
    last_end = 0
    
    for match in re.finditer(pattern, text):
        start = match.start()
        # Add text before the match
        result += text[last_end:start]
        
        # Check if this number is part of a date or year
        if not (is_part_of_date(text, start) or is_year(text, start)):
            # If not a date/year, simplify the number
            result += simplify_regular_number(match, start)
        else:
            # If it's a date/year, keep it as is
            result += match.group(0)
            
        last_end = match.end()
    
    # Add remaining text
    result += text[last_end:]
    
    return result

# Test cases
test_cases = [
    "324.620,22 Euro wurden gespendet.",
    "1.897 Menschen nahmen teil.",
    "25 Prozent der Bevölkerung sind betroffen.",
    "90 Prozent stimmten zu.",
    "14 Prozent lehnten ab.",
    "Bei 38,7 Grad Celsius ist es sehr heiß.",
    "denn die Rente steigt um 4,57 Prozent.",
    "Im Jahr 2024 gab es 1.234 Ereignisse.",
    "Am 1. Januar 2024 waren es 5.678 Teilnehmer.",
    "Im Jahr 2025 gab es 2018 Ereignisse."
]

# Run test cases
for test in test_cases:
    print(f"{simplify_numbers(test)}")