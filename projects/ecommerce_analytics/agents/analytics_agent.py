"""
E-commerce Analytics Agent
Provides insights and analytics for e-commerce businesses.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from core.agents.base_agent import BaseAgent


class AnalyticsAgent(BaseAgent):
    """Agent for e-commerce analytics and insights."""
    
    SYSTEM_PROMPT = """You are an expert e-commerce data analyst with expertise in:
- Sales trend analysis
- Customer behavior patterns
- Product performance metrics
- Revenue forecasting
- Inventory optimization

Provide clear, actionable insights backed by data. Use specific metrics and percentages when possible."""

    def __init__(
        self,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.2,
        enable_forecasting: bool = True
    ):
        super().__init__(
            name="AnalyticsAgent",
            model=model,
            temperature=temperature,
            system_prompt=self.SYSTEM_PROMPT
        )
        self.enable_forecasting = enable_forecasting

    def analyze_sales_trends(
        self,
        period: str = "last_30_days",
        include_predictions: bool = False
    ) -> Dict[str, Any]:
        """Analyze sales trends for specified period."""
        
        prompt = f"""Analyze sales trends for {period}:

1. Overall trend (growth, decline, stable)
2. Key patterns (seasonality, peaks, dips)
3. Top performing categories
4. Anomalies or unusual activity
5. {"Forecast for next period" if include_predictions else ""}

Provide specific insights and recommendations."""
        
        analysis = self.run(prompt)
        
        return {
            "period": period,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "includes_forecast": include_predictions
        }

    def analyze_product_performance(
        self,
        product_ids: Optional[List[str]] = None,
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze product performance metrics."""
        
        if metrics is None:
            metrics = ["sales", "revenue", "conversion_rate", "returns"]
        
        prompt = f"""Analyze product performance:
        
Products: {product_ids if product_ids else "All products"}
Metrics: {', '.join(metrics)}

Provide:
1. Top performers
2. Underperformers needing attention
3. Improvement opportunities
4. Pricing recommendations"""
        
        analysis = self.run(prompt)
        
        return {
            "products": product_ids,
            "metrics": metrics,
            "analysis": analysis
        }

    def analyze_customer_behavior(
        self,
        segment: Optional[str] = None,
        metrics: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze customer behavior patterns."""
        
        if metrics is None:
            metrics = ["purchase_frequency", "avg_order_value", "lifetime_value"]
        
        prompt = f"""Analyze customer behavior:
        
Segment: {segment if segment else "All customers"}
Metrics: {', '.join(metrics)}

Provide insights on:
1. Purchasing patterns
2. Customer segments
3. Retention opportunities
4. Churn risk factors
5. Cross-sell opportunities"""
        
        analysis = self.run(prompt)
        
        return {
            "segment": segment,
            "metrics": metrics,
            "analysis": analysis
        }

    def generate_recommendations(
        self,
        customer_id: Optional[str] = None,
        product_id: Optional[str] = None,
        limit: int = 5
    ) -> Dict[str, Any]:
        """Generate product recommendations."""
        
        if customer_id:
            prompt = f"""Generate {limit} product recommendations for customer {customer_id} based on:
- Purchase history
- Browsing behavior
- Similar customer patterns
- Popular items in their segments"""
        elif product_id:
            prompt = f"""Generate {limit} related products for product {product_id} based on:
- Frequently bought together
- Similar products
- Complementary items"""
        else:
            prompt = f"""Generate {limit} trending product recommendations based on:
- Current bestsellers
- Seasonal trends
- High-margin items
- New arrivals"""
        
        recommendations = self.run(prompt)
        
        return {
            "customer_id": customer_id,
            "product_id": product_id,
            "recommendations": recommendations,
            "limit": limit
        }

    def analyze_cart_abandonment(self) -> Dict[str, Any]:
        """Analyze cart abandonment patterns."""
        
        prompt = """Analyze cart abandonment:

1. Abandonment rate trends
2. Common abandonment points
3. Product categories most affected
4. Potential causes
5. Recovery strategies

Provide actionable recommendations to reduce abandonment."""
        
        analysis = self.run(prompt)
        
        return {
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }

    def forecast_revenue(
        self,
        period: str = "next_quarter",
        factors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Forecast revenue for upcoming period."""
        
        if not self.enable_forecasting:
            return {"error": "Forecasting is disabled"}
        
        prompt = f"""Forecast revenue for {period}:
        
Consider factors: {factors if factors else "Historical trends, seasonality, market conditions"}

Provide:
1. Revenue forecast range
2. Confidence level
3. Key assumptions
4. Risk factors
5. Optimization opportunities"""
        
        forecast = self.run(prompt)
        
        return {
            "period": period,
            "forecast": forecast,
            "generated_at": datetime.now().isoformat()
        }


def create_analytics_agent(**kwargs) -> AnalyticsAgent:
    """Factory function to create an AnalyticsAgent."""
    return AnalyticsAgent(**kwargs)
