# German Number Simplifier

A Python utility for simplifying and formatting numbers in German text according to German conventions and readability rules.

## Features

- Simplifies large numbers by rounding to significant digits
- Formats numbers according to German conventions (dot as thousands separator)
- Handles various number formats:
  - Euro amounts (e.g., "324.620,22 Euro" → "etwa 325.000 Euro")
  - Regular counts (e.g., "1.234 Ereignisse" → "etwa 1.000 Ereignisse")
  - Years (preserved without modification)
  - Percentages with special cases (e.g., "25 Prozent" → "jeder Vierte")
- Preserves dates and contextual year references
- Intelligent handling of numbers that look like years but are counts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/german-number-simplifier.git
cd german-number-simplifier
```

2. The script requires Python 3.6+ (only uses standard library modules).

## Usage

### Basic Usage

```python
from number_simplifier import simplify_numbers

# Simple example
text = "324.620,22 Euro wurden gespendet."
simplified = simplify_numbers(text)
print(simplified)  # Output: "etwa 325.000 Euro wurden gespendet."

# Multiple numbers in text
text = "Im Jahr 2024 gab es 1.234 Ereignisse."
simplified = simplify_numbers(text)
print(simplified)  # Output: "Im Jahr 2024 gab es etwa 1.000 Ereignisse."
```

### Formatting Rules

1. **Large Numbers (≥1000)**:
   - Use dot as thousands separator
   - Example: "1.234" → "1.000"

2. **Euro Amounts**:
   - Always use German formatting with thousands separator
   - Round to nearest significant number
   - Example: "324.620,22 Euro" → "etwa 325.000 Euro"

3. **Percentages**:
   - Special cases for common percentages:
     - 25% → "jeder Vierte"
     - 50% → "die Hälfte"
     - 75% → "drei von vier"
     - ≥90% → "fast alle"
     - >50% → "mehr als die Hälfte"
     - ≤15% → "wenige"
   - Others are rounded to whole numbers

4. **Years and Dates**:
   - Preserved without modification when in context
   - Numbers that look like years but are counts are formatted without separator
   - Example: "Im Jahr 2025 gab es 2018 Ereignisse" → "Im Jahr 2025 gab es etwa 2000 Ereignisse"

## Examples

```python
test_cases = [
    "324.620,22 Euro wurden gespendet.",
    "1.897 Menschen nahmen teil.",
    "25 Prozent der Bevölkerung sind betroffen.",
    "90 Prozent stimmten zu.",
    "14 Prozent lehnten ab.",
    "Bei 38,7 Grad Celsius ist es sehr heiß.",
    "Im Jahr 2024 gab es 1.234 Ereignisse.",
    "Am 1. Januar 2024 waren es 5.678 Teilnehmer."
]

for test in test_cases:
    print(f"Input:  {test}")
    print(f"Output: {simplify_numbers(test)}\n")
```

Output:
```
Input:  324.620,22 Euro wurden gespendet.
Output: etwa 325.000 Euro wurden gespendet.

Input:  1.897 Menschen nahmen teil.
Output: etwa 2.000 Menschen nahmen teil.

Input:  25 Prozent der Bevölkerung sind betroffen.
Output: jeder Vierte der Bevölkerung sind betroffen.
```

## Implementation Details

The main functionality is implemented through several key components:

1. **Number Detection**: Uses regular expressions to identify numbers in text while preserving context

2. **Context Analysis**: 
   - Detects dates through date patterns and month names
   - Identifies years through context and value range
   - Distinguishes between counts and year-like numbers

3. **Formatting Logic**:
   - `convert_german_number()`: Converts German number format to float
   - `format_german_number()`: Applies appropriate formatting based on context
   - `round_to_significant()`: Intelligently rounds numbers to meaningful values

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
