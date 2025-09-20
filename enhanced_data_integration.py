"""
Enhanced Legal Agent Data Integration Module
===========================================

This module integrates multiple crime datasets with the Legal Agent system:
- crime_data.json: Senior citizen crimes (2020-2022)
- INSERT2.json: General IPC crimes and population data (2020-2022)
- INSERT3.json: Senior citizen crimes (2019-2021) and other categories

Features:
- Multi-dataset crime statistics analysis
- Comprehensive population data
- Historical crime trends (2019-2022)
- Enhanced location-based insights
- Cross-dataset correlation analysis

Author: Legal Agent Team
Version: 3.0.0
Date: 2025-07-22
"""

import json
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EnhancedCrimeStatistics:
    """Enhanced data structure for comprehensive crime statistics"""
    state_ut: str
    
    # Senior citizen crimes (multiple years)
    senior_crimes_2019: Optional[int] = None
    senior_crimes_2020: Optional[int] = None
    senior_crimes_2021: Optional[int] = None
    senior_crimes_2022: Optional[int] = None
    
    # General IPC crimes
    ipc_crimes_2020: Optional[int] = None
    ipc_crimes_2021: Optional[int] = None
    ipc_crimes_2022: Optional[int] = None
    
    # Population data
    senior_population_lakhs: Optional[float] = None
    total_population_2021_lakhs: Optional[float] = None
    total_population_2022_lakhs: Optional[float] = None
    
    # Crime rates
    senior_crime_rate_2021: Optional[float] = None
    senior_crime_rate_2022: Optional[float] = None
    
    # Chargesheeting rates
    senior_chargesheeting_rate_2021: Optional[float] = None
    senior_chargesheeting_rate_2022: Optional[float] = None
    
    is_union_territory: bool = False
    
    @property
    def senior_crime_trend_2019_2022(self) -> str:
        """Calculate senior citizen crime trend from 2019 to 2022"""
        years_data = [
            (2019, self.senior_crimes_2019),
            (2020, self.senior_crimes_2020),
            (2021, self.senior_crimes_2021),
            (2022, self.senior_crimes_2022)
        ]
        
        # Filter out None values
        valid_data = [(year, crimes) for year, crimes in years_data if crimes is not None]
        
        if len(valid_data) < 2:
            return "insufficient_data"
        
        # Compare first and last available years
        first_year, first_crimes = valid_data[0]
        last_year, last_crimes = valid_data[-1]
        
        if last_crimes > first_crimes * 1.1:  # 10% increase threshold
            return "increasing"
        elif last_crimes < first_crimes * 0.9:  # 10% decrease threshold
            return "decreasing"
        else:
            return "stable"
    
    @property
    def senior_risk_level(self) -> str:
        """Determine risk level based on latest senior citizen crime rate"""
        rate = self.senior_crime_rate_2022 or self.senior_crime_rate_2021
        
        if rate is None:
            return "unknown"
        elif rate >= 80:
            return "very_high"
        elif rate >= 50:
            return "high"
        elif rate >= 20:
            return "medium"
        elif rate >= 5:
            return "low"
        else:
            return "very_low"
    
    @property
    def ipc_crime_trend_2020_2022(self) -> str:
        """Calculate general IPC crime trend"""
        if self.ipc_crimes_2020 and self.ipc_crimes_2022:
            if self.ipc_crimes_2022 > self.ipc_crimes_2020 * 1.05:
                return "increasing"
            elif self.ipc_crimes_2022 < self.ipc_crimes_2020 * 0.95:
                return "decreasing"
            else:
                return "stable"
        return "insufficient_data"


