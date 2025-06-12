import streamlit as st
import json
import os
import re
import pandas as pd
from datetime import datetime
import google.generativeai as genai
import PyPDF2
from io import BytesIO

# Google AI Configuration
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# Initialize session state
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []
if 'current_card_index' not in st.session_state:
    st.session_state.current_card_index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error reading PDF file: {str(e)}")
        return None

def clean_text(text):
    """Clean and preprocess text content."""
    # Remove excessive whitespace and normalize line breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def generate_flashcards(content, subject_type="General", num_cards=15):
    """Generate flashcards using Google's Gemini AI."""
    try:
        # Construct the prompt based on subject type
        subject_guidance = {
            "Biology": "Focus on biological processes, terminology, classifications, and scientific concepts.",
            "History": "Focus on dates, events, key figures, causes and effects, and historical significance.",
            "Computer Science": "Focus on algorithms, data structures, programming concepts, and technical definitions.",
            "Mathematics": "Focus on formulas, theorems, problem-solving steps, and mathematical concepts.",
            "Chemistry": "Focus on chemical reactions, formulas, periodic table elements, and chemical processes.",
            "Physics": "Focus on laws, formulas, physical phenomena, and scientific principles.",
            "Literature": "Focus on themes, character analysis, literary devices, and plot elements.",
            "General": "Create diverse flashcards covering key concepts, definitions, and important facts."
        }
        
        guidance = subject_guidance.get(subject_type, subject_guidance["General"])
        
        prompt = f"""
        You are an expert educational content creator. Generate exactly {num_cards} high-quality flashcards from the following educational content.

        Subject Type: {subject_type}
        Guidance: {guidance}

        Content:
        {content}

        Requirements:
        1. Create exactly {num_cards} flashcards
        2. Each flashcard should have a clear, concise question and a factually correct, self-contained answer
        3. Questions should test understanding, not just memorization
        4. Answers should be comprehensive but concise
        5. Cover different aspects and difficulty levels of the content
        6. Ensure questions are specific and unambiguous

        Return the flashcards in the following JSON format:
        {{
            "flashcards": [
                {{
                    "question": "Clear, specific question here",
                    "answer": "Complete, accurate answer here",
                    "difficulty": "Easy|Medium|Hard",
                    "topic": "Specific topic/concept"
                }}
            ]
        }}
        """
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate content using Gemini
        response = model.generate_content(prompt)
        
        # Parse JSON response
        response_text = response.text
        # Clean up any markdown formatting that might be present
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        
        result = json.loads(response_text)
        return result.get("flashcards", [])
        
    except Exception as e:
        st.error(f"Error generating flashcards: {str(e)}")
        return []

def display_flashcard_viewer():
    """Display the flashcard viewer interface."""
    if not st.session_state.flashcards:
        st.info("No flashcards generated yet. Please generate some flashcards first.")
        return
    
    st.header("📚 Flashcard Viewer")
    
    total_cards = len(st.session_state.flashcards)
    current_card = st.session_state.flashcards[st.session_state.current_card_index]
    
    # Card navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.current_card_index == 0):
            st.session_state.current_card_index -= 1
            st.session_state.show_answer = False
            st.rerun()
    
    with col2:
        st.write(f"Card {st.session_state.current_card_index + 1} of {total_cards}")
        progress = (st.session_state.current_card_index + 1) / total_cards
        st.progress(progress)
    
    with col3:
        if st.button("Next ➡️", disabled=st.session_state.current_card_index == total_cards - 1):
            st.session_state.current_card_index += 1
            st.session_state.show_answer = False
            st.rerun()
    
    # Card display
    st.markdown("---")
    
    # Question
    st.subheader("❓ Question")
    st.markdown(f"**{current_card['question']}**")
    
    # Show/Hide answer button
    if st.button("🔍 Show Answer" if not st.session_state.show_answer else "🙈 Hide Answer"):
        st.session_state.show_answer = not st.session_state.show_answer
        st.rerun()
    
    # Answer
    if st.session_state.show_answer:
        st.subheader("✅ Answer")
        st.markdown(current_card['answer'])
        
        # Additional info
        col1, col2 = st.columns(2)
        with col1:
            difficulty_color = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
            difficulty_icon = difficulty_color.get(current_card.get('difficulty', 'Medium'), "🟡")
            st.write(f"**Difficulty:** {difficulty_icon} {current_card.get('difficulty', 'Medium')}")
        with col2:
            st.write(f"**Topic:** {current_card.get('topic', 'General')}")

def export_flashcards_csv():
    """Export flashcards to CSV format."""
    if not st.session_state.flashcards:
        st.warning("No flashcards to export.")
        return None
    
    df = pd.DataFrame(st.session_state.flashcards)
    return df.to_csv(index=False)

