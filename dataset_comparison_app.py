"""
Dataset Comparison App
=====================

A Streamlit application for comparing two CSV datasets with flexible column mapping options.

Packaging Instructions:
----------------------
1. Install required packages:
   pip install streamlit pandas pyinstaller

2. Create executable:
   pyinstaller --onefile --add-data "streamlit:streamlit" dataset_comparison_app.py

Platform Notes:
--------------
- Windows: No special considerations
- Mac: May need to run 'xattr -d com.apple.quarantine dataset_comparison_app' after first run
- Linux: No special considerations

Note: The executable will be created in the 'dist' directory.
"""

import streamlit as st
import pandas as pd
import io
from typing import Dict, List, Tuple, Set
import base64

# Set page config
st.set_page_config(
    page_title="Dataset Comparison Tool",
    page_icon="🔍",
    layout="wide"
)

def load_csv(uploaded_file) -> pd.DataFrame:
    """Load CSV file into a pandas DataFrame."""
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return None

def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame, column_mapping: Dict[str, str], left_filename: str, right_filename: str) -> Tuple[bool, pd.DataFrame]:
    """Compare two datasets using the specified column mapping."""
    try:
        # Create copies to avoid modifying original dataframes
        df1_copy = df1.copy()
        df2_copy = df2.copy()
        
        # Rename columns in second dataframe according to mapping
        df2_copy = df2_copy.rename(columns=column_mapping)
        
        # Perform merge
        merged = pd.merge(
            df1_copy,
            df2_copy,
            on=list(column_mapping.keys()),
            how='outer',
            indicator=True
        )
        
        # Rename the _merge column to use actual filenames
        merged = merged.rename(columns={'_merge': 'Dataset'})
        merged['Dataset'] = merged['Dataset'].map({
            'left_only': f'Only in {left_filename}',
            'right_only': f'Only in {right_filename}',
            'both': f'In both {left_filename} and {right_filename}'
        })
        
        # Check if datasets are identical
        is_identical = (
            len(merged[merged['Dataset'] != f'In both {left_filename} and {right_filename}']) == 0 and
            len(df1) == len(df2)
        )
        
        # Get mismatched rows
        mismatched = merged[merged['Dataset'] != f'In both {left_filename} and {right_filename}']
        
        return is_identical, mismatched
    
    except Exception as e:
        st.error(f"Error comparing datasets: {str(e)}")
        return False, pd.DataFrame()

