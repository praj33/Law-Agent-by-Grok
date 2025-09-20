"""
Legal Agent Data Integration Module
==================================

This module integrates real criminal justice data with the Legal Agent system.
Provides data-driven insights for legal queries related to criminal law and elder abuse.

Features:
- Crime statistics analysis by state/UT
- Senior citizen crime rate analysis
- Chargesheeting rate insights
- Location-based legal advice
- Data-driven route recommendations

Author: Legal Agent Team
Version: 2.0.0
Date: 2025-07-22
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CrimeStatistics:
    """Data structure for crime statistics"""
    state_ut: str
    crime_2020: int
    crime_2021: int
    crime_2022: int
    senior_population_lakhs: float
    crime_rate_2022: float
    chargesheeting_rate_2022: Optional[float]
    is_union_territory: bool = False
    
    @property
    def crime_trend(self) -> str:
        """Calculate crime trend from 2020 to 2022"""
        if self.crime_2022 > self.crime_2021:
            return "increasing"
        elif self.crime_2022 < self.crime_2021:
            return "decreasing"
        else:
            return "stable"
    
    @property
    def risk_level(self) -> str:
        """Determine risk level based on crime rate"""
        if self.crime_rate_2022 >= 80:
            return "very_high"
        elif self.crime_rate_2022 >= 50:
            return "high"
        elif self.crime_rate_2022 >= 20:
            return "medium"
        elif self.crime_rate_2022 >= 5:
            return "low"
        else:
            return "very_low"


class CrimeDataAnalyzer:
    """Analyzes crime data and provides insights for legal queries"""
    
    def __init__(self, data_file: str = "crime_data.json"):
        """Initialize with crime data"""
        self.data_file = data_file
        self.crime_stats: Dict[str, CrimeStatistics] = {}
        self.load_data()
    
    def load_data(self):
        """Load and process crime data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            crime_data = data["table_6A.1_crime_against_senior_citizens_state_ut_wise_2020_2022"]
            
            # Process states
            for state_data in crime_data["STATES"]:
                self._process_location_data(state_data, is_ut=False)
            
            # Process union territories
            for ut_data in crime_data["UNION TERRITORIES"]:
                self._process_location_data(ut_data, is_ut=True)
            
            logger.info(f"Loaded crime data for {len(self.crime_stats)} states/UTs")
            
        except FileNotFoundError:
            logger.error(f"Crime data file {self.data_file} not found")
            self.crime_stats = {}
        except Exception as e:
            logger.error(f"Error loading crime data: {e}")
            self.crime_stats = {}
    
    def _process_location_data(self, location_data: Dict, is_ut: bool = False):
        """Process individual location data"""
        state_ut = location_data["State/UT"]
        
        crime_stats = CrimeStatistics(
            state_ut=state_ut,
            crime_2020=location_data["2020"],
            crime_2021=location_data["2021"],
            crime_2022=location_data["2022"],
            senior_population_lakhs=location_data["Actual Senior Citizen Population (in Lakhs) (2011)"],
            crime_rate_2022=location_data["Rate of Total Crime against Senior Citizen (2022)"],
            chargesheeting_rate_2022=location_data.get("Chargesheeting Rate (2022)"),
            is_union_territory=is_ut
        )
        
        self.crime_stats[state_ut.lower()] = crime_stats
    
    def get_location_stats(self, location: str) -> Optional[CrimeStatistics]:
        """Get crime statistics for a specific location"""
        if not location:
            return None
        location_key = location.lower().strip()
        
        # Direct match
        if location_key in self.crime_stats:
            return self.crime_stats[location_key]
        
        # Partial match
        for key, stats in self.crime_stats.items():
            if location_key in key or key in location_key:
                return stats
        
        return None
    
    def get_high_risk_states(self, threshold: float = 50.0) -> List[CrimeStatistics]:
        """Get states with high crime rates against senior citizens"""
        high_risk = []
        for stats in self.crime_stats.values():
            if stats.crime_rate_2022 >= threshold:
                high_risk.append(stats)
        
        return sorted(high_risk, key=lambda x: x.crime_rate_2022, reverse=True)
    
    def get_low_chargesheeting_states(self, threshold: float = 60.0) -> List[CrimeStatistics]:
        """Get states with low chargesheeting rates"""
        low_chargesheeting = []
        for stats in self.crime_stats.values():
            if (stats.chargesheeting_rate_2022 is not None and 
                stats.chargesheeting_rate_2022 < threshold):
                low_chargesheeting.append(stats)
        
        return sorted(low_chargesheeting, key=lambda x: x.chargesheeting_rate_2022 or 0)
    
    def analyze_crime_trends(self) -> Dict[str, Any]:
        """Analyze overall crime trends"""
        total_2020 = sum(stats.crime_2020 for stats in self.crime_stats.values())
        total_2021 = sum(stats.crime_2021 for stats in self.crime_stats.values())
        total_2022 = sum(stats.crime_2022 for stats in self.crime_stats.values())
        
        increasing_states = [s for s in self.crime_stats.values() if s.crime_trend == "increasing"]
        decreasing_states = [s for s in self.crime_stats.values() if s.crime_trend == "decreasing"]
        
        avg_chargesheeting = np.mean([
            s.chargesheeting_rate_2022 for s in self.crime_stats.values() 
            if s.chargesheeting_rate_2022 is not None
        ])
        
        return {
            "total_crimes": {
                "2020": total_2020,
                "2021": total_2021,
                "2022": total_2022
            },
            "overall_trend": "increasing" if total_2022 > total_2021 else "decreasing",
            "states_with_increasing_crime": len(increasing_states),
            "states_with_decreasing_crime": len(decreasing_states),
            "average_chargesheeting_rate": round(avg_chargesheeting, 2),
            "highest_crime_rate_state": max(self.crime_stats.values(), key=lambda x: x.crime_rate_2022).state_ut,
            "lowest_crime_rate_state": min(self.crime_stats.values(), key=lambda x: x.crime_rate_2022).state_ut
        }
    
    def get_location_based_advice(self, location: str, crime_type: str = "senior_citizen_abuse") -> Dict[str, Any]:
        """Get location-specific legal advice based on crime data"""
        stats = self.get_location_stats(location)
        
        if not stats:
            return {
                "location_found": False,
                "advice": "Location not found in database. Please consult local legal authorities.",
                "risk_level": "unknown"
            }
        
        # Generate location-specific advice
        advice_components = []
        
        # Risk assessment
        risk_level = stats.risk_level
        if risk_level in ["very_high", "high"]:
            advice_components.append(f"⚠️ HIGH RISK AREA: {stats.state_ut} has a high crime rate against senior citizens ({stats.crime_rate_2022} per lakh).")
            advice_components.append("Consider immediate protective measures and legal action.")
        elif risk_level == "medium":
            advice_components.append(f"⚠️ MODERATE RISK: {stats.state_ut} has moderate crime rates against senior citizens.")
        else:
            advice_components.append(f"✅ LOWER RISK: {stats.state_ut} has relatively lower crime rates against senior citizens.")
        
        # Chargesheeting rate advice
        if stats.chargesheeting_rate_2022:
            if stats.chargesheeting_rate_2022 >= 80:
                advice_components.append(f"✅ Good prosecution rate: {stats.chargesheeting_rate_2022}% chargesheeting rate indicates effective law enforcement.")
            elif stats.chargesheeting_rate_2022 >= 60:
                advice_components.append(f"⚠️ Moderate prosecution rate: {stats.chargesheeting_rate_2022}% chargesheeting rate.")
            else:
                advice_components.append(f"❌ Low prosecution rate: {stats.chargesheeting_rate_2022}% chargesheeting rate may indicate challenges in case resolution.")
        
        # Trend analysis
        if stats.crime_trend == "increasing":
            advice_components.append("📈 Crime trend is increasing - consider enhanced precautions.")
        elif stats.crime_trend == "decreasing":
            advice_components.append("📉 Crime trend is decreasing - positive law enforcement trend.")
        
        return {
            "location_found": True,
            "location": stats.state_ut,
            "risk_level": risk_level,
            "crime_rate_2022": stats.crime_rate_2022,
            "chargesheeting_rate_2022": stats.chargesheeting_rate_2022,
            "crime_trend": stats.crime_trend,
            "advice": " ".join(advice_components),
            "statistics": {
                "crimes_2022": stats.crime_2022,
                "senior_population_lakhs": stats.senior_population_lakhs,
                "is_union_territory": stats.is_union_territory
            }
        }