class EnhancedCrimeDataAnalyzer:
    """Enhanced analyzer that integrates multiple crime datasets"""
    
    def __init__(self, 
                 crime_data_file: str = "crime_data.json",
                 insert2_file: str = "INSERT2.json", 
                 insert3_file: str = "INSERT3.json"):
        """Initialize with multiple data files"""
        self.crime_data_file = crime_data_file
        self.insert2_file = insert2_file
        self.insert3_file = insert3_file
        self.enhanced_stats: Dict[str, EnhancedCrimeStatistics] = {}
        self.load_all_datasets()
    
    def load_all_datasets(self):
        """Load and integrate all crime datasets"""
        try:
            # Load primary crime data (2020-2022 senior citizen crimes)
            self._load_primary_crime_data()
            
            # Load INSERT2 data (general IPC crimes and population)
            self._load_insert2_data()
            
            # Load INSERT3 data (2019-2021 senior citizen crimes)
            self._load_insert3_data()
            
            logger.info(f"Enhanced data integration loaded for {len(self.enhanced_stats)} states/UTs")
            
        except Exception as e:
            logger.error(f"Error loading enhanced crime data: {e}")
            self.enhanced_stats = {}
    
    def _load_primary_crime_data(self):
        """Load crime_data.json (senior citizen crimes 2020-2022)"""
        try:
            with open(self.crime_data_file, 'r') as f:
                data = json.load(f)
            
            crime_data = data["table_6A.1_crime_against_senior_citizens_state_ut_wise_2020_2022"]
            
            # Process states
            for state_data in crime_data["STATES"]:
                state_name = state_data["State/UT"].lower()
                
                stats = EnhancedCrimeStatistics(
                    state_ut=state_data["State/UT"],
                    senior_crimes_2020=state_data["2020"],
                    senior_crimes_2021=state_data["2021"],
                    senior_crimes_2022=state_data["2022"],
                    senior_population_lakhs=state_data["Actual Senior Citizen Population (in Lakhs) (2011)"],
                    senior_crime_rate_2022=state_data["Rate of Total Crime against Senior Citizen (2022)"],
                    senior_chargesheeting_rate_2022=state_data.get("Chargesheeting Rate (2022)"),
                    is_union_territory=False
                )
                
                self.enhanced_stats[state_name] = stats
            
            # Process union territories
            for ut_data in crime_data["UNION TERRITORIES"]:
                ut_name = ut_data["State/UT"].lower()
                
                stats = EnhancedCrimeStatistics(
                    state_ut=ut_data["State/UT"],
                    senior_crimes_2020=ut_data["2020"],
                    senior_crimes_2021=ut_data["2021"],
                    senior_crimes_2022=ut_data["2022"],
                    senior_population_lakhs=ut_data["Actual Senior Citizen Population (in Lakhs) (2011)"],
                    senior_crime_rate_2022=ut_data["Rate of Total Crime against Senior Citizen (2022)"],
                    senior_chargesheeting_rate_2022=ut_data.get("Chargesheeting Rate (2022)"),
                    is_union_territory=True
                )
                
                self.enhanced_stats[ut_name] = stats
                
        except FileNotFoundError:
            logger.warning(f"Primary crime data file {self.crime_data_file} not found")
        except Exception as e:
            logger.error(f"Error loading primary crime data: {e}")
    
    def _load_insert2_data(self):
        """Load INSERT2.json (general IPC crimes and population 2020-2022)"""
        try:
            with open(self.insert2_file, 'r') as f:
                data = json.load(f)
            
            # Load population data for 2022
            if "projected_population_states_uts_2022" in data:
                for pop_data in data["projected_population_states_uts_2022"]:
                    state_name = pop_data["STATE/UT"].lower()
                    
                    if state_name in self.enhanced_stats:
                        self.enhanced_stats[state_name].total_population_2022_lakhs = pop_data["Population (in Lakhs)"]
                    else:
                        # Create new entry if not exists
                        self.enhanced_stats[state_name] = EnhancedCrimeStatistics(
                            state_ut=pop_data["STATE/UT"],
                            total_population_2022_lakhs=pop_data["Population (in Lakhs)"]
                        )
            
            # Load IPC crime data by state
            if "table_1A.1_cases_registered_under_ipc_crimes_state_ut_wise_2020_2022" in data:
                ipc_data = data["table_1A.1_cases_registered_under_ipc_crimes_state_ut_wise_2020_2022"]
                
                # Process states
                for state_data in ipc_data["STATES"]:
                    state_name = state_data["State/UT"].lower()
                    
                    if state_name in self.enhanced_stats:
                        self.enhanced_stats[state_name].ipc_crimes_2020 = state_data["2020"]
                        self.enhanced_stats[state_name].ipc_crimes_2021 = state_data["2021"]
                        self.enhanced_stats[state_name].ipc_crimes_2022 = state_data["2022"]
                
                # Process union territories
                for ut_data in ipc_data["UNION TERRITORIES"]:
                    ut_name = ut_data["State/UT"].lower()
                    
                    if ut_name in self.enhanced_stats:
                        self.enhanced_stats[ut_name].ipc_crimes_2020 = ut_data["2020"]
                        self.enhanced_stats[ut_name].ipc_crimes_2021 = ut_data["2021"]
                        self.enhanced_stats[ut_name].ipc_crimes_2022 = ut_data["2022"]
                        self.enhanced_stats[ut_name].is_union_territory = True
                        
        except FileNotFoundError:
            logger.warning(f"INSERT2 data file {self.insert2_file} not found")
        except Exception as e:
            logger.error(f"Error loading INSERT2 data: {e}")
    
    def _load_insert3_data(self):
        """Load INSERT3.json (senior citizen crimes 2019-2021)"""
        try:
            with open(self.insert3_file, 'r') as f:
                data = json.load(f)
            
            # Load population data for 2021
            if "projected_population_states_uts_2021" in data["crime_in_india_2021_volume_2"]:
                for pop_data in data["crime_in_india_2021_volume_2"]["projected_population_states_uts_2021"]:
                    state_name = pop_data["STATE/UT"].lower()
                    
                    if state_name in self.enhanced_stats:
                        self.enhanced_stats[state_name].total_population_2021_lakhs = pop_data["Population (in Lakhs)"]
            
            # Load senior citizen crime data (2019-2021)
            if "table_6A.1_crime_against_senior_citizens_state_ut_wise_2019_2021" in data["crime_in_india_2021_volume_2"]:
                senior_data = data["crime_in_india_2021_volume_2"]["table_6A.1_crime_against_senior_citizens_state_ut_wise_2019_2021"]
                
                # Process states
                for state_data in senior_data["STATES"]:
                    state_name = state_data["State/UT"].lower()
                    
                    if state_name in self.enhanced_stats:
                        self.enhanced_stats[state_name].senior_crimes_2019 = state_data["2019"]
                        # Update 2020, 2021 data if not already present
                        if self.enhanced_stats[state_name].senior_crimes_2020 is None:
                            self.enhanced_stats[state_name].senior_crimes_2020 = state_data["2020"]
                        if self.enhanced_stats[state_name].senior_crimes_2021 is None:
                            self.enhanced_stats[state_name].senior_crimes_2021 = state_data["2021"]
                        
                        # Update rates from 2021 data
                        self.enhanced_stats[state_name].senior_crime_rate_2021 = state_data["Rate of Total Crime against Senior Citizen (2021)"]
                        self.enhanced_stats[state_name].senior_chargesheeting_rate_2021 = state_data["Chargesheeting Rate (2021)"]
                
                # Process union territories from INSERT3
                for ut_data in senior_data["UNION TERRITORIES"]:
                    ut_name = ut_data["State/UT"].lower()
                    
                    if ut_name in self.enhanced_stats:
                        self.enhanced_stats[ut_name].senior_crimes_2019 = ut_data["2019"]
                        if self.enhanced_stats[ut_name].senior_crimes_2020 is None:
                            self.enhanced_stats[ut_name].senior_crimes_2020 = ut_data["2020"]
                        if self.enhanced_stats[ut_name].senior_crimes_2021 is None:
                            self.enhanced_stats[ut_name].senior_crimes_2021 = ut_data["2021"]
                        
                        self.enhanced_stats[ut_name].senior_crime_rate_2021 = ut_data["Rate of Total Crime against Senior Citizen (2021)"]
                        self.enhanced_stats[ut_name].senior_chargesheeting_rate_2021 = ut_data["Chargesheeting Rate (2021)"]
                        self.enhanced_stats[ut_name].is_union_territory = True
                        
        except FileNotFoundError:
            logger.warning(f"INSERT3 data file {self.insert3_file} not found")
        except Exception as e:
            logger.error(f"Error loading INSERT3 data: {e}")
    
    def get_enhanced_location_stats(self, location: str) -> Optional[EnhancedCrimeStatistics]:
        """Get enhanced crime statistics for a specific location"""
        location_key = location.lower().strip()
        
        # Direct match
        if location_key in self.enhanced_stats:
            return self.enhanced_stats[location_key]
        
        # Partial match
        for key, stats in self.enhanced_stats.items():
            if location_key in key or key in location_key:
                return stats
        
        return None
    
    def get_comprehensive_location_advice(self, location: str, crime_type: str = "senior_citizen_abuse") -> Dict[str, Any]:
        """Get comprehensive location-specific legal advice with enhanced data"""
        stats = self.get_enhanced_location_stats(location)
        
        if not stats:
            return {
                "location_found": False,
                "advice": "Location not found in enhanced database. Please consult local legal authorities.",
                "risk_level": "unknown"
            }
        
        # Generate comprehensive advice
        advice_components = []
        
        # Senior citizen crime analysis
        if crime_type == "senior_citizen_abuse" and stats.senior_crime_rate_2022:
            risk_level = stats.senior_risk_level
            
            if risk_level in ["very_high", "high"]:
                advice_components.append(f"🚨 HIGH RISK AREA: {stats.state_ut} has a high senior citizen crime rate ({stats.senior_crime_rate_2022} per lakh).")
                advice_components.append("Immediate protective measures and legal action strongly recommended.")
            elif risk_level == "medium":
                advice_components.append(f"⚠️ MODERATE RISK: {stats.state_ut} has moderate senior citizen crime rates.")
            else:
                advice_components.append(f"✅ LOWER RISK: {stats.state_ut} has relatively lower senior citizen crime rates.")
            
            # Historical trend analysis
            trend = stats.senior_crime_trend_2019_2022
            if trend == "increasing":
                advice_components.append("📈 CONCERNING TREND: Senior citizen crimes are increasing over the past years.")
            elif trend == "decreasing":
                advice_components.append("📉 POSITIVE TREND: Senior citizen crimes are decreasing.")
            
            # Chargesheeting rate analysis
            chargesheeting_rate = stats.senior_chargesheeting_rate_2022 or stats.senior_chargesheeting_rate_2021
            if chargesheeting_rate:
                if chargesheeting_rate >= 80:
                    advice_components.append(f"✅ Strong prosecution: {chargesheeting_rate}% chargesheeting rate indicates effective law enforcement.")
                elif chargesheeting_rate >= 60:
                    advice_components.append(f"⚠️ Moderate prosecution: {chargesheeting_rate}% chargesheeting rate.")
                else:
                    advice_components.append(f"❌ Weak prosecution: {chargesheeting_rate}% chargesheeting rate may indicate challenges in case resolution.")
        
        # General crime context
        if stats.ipc_crimes_2022 and stats.total_population_2022_lakhs:
            general_crime_rate = (stats.ipc_crimes_2022 / stats.total_population_2022_lakhs) * 100
            advice_components.append(f"📊 General crime context: {general_crime_rate:.1f} IPC crimes per lakh population in 2022.")
        
        return {
            "location_found": True,
            "location": stats.state_ut,
            "risk_level": stats.senior_risk_level,
            "senior_crime_rate_2022": stats.senior_crime_rate_2022,
            "senior_crime_rate_2021": stats.senior_crime_rate_2021,
            "chargesheeting_rate_2022": stats.senior_chargesheeting_rate_2022,
            "chargesheeting_rate_2021": stats.senior_chargesheeting_rate_2021,
            "senior_crime_trend": stats.senior_crime_trend_2019_2022,
            "ipc_crime_trend": stats.ipc_crime_trend_2020_2022,
            "advice": " ".join(advice_components),
            "enhanced_statistics": {
                "senior_crimes_2019": stats.senior_crimes_2019,
                "senior_crimes_2020": stats.senior_crimes_2020,
                "senior_crimes_2021": stats.senior_crimes_2021,
                "senior_crimes_2022": stats.senior_crimes_2022,
                "ipc_crimes_2020": stats.ipc_crimes_2020,
                "ipc_crimes_2021": stats.ipc_crimes_2021,
                "ipc_crimes_2022": stats.ipc_crimes_2022,
                "total_population_2021_lakhs": stats.total_population_2021_lakhs,
                "total_population_2022_lakhs": stats.total_population_2022_lakhs,
                "is_union_territory": stats.is_union_territory
            }
        }
    
    def get_enhanced_high_risk_states(self, threshold: float = 50.0) -> List[EnhancedCrimeStatistics]:
        """Get states with high senior citizen crime rates using enhanced data"""
        high_risk = []
        for stats in self.enhanced_stats.values():
            rate = stats.senior_crime_rate_2022 or stats.senior_crime_rate_2021
            if rate and rate >= threshold:
                high_risk.append(stats)
        
        return sorted(high_risk, key=lambda x: x.senior_crime_rate_2022 or x.senior_crime_rate_2021 or 0, reverse=True)
    
    def analyze_enhanced_crime_trends(self) -> Dict[str, Any]:
        """Analyze comprehensive crime trends across all datasets"""
        # Senior citizen crime totals
        total_senior_2019 = sum(s.senior_crimes_2019 for s in self.enhanced_stats.values() if s.senior_crimes_2019)
        total_senior_2020 = sum(s.senior_crimes_2020 for s in self.enhanced_stats.values() if s.senior_crimes_2020)
        total_senior_2021 = sum(s.senior_crimes_2021 for s in self.enhanced_stats.values() if s.senior_crimes_2021)
        total_senior_2022 = sum(s.senior_crimes_2022 for s in self.enhanced_stats.values() if s.senior_crimes_2022)
        
        # IPC crime totals
        total_ipc_2020 = sum(s.ipc_crimes_2020 for s in self.enhanced_stats.values() if s.ipc_crimes_2020)
        total_ipc_2021 = sum(s.ipc_crimes_2021 for s in self.enhanced_stats.values() if s.ipc_crimes_2021)
        total_ipc_2022 = sum(s.ipc_crimes_2022 for s in self.enhanced_stats.values() if s.ipc_crimes_2022)
        
        # Trend analysis
        increasing_senior_states = [s for s in self.enhanced_stats.values() if s.senior_crime_trend_2019_2022 == "increasing"]
        decreasing_senior_states = [s for s in self.enhanced_stats.values() if s.senior_crime_trend_2019_2022 == "decreasing"]
        
        # Average chargesheeting rates
        avg_chargesheeting_2021 = np.mean([
            s.senior_chargesheeting_rate_2021 for s in self.enhanced_stats.values() 
            if s.senior_chargesheeting_rate_2021 is not None
        ])
        
        avg_chargesheeting_2022 = np.mean([
            s.senior_chargesheeting_rate_2022 for s in self.enhanced_stats.values() 
            if s.senior_chargesheeting_rate_2022 is not None
        ])
        
        # Find extremes
        highest_senior_rate_state = max(
            self.enhanced_stats.values(), 
            key=lambda x: x.senior_crime_rate_2022 or x.senior_crime_rate_2021 or 0
        )
        
        lowest_senior_rate_state = min(
            [s for s in self.enhanced_stats.values() if (s.senior_crime_rate_2022 or s.senior_crime_rate_2021)],
            key=lambda x: x.senior_crime_rate_2022 or x.senior_crime_rate_2021 or float('inf')
        )
        
        return {
            "senior_citizen_crimes": {
                "2019": total_senior_2019,
                "2020": total_senior_2020,
                "2021": total_senior_2021,
                "2022": total_senior_2022
            },
            "ipc_crimes": {
                "2020": total_ipc_2020,
                "2021": total_ipc_2021,
                "2022": total_ipc_2022
            },
            "senior_crime_trend": "increasing" if total_senior_2022 > total_senior_2019 else "decreasing",
            "ipc_crime_trend": "increasing" if total_ipc_2022 > total_ipc_2020 else "decreasing",
            "states_with_increasing_senior_crime": len(increasing_senior_states),
            "states_with_decreasing_senior_crime": len(decreasing_senior_states),
            "average_chargesheeting_rate_2021": round(avg_chargesheeting_2021, 2) if not np.isnan(avg_chargesheeting_2021) else None,
            "average_chargesheeting_rate_2022": round(avg_chargesheeting_2022, 2) if not np.isnan(avg_chargesheeting_2022) else None,
            "highest_senior_crime_rate_state": highest_senior_rate_state.state_ut,
            "lowest_senior_crime_rate_state": lowest_senior_rate_state.state_ut,
            "data_coverage": {
                "states_with_senior_data": len([s for s in self.enhanced_stats.values() if s.senior_crimes_2022]),
                "states_with_ipc_data": len([s for s in self.enhanced_stats.values() if s.ipc_crimes_2022]),
                "states_with_population_data": len([s for s in self.enhanced_stats.values() if s.total_population_2022_lakhs])
            }
        }


