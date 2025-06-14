# LLM-Powered Flashcard Generator

An intelligent flashcard generation tool that converts educational content into effective Q&A flashcards using Google's Gemini AI and Streamlit.

 ** Website Link = [https://flashcard-generator.replit.app/] 
 ** Github Link = [https://github.com/shamee12312/Flashcard-Generator] 
 ** Video Link  = [https://drive.google.com/file/d/1qVy_WaYIPYddSIr6o-sFvrCrNJuYMR9i/view?usp=sharing]
## Features

- **Smart Content Processing**: Upload PDF files or paste text directly
- **AI-Powered Generation**: Uses Google Gemini AI to create intelligent flashcards
- **Subject-Specific Optimization**: Tailored prompts for Biology, History, Computer Science, Mathematics, Chemistry, Physics, Literature, and General topics
- **Interactive Viewer**: Navigate through flashcards with show/hide answer functionality
- **Export Options**: Download flashcards in CSV or JSON formats
- **Difficulty Levels**: Automatically assigns Easy, Medium, or Hard difficulty levels
- **Topic Categorization**: Groups flashcards by detected topics

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Google AI Studio API key

### Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install streamlit google-generativeai PyPDF2 pandas
   ```

### API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create an account or sign in
3. Click "Get API key" in the left sidebar
4. Create a new API key
5. Set the environment variable:
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

### Running the Application

1. Navigate to the project directory
2. Run the Streamlit application:
   ```bash
   streamlit run flashcard_generator.py
   ```
3. Open your browser and go to `http://localhost:8501`

## Usage

### 1. Generate Flashcards

- **Content Input**: Choose between direct text input or file upload (supports .txt and .pdf files)
- **Subject Selection**: Select the appropriate subject type for optimized flashcard generation
- **Number of Cards**: Adjust the slider to set how many flashcards to generate (5-25)
- **Generate**: Click the "Generate Flashcards" button to create your flashcards

### 2. View Flashcards

- Navigate through flashcards using Previous/Next buttons
- Progress bar shows your current position
- Click "Show Answer" to reveal the answer
- View difficulty level and topic for each card

### 3. Export Flashcards

- **CSV Format**: For use in spreadsheet applications
- **JSON Format**: For programmatic use or importing into other applications
- Files include timestamp for easy organization

## Supported File Formats

- **Text Files (.txt)**: Plain text educational content
- **PDF Files (.pdf)**: Automatically extracts text from PDF documents
- **Direct Input**: Paste content directly into the text area

## Subject Types

The application provides specialized prompts for different subjects:

- **Biology**: Focuses on biological processes, terminology, and scientific concepts
- **History**: Emphasizes dates, events, key figures, and historical significance
- **Computer Science**: Covers algorithms, data structures, and programming concepts
- **Mathematics**: Highlights formulas, theorems, and mathematical concepts
- **Chemistry**: Centers on reactions, formulas, and chemical processes
- **Physics**: Focuses on laws, formulas, and physical phenomena
- **Literature**: Emphasizes themes, character analysis, and literary devices
- **General**: Creates diverse flashcards for any subject matter

## Sample Output

Each flashcard includes:
- **Question**: Clear, specific question testing understanding
- **Answer**: Comprehensive, factually correct response
- **Difficulty**: Easy, Medium, or Hard classification
- **Topic**: Specific subject area or concept

## Project Structure

```
├── flashcard_generator.py    # Main application file
├── README.md                # This documentation
├── .streamlit/
│   └── config.toml         # Streamlit configuration
└── pyproject.toml          # Python dependencies
```

## Technical Details

- **Framework**: Streamlit for web interface
- **AI Model**: Google Gemini 1.5 Flash for content generation
- **PDF Processing**: PyPDF2 for text extraction
- **Data Export**: Pandas for CSV generation

## Error Handling

The application includes robust error handling for:
- Invalid API keys
- Malformed PDF files
- Network connectivity issues
- Content that's too short or empty
- JSON parsing errors

## Customization

You can modify the application by:
- Adding new subject types in the `subject_guidance` dictionary
- Adjusting the prompt templates for different flashcard styles
- Modifying the UI layout and styling
- Adding new export formats

## Troubleshooting

**API Key Issues:**
- Ensure your Google API key is correctly set in environment variables
- Verify the key has access to Gemini AI services

**PDF Upload Problems:**
- Check that the PDF contains readable text (not just images)
- Try converting scanned PDFs to text-searchable format

**Generation Failures:**
- Ensure content is at least 100 characters long
- Try different subject types for better results
- Check your internet connection

## Contributing

This project was created as an internship assignment demonstrating LLM integration capabilities. Feel free to extend the functionality by:
- Adding support for more file formats
- Implementing user authentication
- Adding flashcard review scheduling
- Creating mobile-responsive design

## License

This project is for educational purposes and demonstration of LLM integration capabilities.

## Acknowledgments

- Built with Streamlit for rapid web app development
- Powered by Google's Gemini AI for intelligent content generation
- Uses PyPDF2 for reliable PDF text extraction
