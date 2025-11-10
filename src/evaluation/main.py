"""
Main runner for company evaluation.

Evaluates companies based on merged analysis and generates investment scores.

Usage:
    python -m src.evaluation.main
    
Or with a specific company output directory:
    python -m src.evaluation.main output/company-name
"""
import os
import sys
from pathlib import Path

from .graph import evaluation_graph, EvaluationState
from .renderer import render_evaluation
from .schemas import CompanyEvaluation
from ..core.utils import ensure_dir


# Default paths
OUTPUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "output")
)


def evaluate_company_analysis(company_dir: str) -> bool:
    """
    Evaluate a company based on its merged analysis.
    
    Args:
        company_dir: Path to company output directory (e.g., output/company-name)
        
    Returns:
        True if successful, False otherwise
    """
    company_name = os.path.basename(company_dir)
    
    print(f"\n{'='*60}")
    print(f"📊 Evaluating: {company_name}")
    print(f"{'='*60}\n")
    
    # Check for merged analysis
    merged_path = os.path.join(company_dir, "merged_analysis.md")
    
    if not os.path.exists(merged_path):
        print(f"  ❌ No merged analysis found in {company_dir}")
        print(f"      Run merge analysis first!")
        return False
    
    print(f"  📂 Found merged analysis")
    
    # Create initial state
    state = EvaluationState(
        company_name=company_name,
        merged_analysis_path=merged_path,
    )
    
    # Run the evaluation graph
    try:
        result = evaluation_graph.invoke(state)
        
        # Extract the evaluation
        if isinstance(result, dict):
            evaluation_data = result.get("evaluation")
        else:
            evaluation_data = result.evaluation
        
        if not evaluation_data:
            print("  ❌ Failed to generate evaluation")
            return False
        
        # Convert to schema object
        evaluation = CompanyEvaluation(**evaluation_data)
        
        # Render to markdown
        print("  📝 Rendering evaluation...")
        md_content = render_evaluation(evaluation)
        
        # Save to file
        output_path = os.path.join(company_dir, "evaluation.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"  ✅ Saved to: {output_path}")
        print(f"  ⭐ Overall Score: {evaluation.overall_score:.1f}/5.0")
        print()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error during evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_companies(output_dir: str = OUTPUT_DIR) -> None:
    """
    Evaluate all companies in the output directory.
    
    Args:
        output_dir: Path to output directory containing company folders
    """
    if not os.path.exists(output_dir):
        print(f"❌ Output directory not found: {output_dir}")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 Company Evaluation - All Companies")
    print(f"📂 Output directory: {output_dir}")
    print(f"{'='*60}\n")
    
    # Find all company directories with merged analysis
    company_dirs = []
    for item in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item)
        if os.path.isdir(item_path):
            # Check if it has merged analysis
            if os.path.exists(os.path.join(item_path, "merged_analysis.md")):
                company_dirs.append(item_path)
    
    if not company_dirs:
        print("❌ No company directories with merged analysis found")
        print("   Run the merge analysis pipeline first!")
        return
    
    print(f"Found {len(company_dirs)} companies to evaluate\n")
    
    # Process each company
    success_count = 0
    evaluations = []
    
    for company_dir in company_dirs:
        if evaluate_company_analysis(company_dir):
            success_count += 1
            # Load the evaluation for summary
            eval_path = os.path.join(company_dir, "evaluation.md")
            if os.path.exists(eval_path):
                company_name = os.path.basename(company_dir)
                # Read overall score from file (could also store in memory)
                evaluations.append(company_name)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Evaluation Complete!")
    print(f"📊 Evaluated: {success_count}/{len(company_dirs)} companies")
    print(f"{'='*60}\n")
    
    if success_count > 0:
        print("💡 Next steps:")
        print("   - Review evaluation.md files in each company folder")
        print("   - Compare scores across companies")
        print("   - Use scores to prioritize investment decisions")
        print()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Process specific company directory
        company_dir = sys.argv[1]
        if not os.path.isabs(company_dir):
            company_dir = os.path.abspath(company_dir)
        
        evaluate_company_analysis(company_dir)
    else:
        # Process all companies
        run_all_companies()


if __name__ == "__main__":
    main()
