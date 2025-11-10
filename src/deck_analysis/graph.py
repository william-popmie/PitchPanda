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
    """Analyze the entire deck with GPT-4 Vision using structured output."""
    print(f"🤖 Analyzing deck with GPT-4 Vision...")
    
    # Create message with all slides
    messages = create_deck_summary_message(state.images_base64)
    
    # Fallback to manual JSON parsing (structured output has issues with required metadata fields)
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
        print(f"✅ Analysis complete")
        return {"analysis_json": analysis_json}
    except Exception as e:
        print(f"⚠️  JSON parsing failed: {e}")
        print(f"  Response preview: {str(response.content)[:500]}...")
        # Fallback to basic structure
        analysis_json = {
            "problem_statement": str(response.content)[:1000],
            "observations": [f"Analysis parsing failed: {str(e)}"]
        }
        return {"analysis_json": analysis_json}


def validate_analysis_node(state: DeckState) -> dict:
    """Validate and structure the analysis."""
    print(f"✔️  Validating analysis...")
    
    # If we already have a final_analysis from structured output, just return it
    if state.final_analysis is not None:
        print(f"✅ Using structured output (no validation needed)")
        return {"final_analysis": state.final_analysis}
    
    import json
    
    def deep_fix_types(obj):
        """Recursively fix type issues in nested structures."""
        if isinstance(obj, dict):
            fixed = {}
            for k, v in obj.items():
                # Fix None to [] for known list fields
                if v is None and k in ['investors', 'partnerships', 'distribution_channels', 'assumptions_stated', 
                                        'supporting_evidence', 'flags', 'key_takeaways', 'key_points', 'data_items', 
                                        'slide_numbers']:
                    fixed[k] = []
                # Fix [] to None for known optional string fields (but NOT for 'notes' which can be either)
                elif v == [] and k in ['context', 'details', 'date', 'valuation', 'status', 'relevance',
                                         'sales_strategy', 'technical_approach', 'pricing_structure', 'customer_acquisition',
                                         'sales_cycle', 'expansion_strategy']:
                    fixed[k] = None
                # Fix string representation of dict/list back to actual dict/list
                elif isinstance(v, str) and v.strip().startswith(('{', '[')):
                    try:
                        fixed[k] = json.loads(v.replace("'", '"'))
                    except:
                        fixed[k] = v
                # Recursively fix nested structures
                elif isinstance(v, dict):
                    fixed[k] = deep_fix_types(v)
                elif isinstance(v, list):
                    fixed[k] = [deep_fix_types(item) if isinstance(item, (dict, list)) else item for item in v]
                else:
                    fixed[k] = v
            return fixed
        elif isinstance(obj, list):
            return [deep_fix_types(item) if isinstance(item, (dict, list)) else item for item in obj]
        return obj
    
    try:
        # Deep fix type issues
        fixed_json = deep_fix_types(state.analysis_json)
        
        # Create DeckAnalysis object
        analysis = DeckAnalysis(
            deck_name=state.deck_name,
            total_slides=len(state.image_paths),
            **fixed_json
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
                    
                    # Fix nested objects with None values in list fields (e.g., FundingDetail.investors)
                    if isinstance(value, list) and value:
                        cleaned_list = []
                        for item in value:
                            if isinstance(item, dict):
                                # Fix None values in nested dict fields that expect lists
                                cleaned_item = {}
                                for item_key, item_value in item.items():
                                    if item_value is None and item_key in ['investors', 'partnerships', 'distribution_channels', 'notes', 'assumptions_stated', 'supporting_evidence', 'flags', 'key_takeaways', 'key_points', 'data_items', 'slide_numbers']:
                                        cleaned_item[item_key] = []
                                    elif isinstance(item_value, list):
                                        # Ensure lists don't have None elements
                                        cleaned_item[item_key] = [v for v in item_value if v is not None]
                                    else:
                                        cleaned_item[item_key] = item_value
                                cleaned_list.append(cleaned_item)
                            else:
                                cleaned_list.append(item)
                        salvaged_data[key] = cleaned_list
                        continue
                    
                    salvaged_data[key] = value
                except Exception as field_error:
                    # Skip problematic fields
                    print(f"  ⚠️  Skipping field '{key}': {str(field_error)[:100]}")
                    pass
        
        # Add error info to observations
        if "observations" not in salvaged_data:
            salvaged_data["observations"] = []
        elif isinstance(salvaged_data["observations"], str):
            # Convert string to list
            salvaged_data["observations"] = [salvaged_data["observations"]]
        
        if isinstance(salvaged_data["observations"], list):
            salvaged_data["observations"].append(f"Validation error: {str(e)[:300]}")
        
        if "data_quality_notes" not in salvaged_data:
            salvaged_data["data_quality_notes"] = "Partial data salvaged from failed validation"
        
        try:
            # Try to create analysis with salvaged data
            print(f"  🔧 Attempting to create analysis with {len(salvaged_data)} salvaged fields...")
            analysis = DeckAnalysis(**salvaged_data)
            print(f"⚠️  Created analysis with salvaged data")
            return {"final_analysis": analysis}
        except Exception as e2:
            print(f"❌ Salvage failed: {str(e2)[:300]}")
            print(f"  🔍 Problematic fields - trying to skip them...")
            
            # More aggressive salvage - skip any fields that cause validation errors
            safe_data = {
                "deck_name": state.deck_name,
                "total_slides": len(state.image_paths),
            }
            
            # Try each field individually
            for key, value in salvaged_data.items():
                if key in ["deck_name", "total_slides"]:
                    continue
                try:
                    test_data = {**safe_data, key: value}
                    DeckAnalysis(**test_data)
                    safe_data[key] = value
                except:
                    print(f"    ⚠️  Skipping field '{key}' - causes validation error")
            
            # Create absolute minimal valid analysis
            try:
                analysis = DeckAnalysis(**safe_data)
                print(f"⚠️  Created minimal analysis with {len(safe_data)} safe fields")
                return {"final_analysis": analysis}
            except Exception as e3:
                print(f"❌ Even minimal salvage failed: {str(e3)[:200]}")
                # Last resort - completely minimal
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
