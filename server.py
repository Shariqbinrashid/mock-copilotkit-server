from fastapi import FastAPI
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action as CopilotAction
from typing import Dict, List, Optional
import json
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

# Add a health check endpoint
@app.get("/health")
async def health_check():
    logger.info("🏥 [HEALTH CHECK] Health check endpoint called")
    return {"status": "healthy", "message": "CopilotKit server is running"}

# Add a test endpoint to verify server is running
@app.get("/")
async def root():
    logger.info("🌐 [ROOT] Root endpoint called")
    return {"message": "CopilotKit Server is running", "actions": len(sdk.actions)}

# Mock data functions for different categories
def get_purchase_recency_data(category: str) -> List[Dict]:
    """Get purchase recency data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating purchase recency data for category: {category}")
    
    base_data = [
        {"period": "9 Days", "count": 12500, "percentage": 26.5},
        {"period": "8-14 Days", "count": 8300, "percentage": 17.6},
        {"period": "15-21 Days", "count": 6900, "percentage": 14.6},
        {"period": "22-30 Days", "count": 4500, "percentage": 9.5},
    ]
    
    # Adjust data based on category
    multiplier = 1.0
    if category.lower() in ["premium", "luxury"]:
        multiplier = 0.6
    elif category.lower() in ["snacks", "beverages"]:
        multiplier = 1.4
    
    result = [
        {
            "period": item["period"],
            "count": int(item["count"] * multiplier),
            "percentage": item["percentage"]
        }
        for item in base_data
    ]
    
    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} periods for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample data: {result[0] if result else 'None'}")
    
    return result

def get_brand_data(category: str) -> List[Dict]:
    """Get brand data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating brand data for category: {category}")
    
    brand_mapping = {
        "cookies": [
            {"brand": "Oreo", "count": 15000, "percentage": 40},
            {"brand": "Chips Ahoy", "count": 11250, "percentage": 30},
            {"brand": "Pepperidge Farm", "count": 3750, "percentage": 10},
            {"brand": "Private Label", "count": 7500, "percentage": 20},
        ],
        "snacks": [
            {"brand": "Lay's", "count": 18000, "percentage": 35},
            {"brand": "Pringles", "count": 14000, "percentage": 27},
            {"brand": "Cheetos", "count": 9000, "percentage": 17},
            {"brand": "Private Label", "count": 10000, "percentage": 19},
        ],
        "beverages": [
            {"brand": "Coca-Cola", "count": 22000, "percentage": 45},
            {"brand": "Pepsi", "count": 16000, "percentage": 32},
            {"brand": "Dr Pepper", "count": 6000, "percentage": 12},
            {"brand": "Private Label", "count": 5000, "percentage": 10},
        ]
    }
    
    result = brand_mapping.get(category.lower(), brand_mapping["cookies"])
    
    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} brands for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample brand data: {result[0] if result else 'None'}")
    
    return result

