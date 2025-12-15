"""
FastAPI backend for Sequential Pattern Mining.

This is the main entry point for the backend API.
It provides endpoints for:
- Dataset upload and validation
- Data preprocessing
- Pattern mining
- Results retrieval
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from typing import Dict, Any

from data_loader import DataLoader
from preprocessing import DataPreprocessor
from mining import PrefixSpan
from visualization_data import VisualizationDataGenerator
from schemas import (
    PreprocessingRequest, MiningResult, DatasetPreview, 
    ErrorResponse, ColumnSelectionRequest, MiningParameters
)
from utils import logger, ensure_directory_exists

# Initialize FastAPI app
app = FastAPI(
    title="Sequential Pattern Mining API",
    description="Backend API for sequential pattern mining with visualization support",
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (In production, use proper state management or database)
data_loader = None
preprocessor = None
current_sequences = None
current_patterns = None
viz_generator = None

# Ensure output directories exist
ensure_directory_exists("outputs")
ensure_directory_exists("outputs/charts")


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Sequential Pattern Mining API",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/upload", response_model=DatasetPreview)
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload and validate CSV dataset.
    
    Args:
        file: Uploaded CSV file
        
    Returns:
        Dataset preview information
    """
    global data_loader
    
    logger.info(f"Received file upload: {file.filename}")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Initialize data loader
        data_loader = DataLoader()
        
        # Load and validate CSV
        preview = data_loader.load_csv_from_bytes(contents, file.filename)
        
        logger.info("File uploaded and validated successfully")
        return preview
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/columns")
async def get_columns():
    """
    Get list of available columns from uploaded dataset.
    
    Returns:
        List of column names
    """
    global data_loader
    
    if data_loader is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded. Please upload a CSV file first.")
    
    try:
        columns = data_loader.get_column_names()
        return {"columns": columns}
    except Exception as e:
        logger.error(f"Error getting columns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/preprocess")
async def preprocess_data(columns: ColumnSelectionRequest):
    """
    Preprocess data and generate sequences.
    
    Args:
        columns: Selected column names for sequence generation
        
    Returns:
        Preprocessing results and statistics
    """
    global data_loader, preprocessor, current_sequences
    
    if data_loader is None:
        raise HTTPException(status_code=400, detail="No dataset uploaded.")
    
    try:
        logger.info("Starting data preprocessing")
        
        # Validate columns
        validation = data_loader.validate_columns(
            columns.sequence_id_column,
            columns.item_column,
            columns.timestamp_column
        )
        
        if not all(validation.values()):
            raise ValueError(f"Invalid columns selected: {validation}")
        
        # Get dataframe and create preprocessor
        df = data_loader.get_dataframe()
        preprocessor = DataPreprocessor(df)
        
        # Generate sequences
        result = preprocessor.generate_sequences(
            columns.sequence_id_column,
            columns.item_column,
            columns.timestamp_column
        )
        
        # Store sequences for mining
        current_sequences = preprocessor.get_sequences()
        
        logger.info("Preprocessing completed successfully")
        return result
        
    except ValueError as e:
        logger.error(f"Preprocessing validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Preprocessing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mine", response_model=MiningResult)
async def mine_patterns(params: MiningParameters):
    """
    Perform sequential pattern mining.
    
    Args:
        params: Mining parameters (min_support, max_length)
        
    Returns:
        Mining results with frequent patterns
    """
    global current_sequences, current_patterns, viz_generator
    
    if current_sequences is None:
        raise HTTPException(
            status_code=400, 
            detail="No sequences available. Please upload and preprocess data first."
        )
    
    try:
        logger.info(f"Starting pattern mining with min_support={params.min_support}")
        
        start_time = time.time()
        
        # Initialize PrefixSpan
        miner = PrefixSpan(
            sequences=current_sequences,
            min_support=params.min_support,
            max_pattern_length=params.max_sequence_length
        )
        
        # Mine patterns
        patterns = miner.mine_patterns()
        current_patterns = patterns
        
        execution_time = time.time() - start_time
        
        # Initialize visualization generator
        viz_generator = VisualizationDataGenerator(patterns, current_sequences)
        
        # Prepare response
        result = MiningResult(
            patterns=patterns[:100],  # Return top 100 for API response
            total_patterns=len(patterns),
            total_sequences=len(current_sequences),
            min_support_used=params.min_support,
            execution_time=round(execution_time, 2)
        )
        
        logger.info(f"Mining completed: {len(patterns)} patterns found")
        return result
        
    except Exception as e:
        logger.error(f"Mining error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/visualizations/bar")
async def get_bar_chart_data(top_n: int = 20):
    """Get data for bar chart visualization."""
    global viz_generator
    
    if viz_generator is None:
        raise HTTPException(status_code=400, detail="No mining results available.")
    
    try:
        data = viz_generator.prepare_bar_chart_data(top_n)
        return data
    except Exception as e:
        logger.error(f"Error preparing bar chart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/visualizations/line")
async def get_line_chart_data():
    """Get data for line chart visualization."""
    global viz_generator
    
    if viz_generator is None:
        raise HTTPException(status_code=400, detail="No mining results available.")
    
    try:
        data = viz_generator.prepare_line_chart_data()
        return data
    except Exception as e:
        logger.error(f"Error preparing line chart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/visualizations/heatmap")
async def get_heatmap_data():
    """Get data for heatmap visualization."""
    global viz_generator
    
    if viz_generator is None:
        raise HTTPException(status_code=400, detail="No mining results available.")
    
    try:
        data = viz_generator.prepare_heatmap_data()
        return data
    except Exception as e:
        logger.error(f"Error preparing heatmap: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/visualizations/network")
async def get_network_data(top_n: int = 15):
    """Get data for network graph visualization."""
    global viz_generator
    
    if viz_generator is None:
        raise HTTPException(status_code=400, detail="No mining results available.")
    
    try:
        data = viz_generator.prepare_network_data(top_n)
        return data
    except Exception as e:
        logger.error(f"Error preparing network graph: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/table")
async def get_table_data():
    """Get all patterns in table format."""
    global viz_generator
    
    if viz_generator is None:
        raise HTTPException(status_code=400, detail="No mining results available.")
    
    try:
        data = viz_generator.prepare_table_data()
        return {"patterns": data}
    except Exception as e:
        logger.error(f"Error preparing table: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/summary")
async def get_summary_stats():
    """Get summary statistics."""
    global viz_generator, current_sequences, current_patterns
    
    if viz_generator is None:
        raise HTTPException(status_code=400, detail="No mining results available.")
    
    try:
        # Get mining parameters from previous operation
        # In production, store these properly
        stats = viz_generator.prepare_summary_stats(
            total_sequences=len(current_sequences),
            execution_time=0,  # TODO: Store from mining operation
            min_support=0.01  # TODO: Store from mining operation
        )
        return stats
    except Exception as e:
        logger.error(f"Error preparing summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