class EnhancedLegalRouteEngine:
    """Enhanced legal route engine with data-driven recommendations"""
    
    def __init__(self, crime_analyzer: CrimeDataAnalyzer):
        self.crime_analyzer = crime_analyzer
        self.base_routes = self._load_base_routes()
    
    def _load_base_routes(self) -> Dict[str, Dict[str, Any]]:
        """Load base legal routes"""
        return {
            'elder_abuse': {
                'summary': 'File complaint under Maintenance and Welfare of Parents and Senior Citizens Act, 2007',
                'timeline': '2-6 months',
                'outcome': 'Protection order, maintenance, or criminal prosecution',
                'urgency': 'high',
                'cost_estimate': '$300-$2,000'
            },
            'criminal_law': {
                'summary': 'File FIR and engage criminal defense attorney',
                'timeline': '3 months to 2 years',
                'outcome': 'Case resolution through court proceedings',
                'urgency': 'critical',
                'cost_estimate': '$2,000-$15,000+'
            }
        }
    
    def get_enhanced_route(self, domain: str, location: str = None, user_query: str = "") -> Dict[str, Any]:
        """Get enhanced legal route with location-specific data"""
        base_route = self.base_routes.get(domain, self.base_routes.get('criminal_law'))
        
        # Add location-specific insights if available
        location_advice = {}
        if location and 'senior' in user_query.lower() or 'elder' in user_query.lower():
            location_advice = self.crime_analyzer.get_location_based_advice(location, 'senior_citizen_abuse')
        
        enhanced_route = base_route.copy()
        enhanced_route['location_insights'] = location_advice
        
        return enhanced_route