# Factory function for enhanced system
def create_enhanced_legal_system(
    crime_data_file: str = "crime_data.json",
    insert2_file: str = "INSERT2_fixed.json", 
    insert3_file: str = "INSERT3_fixed.json"
) -> EnhancedCrimeDataAnalyzer:
    """Create enhanced legal system with multiple datasets"""
    return EnhancedCrimeDataAnalyzer(crime_data_file, insert2_file, insert3_file)


if __name__ == "__main__":
    # Example usage and testing
    print("🔄 Loading Enhanced Crime Data Integration...")
    analyzer = create_enhanced_legal_system()
    
    # Test enhanced location lookup
    print("\n📍 Testing Enhanced Location Analysis:")
    delhi_stats = analyzer.get_enhanced_location_stats("Delhi")
    if delhi_stats:
        print(f"Delhi Senior Crime Rate 2022: {delhi_stats.senior_crime_rate_2022}")
        print(f"Delhi IPC Crimes 2022: {delhi_stats.ipc_crimes_2022}")
        print(f"Delhi Population 2022: {delhi_stats.total_population_2022_lakhs} lakhs")
        print(f"Delhi Senior Crime Trend: {delhi_stats.senior_crime_trend_2019_2022}")
    
    # Test comprehensive advice
    print("\n💡 Testing Comprehensive Advice:")
    advice = analyzer.get_comprehensive_location_advice("Maharashtra", "senior_citizen_abuse")
    print(f"Maharashtra Advice: {advice['advice'][:200]}...")
    
    # Test enhanced trends
    print("\n📈 Testing Enhanced Trends Analysis:")
    trends = analyzer.analyze_enhanced_crime_trends()
    print(f"Senior Crimes 2022: {trends['senior_citizen_crimes']['2022']:,}")
    print(f"IPC Crimes 2022: {trends['ipc_crimes']['2022']:,}")
    print(f"Senior Crime Trend: {trends['senior_crime_trend']}")
    print(f"Data Coverage: {trends['data_coverage']}")
    
    print("\n✅ Enhanced Data Integration Test Complete!")
