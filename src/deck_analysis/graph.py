"""
LangGraph workflow for pitch deck analysis.
"""
import os
from typing import Dict, Any, List
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END

from .pdf_utils import pdf_to_images, encode_image_base64
from .prompts import create_deck_summary_message
from .schemas import DeckAnalysis, SlideInsight


# Load environment
load_dotenv()

# Use GPT-4 Vision (gpt-4o has vision capabilities)
vision_llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
parser = JsonOutputParser()


class DeckState(BaseModel):
    """State for deck analysis workflow."""
    pdf_path: str
    deck_name: str = ""
    image_paths: List[str] = Field(default_factory=list)
    images_base64: List[str] = Field(default_factory=list)
    analysis_json: Dict[str, Any] = Field(default_factory=dict)
    final_analysis: DeckAnalysis | None = None


def convert_pdf_node(state: DeckState) -> DeckState:
    """Convert PDF to images."""
    print(f"📄 Converting PDF: {state.pdf_path}")
    
    # Get deck name from filename
    from pathlib import Path
    state.deck_name = Path(state.pdf_path).stem
    
    # Convert PDF to images
    state.image_paths = pdf_to_images(state.pdf_path)
    print(f"✅ Converted {len(state.image_paths)} slides to images")
    
    return state


def encode_images_node(state: DeckState) -> DeckState:
    """Encode images to base64."""
    print(f"🖼️  Encoding {len(state.image_paths)} images...")
    
    state.images_base64 = [
        encode_image_base64(img_path) 
        for img_path in state.image_paths
    ]
    
    print(f"✅ Encoded {len(state.images_base64)} images")
    return state


def analyze_deck_node(state: DeckState) -> DeckState:
    """Analyze the entire deck with GPT-4 Vision."""
    print(f"🤖 Analyzing deck with GPT-4 Vision...")
    
    # Create message with all slides
    messages = create_deck_summary_message(state.images_base64)
    
    # Get analysis
    response = vision_llm.invoke(messages)
    
    # Parse JSON response
    import json
    try:
        # Try to extract JSON from response
        content = response.content
        if "```json" in content:
            # Extract JSON from code block
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
        else:
            json_str = content
        
        state.analysis_json = json.loads(json_str)
    except Exception as e:
        print(f"⚠️  JSON parsing failed: {e}")
        # Fallback to basic structure
        state.analysis_json = {
            "problem_statement": str(response.content)[:500],
            "overall_impression": "Analysis parsing failed"
        }
    
    print(f"✅ Analysis complete")
    return state


def validate_analysis_node(state: DeckState) -> DeckState:
    """Validate and structure the analysis."""
    print(f"✔️  Validating analysis...")
    
    try:
        # Create DeckAnalysis object
        analysis = DeckAnalysis(
            deck_name=state.deck_name,
            total_slides=len(state.image_paths),
            **state.analysis_json
        )
        state.final_analysis = analysis
        print(f"✅ Validation successful")
    except Exception as e:
        print(f"⚠️  Validation failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Create minimal valid analysis with new schema
        state.final_analysis = DeckAnalysis(
            deck_name=state.deck_name,
            total_slides=len(state.image_paths),
            metrics={},
            team=[],
            competition_mentioned=[],
            observations=["Analysis validation failed - please check logs"],
            unlabeled_claims=[],
            present_elements=[],
            missing_elements=["Analys"
            ""
            "is could not be completed"],
            data_quality_notes="Validation error occurred"
        )
    
    return state


# Build the graph
def build_deck_graph():
    """Build the deck analysis graph."""
    builder = StateGraph(DeckState)
    
    builder.add_node("convert_pdf", convert_pdf_node)
    builder.add_node("encode_images", encode_images_node)
    builder.add_node("analyze_deck", analyze_deck_node)
    builder.add_node("validate", validate_analysis_node)
    
    builder.set_entry_point("convert_pdf")
    builder.add_edge("convert_pdf", "encode_images")
    builder.add_edge("encode_images", "analyze_deck")
    builder.add_edge("analyze_deck", "validate")
    builder.add_edge("validate", END)
    
    return builder.compile()


# Create the graph instance
deck_graph = build_deck_graph()