def get_spending_data(category: str) -> List[Dict]:
    """Get spending data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating spending data for category: {category}")
    
    base_data = [
        {"range": "$0-10", "count": 8500, "percentage": 22.7},
        {"range": "$10-25", "count": 12000, "percentage": 32.1},
        {"range": "$25-50", "count": 9500, "percentage": 25.4},
        {"range": "$50+", "count": 7400, "percentage": 19.8},
    ]
    
    # Adjust ranges based on category
    if category.lower() in ["premium", "luxury"]:
        result = [
            {"range": "$25-50", "count": 5000, "percentage": 20},
            {"range": "$50-100", "count": 10000, "percentage": 40},
            {"range": "$100-200", "count": 7000, "percentage": 28},
            {"range": "$200+", "count": 3000, "percentage": 12},
        ]
    elif category.lower() in ["snacks", "beverages"]:
        result = [
            {"range": "$0-5", "count": 12000, "percentage": 35},
            {"range": "$5-15", "count": 15000, "percentage": 44},
            {"range": "$15-30", "count": 6000, "percentage": 17},
            {"range": "$30+", "count": 1000, "percentage": 3},
        ]
    else:
        result = base_data
    
    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} spending ranges for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample spending data: {result[0] if result else 'None'}")
    
    return result

# Action handlers
def handle_get_purchase_recency_data(**kwargs):
    category = kwargs.get("category")
    logger.info(f"🚀 [BACKEND ACTION] *** getPurchaseRecencyData CALLED *** with category: {category}")
    logger.info(f"🔥 [BACKEND ACTION] *** THIS IS A BACKEND ACTION - LLM SHOULD CALL THIS ***")
    logger.info(f"📊 [BACKEND DATA] Getting purchase recency data for {category}")
    
    try:
        data = get_purchase_recency_data(category)
        total_consumers = sum(item["count"] for item in data)
        
        result = {
            "chart_type": "purchase_recency",
            "data": data,
            "category": category,
            "total_consumers": total_consumers,
            "title": f"Purchase Recency Distribution",
            "description": f"Analysis of consumers who purchased {category} in the last 30 days and their purchase recency distribution."
        }
        
        logger.info(f"✅ [BACKEND ACTION] *** SUCCESSFULLY RETURNING DATA *** with {len(data)} periods")
        logger.info(f"🎯 [BACKEND ACTION] Result: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getPurchaseRecencyData: {str(e)}")
        raise

def handle_get_brand_data(**kwargs):
    category = kwargs.get("category")
    selected_recency = kwargs.get("selected_recency")
    logger.info(f"🚀 [BACKEND ACTION] *** getBrandData CALLED *** with category: {category}, selected_recency: {selected_recency}")
    logger.info(f"🔥 [BACKEND ACTION] *** THIS IS A BACKEND ACTION - LLM SHOULD CALL THIS ***")
    logger.info(f"📊 [BACKEND DATA] Getting brand data for {category}")
    
    try:
        data = get_brand_data(category)
        
        result = {
            "chart_type": "brand_breakdown",
            "data": data,
            "category": category,
            "selected_recency": selected_recency,
            "title": f"{category.title()} Brand Breakdown",
            "description": f"Brand distribution for {category} consumers in the selected audience."
        }
        
        logger.info(f"✅ [BACKEND ACTION] *** SUCCESSFULLY RETURNING DATA *** with {len(data)} brands")
        logger.info(f"🎯 [BACKEND ACTION] Result: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getBrandData: {str(e)}")
        raise

def handle_get_spending_data(**kwargs):
    category = kwargs.get("category")
    selected_brands = kwargs.get("selected_brands")
    logger.info(f"🚀 [BACKEND ACTION] *** getSpendingData CALLED *** with category: {category}, selected_brands: {selected_brands}")
    logger.info(f"🔥 [BACKEND ACTION] *** THIS IS A BACKEND ACTION - LLM SHOULD CALL THIS ***")
    logger.info(f"📊 [BACKEND DATA] Getting spending data for {category}")
    
    try:
        data = get_spending_data(category)
        
        result = {
            "chart_type": "spending_distribution",
            "data": data,
            "category": category,
            "selected_brands": selected_brands or [],
            "title": f"Spending Distribution (Last 30 Days)",
            "description": f"Spending patterns for {category} consumers in the selected audience."
        }
        
        logger.info(f"✅ [BACKEND ACTION] *** SUCCESSFULLY RETURNING DATA *** with {len(data)} spending ranges")
        logger.info(f"🎯 [BACKEND ACTION] Result: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getSpendingData: {str(e)}")
        raise

# Action 1: Get Purchase Recency Data
get_purchase_recency_data_action = CopilotAction(
    name="getPurchaseRecencyData",
    description="Get purchase recency distribution data for a specific product category",
    parameters=[{
        "name": "category",
        "type": "string",
        "description": "Product category to analyze (e.g., 'cookies', 'snacks', 'beverages')",
        "required": True
    }],
    handler=handle_get_purchase_recency_data
)

# Action 2: Get Brand Data
get_brand_data_action = CopilotAction(
    name="getBrandData",
    description="Get brand breakdown data for a specific product category",
    parameters=[{
        "name": "category",
        "type": "string",
        "description": "Product category being analyzed",
        "required": True
    }, {
        "name": "selected_recency",
        "type": "string",
        "description": "Previously selected recency period",
        "required": False
    }],
    handler=handle_get_brand_data
)

# Action 3: Get Spending Data
get_spending_data_action = CopilotAction(
    name="getSpendingData",
    description="Get spending distribution data for a specific product category",
    parameters=[{
        "name": "category",
        "type": "string",
        "description": "Product category being analyzed",
        "required": True
    }, {
        "name": "selected_brands",
        "type": "array",
        "description": "Previously selected brands",
        "required": False
    }],
    handler=handle_get_spending_data
)

# Action 4: Update Audience Insights
update_audience_insights_action = CopilotAction(
    name="updateAudienceInsights",
    description="Update audience insights with new consumer count and composition",
    parameters=[{
        "name": "total_consumers",
        "type": "number",
        "description": "Total number of consumers in the audience",
        "required": True
    }, {
        "name": "ingredients",
        "type": "array",
        "description": "List of audience ingredients",
        "required": False
    }],
    handler=lambda total_consumers, ingredients=None: {
        "total_consumers": total_consumers,
        "ingredients": ingredients or [],
        "message": f"Updated audience size: {total_consumers:,} consumers"
    }
)

# Action 5: Add Exclusion
add_exclusion_action = CopilotAction(
    name="addExclusion",
    description="Add exclusion criteria to remove certain consumer groups from the audience",
    parameters=[{
        "name": "exclusion_type",
        "type": "string",
        "description": "Type of exclusion (brand, category, behavior)",
        "required": True
    }, {
        "name": "label",
        "type": "string",
        "description": "Label for the exclusion",
        "required": True
    }, {
        "name": "percentage",
        "type": "number",
        "description": "Percentage of audience to exclude",
        "required": True
    }],
    handler=lambda exclusion_type, label, percentage: {
        "exclusion": {
            "id": f"exclusion_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": exclusion_type,
            "label": label,
            "percentage": percentage
        },
        "message": f"Added exclusion: {label} (-{percentage}%)"
    }
)

# Action 6: Add Filter
add_filter_action = CopilotAction(
    name="addFilter",
    description="Add filter criteria to refine the audience",
    parameters=[{
        "name": "filter_type",
        "type": "string",
        "description": "Type of filter (spending, location, frequency)",
        "required": True
    }, {
        "name": "label",
        "type": "string",
        "description": "Label for the filter",
        "required": True
    }, {
        "name": "value",
        "type": "string",
        "description": "Filter value",
        "required": True
    }],
    handler=lambda filter_type, label, value: {
        "filter": {
            "id": f"filter_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": filter_type,
            "label": label,
            "value": value
        },
        "message": f"Added filter: {label}"
    }
)

# Action 7: Create Final Audience
create_audience_action = CopilotAction(
    name="createAudience",
    description="Create the final audience with all selected criteria",
    parameters=[{
        "name": "audience_name",
        "type": "string",
        "description": "Name for the new audience",
        "required": True
    }, {
        "name": "audience_data",
        "type": "object",
        "description": "Complete audience data including insights, ingredients, exclusions, and filters",
        "required": True
    }],
    handler=lambda audience_name, audience_data: {
        "audience": {
            "id": f"audience_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": audience_name,
            "created_at": datetime.now().isoformat(),
            "data": audience_data
        },
        "message": f"Successfully created audience: {audience_name}"
    }
)

# Initialize the CopilotKit SDK with all actions
sdk = CopilotKitRemoteEndpoint(actions=[
    get_purchase_recency_data_action,
    get_brand_data_action,
    get_spending_data_action,
    update_audience_insights_action,
    add_exclusion_action,
    add_filter_action,
    create_audience_action
])

# Test the actions on startup
def test_actions():
    logger.info("🧪 [STARTUP TEST] Testing backend actions...")
    try:
        # Test getPurchaseRecencyData
        result = handle_get_purchase_recency_data(category="cookies")
        logger.info(f"✅ [STARTUP TEST] getPurchaseRecencyData works: {len(result['data'])} periods")
        
        # Test getBrandData
        result = handle_get_brand_data(category="cookies")
        logger.info(f"✅ [STARTUP TEST] getBrandData works: {len(result['data'])} brands")
        
        # Test getSpendingData
        result = handle_get_spending_data(category="cookies")
        logger.info(f"✅ [STARTUP TEST] getSpendingData works: {len(result['data'])} ranges")
        
        logger.info("✅ [STARTUP TEST] All actions working correctly!")
    except Exception as e:
        logger.error(f"❌ [STARTUP TEST] Action test failed: {str(e)}")

# Add the CopilotKit endpoint to your FastAPI app 
add_fastapi_endpoint(app, sdk, "/copilotkit_remote")

# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📨 [REQUEST] {request.method} {request.url.path} - Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"📤 [RESPONSE] {response.status_code} for {request.url.path}")
    return response

def main():
    """Run the uvicorn server."""
    logger.info("🚀 [SERVER] Starting CopilotKit server...")
    logger.info(f"📊 [SERVER] Registered {len(sdk.actions)} actions:")
    for action in sdk.actions:
        logger.info(f"  - {action.name}: {action.description}")
    
    port = int(os.environ.get("PORT", 8000))
    logger.info("🌍 [SERVER] Server will be available at:")
    logger.info(f"  - http://0.0.0.0:{port} - API documentation")
    logger.info(f"  - http://0.0.0.0:{port}/health - Health check")
    logger.info(f"  - http://0.0.0.0:{port}/copilotkit_remote - CopilotKit endpoint")
    
    # Test actions
    test_actions()
    
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False, log_level="info")
 
if __name__ == "__main__":
    main()