def get_matching_columns(left_cols: Set[str], right_cols: Set[str]) -> Tuple[Set[str], Set[str], Set[str]]:
    """Get matching and non-matching columns between two datasets."""
    matching = left_cols.intersection(right_cols)
    left_only = left_cols - right_cols
    right_only = right_cols - left_cols
    return matching, left_only, right_only

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    img_base64 = get_base64_image("db_equal.png")
    st.markdown(
        f'''
        <div style="display: flex; align-items: center; gap: 18px; padding-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" width="200" style="margin-bottom: 0;">
            <h1 style="margin-bottom: 0;">Dataset Comparison Tool</h1>
        </div>
        ''',
        unsafe_allow_html=True
    )
    st.write("Upload two CSV files to compare their contents.")
    
    # File uploaders
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Left Dataset")
        left_file = st.file_uploader("Upload first CSV file", type=['csv'])
    
    with col2:
        st.subheader("Right Dataset")
        right_file = st.file_uploader("Upload second CSV file", type=['csv'])
    
    # Load datasets
    if left_file and right_file:
        df_left = load_csv(left_file)
        df_right = load_csv(right_file)
        
        if df_left is not None and df_right is not None:
            # Get filenames for display
            left_filename = left_file.name.replace('.csv', '')
            right_filename = right_file.name.replace('.csv', '')
            
            # Comparison type selection
            comparison_type = st.radio(
                "Select comparison type:",
                ["All columns", "Single column", "Custom columns"]
            )
            
            # Initialize session state for comparison type if not exists
            if 'previous_comparison_type' not in st.session_state:
                st.session_state.previous_comparison_type = comparison_type
            
            # Reset state if comparison type changes
            if st.session_state.previous_comparison_type != comparison_type:
                # Clear all relevant session state variables
                if 'column_mapping' in st.session_state:
                    del st.session_state.column_mapping
                if 'removed_auto_columns' in st.session_state:
                    del st.session_state.removed_auto_columns
                if 'removed_review_columns' in st.session_state:
                    del st.session_state.removed_review_columns
                if 'selected_left_cols' in st.session_state:
                    del st.session_state.selected_left_cols
                if 'selected_right_cols' in st.session_state:
                    del st.session_state.selected_right_cols
                if 'mismatched' in st.session_state:
                    del st.session_state.mismatched
                if 'is_identical' in st.session_state:
                    del st.session_state.is_identical
                # Update previous comparison type
                st.session_state.previous_comparison_type = comparison_type
                st.rerun()
            
            # Initialize session state for column mappings if not exists
            if 'column_mapping' not in st.session_state:
                st.session_state.column_mapping = {}
            
            # Initialize session state for removed columns if not exists
            if 'removed_auto_columns' not in st.session_state:
                st.session_state.removed_auto_columns = set()
            if 'removed_review_columns' not in st.session_state:
                st.session_state.removed_review_columns = set()
            
            if comparison_type == "All columns":
                # Get matching and non-matching columns
                matching_cols, left_only_cols, right_only_cols = get_matching_columns(
                    set(df_left.columns),
                    set(df_right.columns)
                )
                
                # Initialize column mapping with matching columns if not already set
                if not st.session_state.column_mapping:
                    st.session_state.column_mapping = {col: col for col in matching_cols}
                
                # Show column count information
                st.write(f"Left dataset has {len(df_left.columns)} columns")
                st.write(f"Right dataset has {len(df_right.columns)} columns")
                
                # Show matching columns with option to override
                if matching_cols:
                    # Create expander for automatic mappings (closed by default)
                    with st.expander(
                        f"✅ Automatically mapped columns ({len(matching_cols)})",
                        expanded=False
                    ):
                        for col in sorted(matching_cols):
                            if col in st.session_state.removed_auto_columns:
                                col1, col2, col3 = st.columns([2, 2, 1])
                                with col1:
                                    st.text_input("Left column", value=col, disabled=True, key=f"disabled_left_{col}")
                                with col2:
                                    right_val = st.session_state.column_mapping.get(col, "")
                                    st.text_input("Right column", value=right_val, disabled=True, key=f"disabled_right_{col}")
                                with col3:
                                    if st.button("Add Back", key=f"add_back_auto_{col}"):
                                        st.session_state.column_mapping[col] = col
                                        st.session_state.removed_auto_columns.remove(col)
                                        st.rerun()
                                continue
                            else:
                                st.divider()  # Add divider before each mapping
                                col1, col2, col3 = st.columns([2, 2, 1])
                                with col1:
                                    st.write(f"Left column: {col}")
                                with col2:
                                    # Allow overriding automatic mapping
                                    override = st.checkbox(
                                        "Override mapping",
                                        key=f"override_{col}"
                                    )
                                    if override:
                                        right_col = st.selectbox(
                                            "Map to right column:",
                                            sorted(df_right.columns),
                                            key=f"mapping_auto_{col}"
                                        )
                                        st.session_state.column_mapping[col] = right_col
                                    else:
                                        st.write(f"Right column: {col}")
                                with col3:
                                    if st.button("Remove", key=f"remove_auto_{col}"):
                                        st.session_state.column_mapping.pop(col, None)
                                        st.session_state.removed_auto_columns.add(col)
                                        st.rerun()
                
                # Show and handle non-matching columns
                if left_only_cols or right_only_cols:
                    st.warning("⚠️ Some columns don't match exactly. Please review the mapping:")
                    
                    # Create a container for manual mapping
                    mapping_container = st.container()
                    
                    with mapping_container:
                        # Show left-only columns
                        if left_only_cols:
                            st.write("Columns in left dataset only:")
                            for left_col in sorted(left_only_cols):
                                if left_col not in st.session_state.removed_review_columns:
                                    st.divider()  # Add divider before each mapping
                                    col1, col2, col3 = st.columns([2, 2, 1])
                                    with col1:
                                        st.write(f"Left column: {left_col}")
                                    with col2:
                                        right_col = st.selectbox(
                                            f"Map to right column:",
                                            ["(No mapping)"] + sorted(df_right.columns),
                                            key=f"mapping_left_{left_col}"
                                        )
                                        if right_col != "(No mapping)":
                                            st.session_state.column_mapping[left_col] = right_col
                                        elif left_col in st.session_state.column_mapping:
                                            st.session_state.column_mapping.pop(left_col, None)
                                    with col3:
                                        if st.button("Remove", key=f"remove_left_{left_col}"):
                                            st.session_state.column_mapping.pop(left_col, None)
                                            st.session_state.removed_review_columns.add(left_col)
                                            st.rerun()
                        
                        # Show right-only columns
                        if right_only_cols:
                            st.write("Columns in right dataset only:")
                            for right_col in sorted(right_only_cols):
                                if right_col not in st.session_state.removed_review_columns:
                                    st.divider()  # Add divider before each mapping
                                    col1, col2, col3 = st.columns([2, 2, 1])
                                    with col1:
                                        left_col = st.selectbox(
                                            f"Map to left column:",
                                            ["(No mapping)"] + sorted(df_left.columns),
                                            key=f"mapping_right_{right_col}"
                                        )
                                        with col2:
                                            st.write(f"Right column: {right_col}")
                                        with col3:
                                            if st.button("Remove", key=f"remove_right_{right_col}"):
                                                if left_col in st.session_state.column_mapping:
                                                    st.session_state.column_mapping.pop(left_col, None)
                                                st.session_state.removed_review_columns.add(right_col)
                                                st.rerun()
                                        if left_col != "(No mapping)":
                                            st.session_state.column_mapping[left_col] = right_col
                                        elif left_col in st.session_state.column_mapping:
                                            st.session_state.column_mapping.pop(left_col, None)
                
                # Show current mapping summary
                if st.session_state.column_mapping:
                    st.write("Current column mapping:")
                    mapping_df = pd.DataFrame([
                        {"Left Column": k, "Right Column": v}
                        for k, v in st.session_state.column_mapping.items()
                    ])
                    st.dataframe(mapping_df)
            
            elif comparison_type == "Single column":
                col1, col2 = st.columns(2)
                with col1:
                    left_col = st.selectbox("Select column from left dataset:", df_left.columns)
                with col2:
                    right_col = st.selectbox("Select column from right dataset:", df_right.columns)
                st.session_state.column_mapping = {left_col: right_col}
            
            elif comparison_type == "Custom columns":
                st.write("Select columns to compare and map them between datasets:")
                
                # Initialize session state for selected columns if not exists
                if 'selected_left_cols' not in st.session_state:
                    st.session_state.selected_left_cols = []
                if 'selected_right_cols' not in st.session_state:
                    st.session_state.selected_right_cols = []
                
                # Column selection with bulk operations
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Left dataset columns:")
                    # Add bulk operation buttons
                    bulk_col1, bulk_col2 = st.columns(2)
                    with bulk_col1:
                        if st.button("Add All Columns", key="add_all_left"):
                            st.session_state.selected_left_cols = list(df_left.columns)
                            st.rerun()
                    with bulk_col2:
                        if st.button("Remove All Columns", key="remove_all_left"):
                            st.session_state.selected_left_cols = []
                            st.rerun()
                    # Column multiselect
                    left_cols = st.multiselect(
                        "Select columns from left dataset:",
                        df_left.columns,
                        default=st.session_state.selected_left_cols,
                        key="left_cols_select"
                    )
                    st.session_state.selected_left_cols = left_cols
                
                with col2:
                    st.write("Right dataset columns:")
                    # Add bulk operation buttons
                    bulk_col1, bulk_col2 = st.columns(2)
                    with bulk_col1:
                        if st.button("Add All Columns", key="add_all_right"):
                            st.session_state.selected_right_cols = list(df_right.columns)
                            st.rerun()
                    with bulk_col2:
                        if st.button("Remove All Columns", key="remove_all_right"):
                            st.session_state.selected_right_cols = []
                            st.rerun()
                    # Column multiselect
                    right_cols = st.multiselect(
                        "Select columns from right dataset:",
                        df_right.columns,
                        default=st.session_state.selected_right_cols,
                        key="right_cols_select"
                    )
                    st.session_state.selected_right_cols = right_cols
                
                if len(left_cols) != len(right_cols):
                    st.error("Please select the same number of columns from both datasets.")
                    return
                
                # Column mapping
                st.write("Map columns between datasets:")
                for i, left_col in enumerate(left_cols):
                    st.divider()  # Add divider before each mapping
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"Left column: {left_col}")
                    with col2:
                        right_col = st.selectbox(
                            f"Map to right column:",
                            right_cols,
                            key=f"mapping_{i}"
                        )
                        st.session_state.column_mapping[left_col] = right_col
            
            # Perform comparison if mapping is complete
            if st.session_state.column_mapping:
                if st.button("Compare Datasets"):
                    is_identical, mismatched = compare_datasets(
                        df_left,
                        df_right,
                        st.session_state.column_mapping,
                        left_filename,
                        right_filename
                    )
                    # Store results in session state
                    st.session_state.is_identical = is_identical
                    st.session_state.mismatched = mismatched
                    st.session_state.left_filename = left_filename
                    st.session_state.right_filename = right_filename
                
                # Check if we have comparison results in session state
                if 'mismatched' in st.session_state and st.session_state.mismatched is not None:
                    if st.session_state.is_identical:
                        st.success("✅ Datasets are identical!")
                    else:
                        st.error(f"❌ Datasets are different! Found {len(st.session_state.mismatched)} mismatched rows.")
                        
                        # Add filtering options using radio buttons
                        filter_option = st.radio(
                            "Filter mismatched rows:",
                            [
                                "Show All",
                                f"Only in {st.session_state.left_filename}",
                                f"Only in {st.session_state.right_filename}",
                                f"In both {st.session_state.left_filename} and {st.session_state.right_filename}"
                            ],
                            horizontal=True,
                            key="filter_option"
                        )
                        
                        try:
                            # Apply filter based on selection
                            if filter_option == "Show All":
                                filtered_mismatched = st.session_state.mismatched.copy()
                            else:
                                filtered_mismatched = st.session_state.mismatched[
                                    st.session_state.mismatched['Dataset'] == filter_option
                                ].copy()
                            
                            # Show filtered mismatched rows preview with count
                            st.write(f"Preview of filtered mismatched rows ({len(filtered_mismatched)} rows, showing first 50):")
                            if len(filtered_mismatched) > 0:
                                st.dataframe(filtered_mismatched.head(50))
                            else:
                                st.info("No rows match the selected filter.")
                            
                            # Download button for filtered mismatched rows
                            if len(filtered_mismatched) > 0:
                                csv = filtered_mismatched.to_csv(index=False)
                                st.download_button(
                                    label="Download filtered mismatched rows as CSV",
                                    data=csv,
                                    file_name="mismatched_rows.csv",
                                    mime="text/csv"
                                )
                        except Exception as e:
                            st.error(f"Error during filtering: {str(e)}")

if __name__ == "__main__":
    main() 