def export_flashcards_json():
    """Export flashcards to JSON format."""
    if not st.session_state.flashcards:
        st.warning("No flashcards to export.")
        return None
    
    export_data = {
        "generated_on": datetime.now().isoformat(),
        "total_cards": len(st.session_state.flashcards),
        "flashcards": st.session_state.flashcards
    }
    return json.dumps(export_data, indent=2)

def main():
    """Main application function."""
    st.set_page_config(
        page_title="LLM-Powered Flashcard Generator",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 LLM-Powered Flashcard Generator")
    st.markdown("Convert your educational content into effective Q&A flashcards using AI")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Generate Flashcards", "View Flashcards", "Export"])
    
    if page == "Generate Flashcards":
        st.header("📝 Content Input")
        
        # Subject selection
        subject_options = [
            "General", "Biology", "History", "Computer Science", 
            "Mathematics", "Chemistry", "Physics", "Literature"
        ]
        subject = st.selectbox("Select Subject Type (optional):", subject_options)
        
        # Number of flashcards
        num_cards = st.slider("Number of flashcards to generate:", min_value=5, max_value=25, value=15)
        
        # Input method selection
        input_method = st.radio("Choose input method:", ["Direct Text Input", "File Upload"])
        
        content = ""
        
        if input_method == "Direct Text Input":
            content = st.text_area(
                "Paste your educational content here:",
                height=300,
                placeholder="Enter your educational content here (lecture notes, textbook excerpts, etc.)"
            )
        
        else:  # File Upload
            uploaded_file = st.file_uploader(
                "Upload your educational content:",
                type=['txt', 'pdf'],
                help="Supported formats: .txt, .pdf"
            )
            
            if uploaded_file is not None:
                if uploaded_file.type == "text/plain":
                    content = str(uploaded_file.read(), "utf-8")
                elif uploaded_file.type == "application/pdf":
                    content = extract_text_from_pdf(uploaded_file)
                
                if content:
                    st.success(f"File uploaded successfully! Content length: {len(content)} characters")
                    with st.expander("Preview content"):
                        st.text(content[:500] + "..." if len(content) > 500 else content)
        
        # Generate flashcards button
        if st.button("🚀 Generate Flashcards", type="primary"):
            if not content or not content.strip():
                st.error("Please provide some educational content to generate flashcards.")
            elif len(content.strip()) < 100:
                st.error("Content is too short. Please provide more substantial educational material.")
            else:
                with st.spinner("Generating flashcards using AI... This may take a moment."):
                    cleaned_content = clean_text(content)
                    flashcards = generate_flashcards(cleaned_content, subject, num_cards)
                    
                    if flashcards:
                        st.session_state.flashcards = flashcards
                        st.session_state.current_card_index = 0
                        st.session_state.show_answer = False
                        st.success(f"Successfully generated {len(flashcards)} flashcards!")
                        st.info("Go to 'View Flashcards' to review your generated flashcards.")
                    else:
                        st.error("Failed to generate flashcards. Please try again with different content.")
    
    elif page == "View Flashcards":
        display_flashcard_viewer()
    
    elif page == "Export":
        st.header("📤 Export Flashcards")
        
        if not st.session_state.flashcards:
            st.info("No flashcards to export. Please generate some flashcards first.")
        else:
            st.write(f"Total flashcards: {len(st.session_state.flashcards)}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("CSV Export")
                st.write("Export as CSV file for use in spreadsheet applications")
                csv_data = export_flashcards_csv()
                if csv_data:
                    st.download_button(
                        label="📊 Download CSV",
                        data=csv_data,
                        file_name=f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                st.subheader("JSON Export")
                st.write("Export as JSON file for programmatic use")
                json_data = export_flashcards_json()
                if json_data:
                    st.download_button(
                        label="📋 Download JSON",
                        data=json_data,
                        file_name=f"flashcards_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            # Preview section
            st.subheader("Preview Generated Flashcards")
            for i, card in enumerate(st.session_state.flashcards[:5]):  # Show first 5 cards
                with st.expander(f"Card {i+1}: {card['question'][:50]}..."):
                    st.write(f"**Question:** {card['question']}")
                    st.write(f"**Answer:** {card['answer']}")
                    st.write(f"**Difficulty:** {card.get('difficulty', 'Medium')}")
                    st.write(f"**Topic:** {card.get('topic', 'General')}")
            
            if len(st.session_state.flashcards) > 5:
                st.info(f"Showing preview of first 5 cards. Total cards: {len(st.session_state.flashcards)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>LLM-Powered Flashcard Generator | Built with Streamlit and Google Gemini AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
