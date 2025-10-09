"""
Reusable participant selection component
"""
import streamlit as st
from utils.data_loader import get_available_participants, get_participant_pairs

def participant_selector(mode="individual", key_prefix=""):
    """
    Flexible participant selector component
    
    Args:
        mode: "individual", "pairs", or "mixed"
        key_prefix: prefix for session state keys to avoid conflicts
    
    Returns:
        list of selected participant IDs
    """
    
    if mode == "pairs":
        return _pair_selector(key_prefix)
    elif mode == "individual":
        return _individual_selector(key_prefix)
    else:
        return _mixed_selector(key_prefix)

def _pair_selector(key_prefix=""):
    """Select by participant pairs"""
    pairs = get_participant_pairs()
    
    st.subheader("Select Participant Pairs")
    st.caption("Each pair consists of one OCD participant matched with one healthy control")
    
    selected_pairs = []
    
    for pair in pairs:
        # Simplified layout for sidebar compatibility - no columns
        selected = st.checkbox(
            f"**{pair['pair_id']}**: {pair['ocd_id']} (OCD) ↔ {pair['control_id']} (Control)",
            key=f"{key_prefix}_pair_{pair['pair_id']}",
        )
        
        if selected:
            selected_pairs.extend([pair['ocd_id'], pair['control_id']])
    
    return selected_pairs

def _individual_selector(key_prefix=""):
    """Select individual participants"""
    participants = get_available_participants()
    
    st.subheader("Select Participants")
    
    # Group by type
    ocd_participants = [p for p in participants if p['type'] == 'OCD']
    control_participants = [p for p in participants if p['type'] == 'Control']
    
    # Simplified layout for sidebar compatibility - no columns
    st.markdown("### 🔴 OCD Participants")
    ocd_selected = st.multiselect(
        "Select OCD participants",
        options=[p['id'] for p in ocd_participants],
        key=f"{key_prefix}_ocd_select",
        label_visibility="collapsed"
    )
    
    st.markdown("### 🟢 Control Participants")
    control_selected = st.multiselect(
        "Select control participants",
        options=[p['id'] for p in control_participants],
        key=f"{key_prefix}_control_select",
        label_visibility="collapsed"
    )
    
    return ocd_selected + control_selected

def _mixed_selector(key_prefix=""):
    """Mixed selection with radio button to switch between modes"""
    view_mode = st.radio(
        "Select participants by:",
        ["👥 Pairs", "👤 Individual"],
        horizontal=True,
        key=f"{key_prefix}_view_mode"
    )
    
    st.divider()
    
    if view_mode == "👥 Pairs":
        return _pair_selector(key_prefix)
    else:
        return _individual_selector(key_prefix)

def show_participant_summary(participant_ids):
    """Show summary of selected participants"""
    if not participant_ids:
        st.info("👈 Select participants from the options above")
        return
    
    participants = get_available_participants()
    selected = [p for p in participants if p['id'] in participant_ids]
    
    ocd_count = sum(1 for p in selected if p['type'] == 'OCD')
    control_count = sum(1 for p in selected if p['type'] == 'Control')
    
    # Simplified layout for sidebar compatibility - no columns
    st.metric("Total Selected", len(participant_ids))
    st.metric("🔴 OCD", ocd_count)
    st.metric("🟢 Control", control_count)
    
    if ocd_count > 0 and control_count > 0:
        st.success("✅ Good selection! You have both OCD and Control participants for comparison")
    elif ocd_count == 0:
        st.warning("⚠️ No OCD participants selected - consider adding some for comparison")
    elif control_count == 0:
        st.warning("⚠️ No Control participants selected - consider adding some for comparison")