# Factory function for easy integration
def create_enhanced_legal_system(crime_data_file: str = "crime_data.json") -> Tuple[CrimeDataAnalyzer, EnhancedLegalRouteEngine]:
    """Create enhanced legal system with crime data integration"""
    crime_analyzer = CrimeDataAnalyzer(crime_data_file)
    enhanced_route_engine = EnhancedLegalRouteEngine(crime_analyzer)
    
    return crime_analyzer, enhanced_route_engine


if __name__ == "__main__":
    # Example usage and testing
    analyzer = CrimeDataAnalyzer()
    
    # Test location lookup
    delhi_stats = analyzer.get_location_stats("Delhi")
    if delhi_stats:
        print(f"Delhi Crime Rate: {delhi_stats.crime_rate_2022}")
        print(f"Delhi Risk Level: {delhi_stats.risk_level}")
    
    # Test high-risk states
    high_risk = analyzer.get_high_risk_states(50.0)
    print(f"\nTop 5 High-Risk States:")
    for stats in high_risk[:5]:
        print(f"- {stats.state_ut}: {stats.crime_rate_2022} per lakh")
    
    # Test location-based advice
    advice = analyzer.get_location_based_advice("Maharashtra", "senior_citizen_abuse")
    print(f"\nMaharashtra Advice: {advice['advice']}")
    
    # Test crime trends
    trends = analyzer.analyze_crime_trends()
    print(f"\nOverall Trends: {trends}")
