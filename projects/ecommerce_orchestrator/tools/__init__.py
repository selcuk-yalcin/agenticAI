"""E-Commerce Orchestrator Tools Package."""

from .mcp_tools import (
    connect_to_platform_tool,
    sync_data_tool,
    fetch_sales_data_tool,
    fetch_product_data_tool,
    publish_product_tool,
    update_inventory_tool,
    fetch_customer_data_tool,
    get_mcp_tool_definitions
)

from .image_processing_tools import (
    generate_image_variants_tool,
    optimize_image_quality_tool,
    add_watermark_tool,
    convert_image_format_tool,
    generate_product_mockups_tool,
    enhance_product_photo_tool,
    get_image_processing_tool_definitions
)

from .analytics_tools import (
    generate_sales_graph_tool,
    create_dashboard_tool,
    analyze_trends_tool,
    generate_report_tool,
    calculate_kpis_tool,
    get_analytics_tool_definitions
)

__all__ = [
    # MCP Tools
    'connect_to_platform_tool',
    'sync_data_tool',
    'fetch_sales_data_tool',
    'fetch_product_data_tool',
    'publish_product_tool',
    'update_inventory_tool',
    'fetch_customer_data_tool',
    'get_mcp_tool_definitions',
    
    # Image Processing Tools
    'generate_image_variants_tool',
    'optimize_image_quality_tool',
    'add_watermark_tool',
    'convert_image_format_tool',
    'generate_product_mockups_tool',
    'enhance_product_photo_tool',
    'get_image_processing_tool_definitions',
    
    # Analytics Tools
    'generate_sales_graph_tool',
    'create_dashboard_tool',
    'analyze_trends_tool',
    'generate_report_tool',
    'calculate_kpis_tool',
    'get_analytics_tool_definitions',
]
