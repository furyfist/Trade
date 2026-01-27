from .database import get_supabase
from typing import Dict, Any, List, Optional
from datetime import datetime

def create_hypothesis_analysis(analysis_data: Dict[str, Any]) -> str:
    """
    Saves the analysis object to the 'hypotheses' table in Supabase.
    """
    client = get_supabase()
    if client is None:
        raise Exception("Database not connected.")
        
    # Prepare the record for insertion
    # We map the complex nested dictionaries to JSONB columns
    record = {
        "processed_hypothesis": analysis_data.get("processed_hypothesis"),
        "confidence_score": analysis_data.get("confidence_score"),
        "synthesis": analysis_data.get("synthesis"),
        "status": analysis_data.get("status"),
        "original_hypothesis": analysis_data.get("original_hypothesis"),
        "method": analysis_data.get("method"),
        
        # JSONB fields
        "context": analysis_data.get("context", {}),
        "research_data": analysis_data.get("research_data", {}),
        "contradictions": analysis_data.get("contradictions", []),
        "confirmations": analysis_data.get("confirmations", []),
        "alerts": analysis_data.get("alerts", [])
    }
    
    # Execute insert and return the new ID
    response = client.table("hypotheses").insert(record).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]["id"]
    else:
        raise Exception("Failed to insert hypothesis.")

def get_all_hypotheses_summary() -> List[Dict[str, Any]]:
    """
    Gets a summary of recent hypotheses for the dashboard.
    """
    client = get_supabase()
    if client is None:
        raise Exception("Database not connected.")
        
    # Select specific fields and order by created_at desc
    response = client.table("hypotheses").select(
        "id, processed_hypothesis, confidence_score, synthesis, contradictions, confirmations, status, context, created_at"
    ).order("created_at", desc=True).limit(50).execute()
    
    summaries = []
    
    for row in response.data:
        # Prepare list fields
        contradictions_list = row.get("contradictions", [])
        confirmations_list = row.get("confirmations", [])
        
        # Determine confidence percentage
        confidence_val = row.get("confidence_score")
        confidence_pct = round(confidence_val * 100) if confidence_val is not None else 50
        
        # Get primary symbol from nested JSON context
        # Supabase returns the JSON object directly for JSONB columns
        context_data = row.get("context") or {}
        primary_symbol = context_data.get("primary_symbol")
        
        # Transform for frontend
        summary = {
            "_id": row["id"], # Keep _id for frontend compatibility if needed, or update frontend to use id
            "id": row["id"],
            "title": row.get("processed_hypothesis", "Untitled Hypothesis"),
            "status": row.get("status"),
            "confidence": confidence_pct,
            "confidence_score": confidence_val,
            "synthesis": row.get("synthesis"),
            
            # Counts
            "contradictions": len(contradictions_list) if isinstance(contradictions_list, list) else 0,
            "confirmations": len(confirmations_list) if isinstance(confirmations_list, list) else 0,
            
            # Details
            "contradictions_detail": contradictions_list if isinstance(contradictions_list, list) else [],
            "confirmations_detail": confirmations_list if isinstance(confirmations_list, list) else [],
            
            # Context
            "context": {"primary_symbol": primary_symbol} if primary_symbol else {},
            "created_at": row.get("created_at")
        }
        
        # Format lastUpdated
        if row.get("created_at"):
            try:
                dt = datetime.fromisoformat(row["created_at"].replace('Z', '+00:00'))
                summary["lastUpdated"] = dt.strftime("%Y-%m-%d %H:%M")
            except:
                summary["lastUpdated"] = "Recently"
        else:
            summary["lastUpdated"] = "Recently"
            
        summaries.append(summary)
        
    return summaries

def get_hypothesis_by_id(hypothesis_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a single complete hypothesis by UUID.
    """
    client = get_supabase()
    if client is None:
        raise Exception("Database not connected.")
        
    try:
        response = client.table("hypotheses").select("*").eq("id", hypothesis_id).single().execute()
        doc = response.data
        
        if doc:
            doc["_id"] = doc["id"] # Compatibility
            return doc
            
    except Exception as e:
        print(f"Error fetching hypothesis {hypothesis_id}: {e}")
        return None
    
    return None
