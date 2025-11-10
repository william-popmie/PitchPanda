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


def convert_pdf_node(state: DeckState) -> dict:
    """Convert PDF to images."""
    print(f"📄 Converting PDF: {state.pdf_path}")
    
    # Get deck name from filename
    from pathlib import Path
    deck_name = Path(state.pdf_path).stem
    
    # Convert PDF to images
    image_paths = pdf_to_images(state.pdf_path)
    print(f"✅ Converted {len(image_paths)} slides to images")
    
    return {"deck_name": deck_name, "image_paths": image_paths}


def encode_images_node(state: DeckState) -> dict:
    """Encode images to base64."""
    print(f"🖼️  Encoding {len(state.image_paths)} images...")
    
    images_base64 = [
        encode_image_base64(img_path) 
        for img_path in state.image_paths
    ]
    
    print(f"✅ Encoded {len(images_base64)} images")
    return {"images_base64": images_base64}


def analyze_deck_node(state: DeckState) -> dict:
    """Analyze the entire deck with GPT-4 Vision."""
    print(f"🤖 Analyzing deck with GPT-4 Vision...")
    
    # Create message with all slides
    messages = create_deck_summary_message(state.images_base64)
    
    # Use JSON mode for more reliable parsing
    try:
        response = vision_llm.invoke(
            messages,
            response_format={"type": "json_object"}
        )
        print(f"  ✓ Received response from GPT-4 Vision")
    except Exception as e:
        print(f"⚠️  JSON mode failed: {e}, trying without")
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
        
        analysis_json = json.loads(json_str)
        print(f"  ✓ Successfully parsed JSON response")
    except Exception as e:
        print(f"⚠️  JSON parsing failed: {e}")
        print(f"  Response preview: {str(response.content)[:500]}...")
        # Fallback to basic structure
        analysis_json = {
            "problem_statement": str(response.content)[:1000],
            "observations": [f"Analysis parsing failed: {str(e)}"]
        }
    
    print(f"✅ Analysis complete")
    return {"analysis_json": analysis_json}


def validate_analysis_node(state: DeckState) -> dict:
    """Validate and structure the analysis."""
    print(f"✔️  Validating analysis...")
    
    try:
        # Create DeckAnalysis object
        analysis = DeckAnalysis(
            deck_name=state.deck_name,
            total_slides=len(state.image_paths),
            **state.analysis_json
        )
        print(f"✅ Validation successful")
        return {"final_analysis": analysis}
    except Exception as e:
        print(f"⚠️  Validation failed: {str(e)[:200]}")
        print(f"⚠️  Analysis JSON keys: {list(state.analysis_json.keys())[:20]}")
        
        # Try to salvage what we can from the analysis_json
        salvaged_data = {
            "deck_name": state.deck_name,
            "total_slides": len(state.image_paths),
        }
        
        # Copy over any fields that exist in the schema with type coercion
        schema_fields = DeckAnalysis.model_fields.keys()
        for key, value in state.analysis_json.items():
            if key in schema_fields:
                try:
                    # Type coercion for common mismatches
                    field_info = DeckAnalysis.model_fields[key]
                    
                    # If field expects Optional[str] but got empty list, convert to None
                    if value == [] and hasattr(field_info.annotation, '__origin__'):
                        if field_info.annotation.__origin__ is type(None) or 'str' in str(field_info.annotation):
                            salvaged_data[key] = None
                            continue
                    
                    # If field expects str but got list, try to join or convert
                    if isinstance(value, list) and 'str' in str(field_info.annotation):
                        if len(value) == 0:
                            salvaged_data[key] = None
                        elif len(value) == 1:
                            salvaged_data[key] = str(value[0])
                        else:
                            salvaged_data[key] = "; ".join(str(v) for v in value)
                        continue
                    
                    salvaged_data[key] = value
                except Exception as field_error:
                    # Skip problematic fields
                    print(f"  ⚠️  Skipping field '{key}': {str(field_error)[:100]}")
                    pass
        
        # Add error info to observations
        if "observations" not in salvaged_data:
            salvaged_data["observations"] = []
        salvaged_data["observations"].append(f"Validation error: {str(e)[:300]}")
        
        if "data_quality_notes" not in salvaged_data:
            salvaged_data["data_quality_notes"] = "Partial data salvaged from failed validation"
        
        try:
            # Try to create analysis with salvaged data
            analysis = DeckAnalysis(**salvaged_data)
            print(f"⚠️  Created analysis with {len(salvaged_data)} salvaged fields")
            return {"final_analysis": analysis}
        except Exception as e2:
            print(f"❌ Salvage failed: {str(e2)[:200]}")
            # Create absolute minimal valid analysis
            analysis = DeckAnalysis(
                deck_name=state.deck_name,
                total_slides=len(state.image_paths),
                problem_statement=state.analysis_json.get("problem_statement", "Analysis could not be completed"),
                observations=[f"Analysis validation failed: {str(e)[:200]}"],
                missing_elements=["Full analysis could not be completed - check logs"],
                data_quality_notes="Validation error occurred - minimal data available"
            )
            return {"final_analysis": analysis}


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
