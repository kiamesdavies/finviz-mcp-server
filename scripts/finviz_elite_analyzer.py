#!/usr/bin/env python3
"""
Finviz Elite Filter Analysis Script

Logs in to the Finviz Elite screener and analyzes all available filter
items and their values in detail.

Requirements:
- requests
- beautifulsoup4
- selenium (for dynamic content)
- pandas (for result organization)

Usage:
    python finviz_elite_analyzer.py
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FilterOption:
    """Data class for a filter option."""
    value: str
    label: str
    group: Optional[str] = None

@dataclass
class FilterParameter:
    """Data class for a filter parameter."""
    name: str
    id: str
    data_filter: str
    options: List[FilterOption]
    selected_value: Optional[str] = None
    category: Optional[str] = None

class FinvizEliteAnalyzer:
    """Finviz Elite filter analysis class."""
    
    def __init__(self):
        self.base_url = "https://elite.finviz.com"
        self.screener_url = f"{self.base_url}/screener.ashx"
        self.login_url = f"{self.base_url}/login.ashx"
        self.session = requests.Session()
        self.driver = None
        self.filters = []
        
        # Filters to exclude (personal settings, etc.)
        self.excluded_filters = {
            'screenerpresetsselect',     # Screener preset selection
            'screenerpresets',           # Screener presets
            'fs_screenerpresetsselect',  # Full ID version
            'fs_screenerpresets',        # Full ID version
        }
        
        # User-agent settings
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        logger.info(f"Excluded filters: {', '.join(self.excluded_filters)}")
    
    def setup_selenium_driver(self, headless: bool = True):
        """Set up the Selenium driver."""
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Auto-download ChromeDriver (if using webdriver-manager)
            # service = Service(ChromeDriverManager().install())
            
            # If specifying ChromeDriver manually
            service = Service()  # Use chromedriver from system PATH
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium driver setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set up Selenium driver: {e}")
            return False
    
    def login_with_selenium(self, username: str, password: str) -> bool:
        """Log in to Finviz Elite with Selenium."""
        try:
            if not self.driver:
                if not self.setup_selenium_driver():
                    return False
            
            logger.info("Logging in to Finviz Elite...")
            self.driver.get(self.login_url)
            
            # Wait for login form elements
            wait = WebDriverWait(self.driver, 10)
            
            # Enter username and password
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']")
            login_button.click()
            
            # Confirm login success (URL change or element existence)
            time.sleep(3)
            
            if "screener.ashx" in self.driver.current_url or self.driver.current_url == f"{self.base_url}/":
                logger.info("Login successful")
                return True
            else:
                logger.error("Login failed")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def navigate_to_screener(self):
        """Navigate to the screener page."""
        try:
            self.driver.get(self.screener_url)
            time.sleep(2)
            logger.info("Navigated to the screener page")
            return True
        except Exception as e:
            logger.error(f"Screener page navigation error: {e}")
            return False
    
    def extract_filter_parameters(self) -> List[FilterParameter]:
        """Extract filter parameters."""
        try:
            # Get page HTML
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            filters = []
            
            # Find filter elements in select tags
            select_elements = soup.find_all('select', class_=re.compile(r'screener-combo|fv-select'))
            
            for select in select_elements:
                try:
                    filter_param = self._parse_select_element(select)
                    if filter_param:
                        filters.append(filter_param)
                except Exception as e:
                    logger.warning(f"Select element parsing error: {e}")
                    continue
            
            logger.info(f"Detected {len(filters)} filter parameters")
            return filters
            
        except Exception as e:
            logger.error(f"Filter parameter extraction error: {e}")
            return []
    
    def _parse_select_element(self, select) -> Optional[FilterParameter]:
        """Parse a select element into a FilterParameter object."""
        try:
            # Get basic attributes
            select_id = select.get('id', '')
            data_filter = select.get('data-filter', '')
            
            if not data_filter:
                return None
            
            # Check excluded filters
            if (select_id.lower() in self.excluded_filters or 
                data_filter.lower() in self.excluded_filters):
                logger.debug(f"Excluded filter: {select_id} (data-filter: {data_filter})")
                return None
            
            # Parse options
            options = []
            current_group = None
            
            for element in select.find_all(['option', 'optgroup']):
                if element.name == 'optgroup':
                    current_group = element.get('label', '')
                elif element.name == 'option':
                    value = element.get('value', '')
                    label = element.get_text(strip=True)
                    
                    option = FilterOption(
                        value=value,
                        label=label,
                        group=current_group
                    )
                    options.append(option)
            
            # Get selected value
            selected_option = select.find('option', selected=True)
            selected_value = selected_option.get('value', '') if selected_option else None
            
            return FilterParameter(
                name=self._get_filter_name_from_id(select_id),
                id=select_id,
                data_filter=data_filter,
                options=options,
                selected_value=selected_value
            )
            
        except Exception as e:
            logger.warning(f"Error parsing select element: {e}")
            return None
    
    def _get_filter_name_from_id(self, element_id: str) -> str:
        """Infer a filter name from element ID."""
        # ID to name mapping
        id_to_name = {
            'fs_exch': 'Exchange',
            'fs_idx': 'Index',
            'fs_sec': 'Sector',
            'fs_ind': 'Industry',
            'fs_geo': 'Country',
            'fs_cap': 'Market Cap',
            'fs_sh_price': 'Price',
            'fs_fa_div': 'Dividend Yield',
            'fs_fa_epsrev': 'EPS/Revenue Revision',
            'fs_sh_short': 'Short Float',
            'fs_an_recom': 'Analyst Recommendation',
            'fs_earningsdate': 'Earnings Date',
            'fs_ipodate': 'IPO Date',
            'fs_sh_avgvol': 'Average Volume',
            'fs_sh_relvol': 'Relative Volume',
            'fs_sh_curvol': 'Current Volume',
            'fs_sh_outstanding': 'Shares Outstanding',
            'fs_sh_float': 'Float',
            'fs_ta_perf2': 'Performance 2',
            'fs_targetprice': 'Target Price',
            # Add other mappings as needed
        }
        
        return id_to_name.get(element_id, element_id)
    
    def categorize_filters(self, filters: List[FilterParameter]) -> Dict[str, List[FilterParameter]]:
        """Categorize filters by category."""
        categories = {
            'Basic Info': [],
            'Price & Market Cap': [],
            'Dividend & Financials': [],
            'Analyst & Recommendations': [],
            'Dates': [],
            'Volume & Trading': [],
            'Share Structure': [],
            'Technical Analysis': [],
            'Other': []
        }
        
        category_mapping = {
            'Exchange': 'Basic Info',
            'Index': 'Basic Info',
            'Sector': 'Basic Info',
            'Industry': 'Basic Info',
            'Country': 'Basic Info',
            'Market Cap': 'Price & Market Cap',
            'Price': 'Price & Market Cap',
            'Target Price': 'Price & Market Cap',
            'Dividend Yield': 'Dividend & Financials',
            'EPS/Revenue Revision': 'Dividend & Financials',
            'Short Float': 'Dividend & Financials',
            'Analyst Recommendation': 'Analyst & Recommendations',
            'Earnings Date': 'Dates',
            'IPO Date': 'Dates',
            'Average Volume': 'Volume & Trading',
            'Relative Volume': 'Volume & Trading',
            'Current Volume': 'Volume & Trading',
            'Shares Outstanding': 'Share Structure',
            'Float': 'Share Structure',
            'Performance 2': 'Technical Analysis',
        }
        
        for filter_param in filters:
            category = category_mapping.get(filter_param.name, 'Other')
            categories[category].append(filter_param)
        
        return categories
    
    def export_to_markdown(self, filters: List[FilterParameter], output_file: str = 'finviz_elite_filters.md'):
        """Export filter information to Markdown."""
        try:
            categorized_filters = self.categorize_filters(filters)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# Finviz Elite Filter Parameter Reference\n\n")
                f.write("Detailed filter parameters available to Elite users.\n\n")
                
                for category, category_filters in categorized_filters.items():
                    if not category_filters:
                        continue
                        
                    f.write(f"## {category}\n\n")
                    
                    for filter_param in category_filters:
                        f.write(f"### {filter_param.name} - `{filter_param.data_filter}`\n\n")
                        
                        if filter_param.options:
                            f.write("| Value | Description | Group |\n")
                            f.write("|---|---|---|\n")
                            
                            for option in filter_param.options:
                                group = option.group or "-"
                                f.write(f"| `{option.value}` | {option.label} | {group} |\n")
                            
                            f.write("\n")
                        
                        f.write("\n")
            
            logger.info(f"Exported filter info to {output_file}")
            
        except Exception as e:
            logger.error(f"Markdown export error: {e}")
    
    def export_to_json(self, filters: List[FilterParameter], output_file: str = 'finviz_elite_filters.json'):
        """Export filter information to JSON."""
        try:
            filter_data = []
            
            for filter_param in filters:
                options_data = []
                for option in filter_param.options:
                    options_data.append({
                        'value': option.value,
                        'label': option.label,
                        'group': option.group
                    })
                
                filter_data.append({
                    'name': filter_param.name,
                    'id': filter_param.id,
                    'data_filter': filter_param.data_filter,
                    'selected_value': filter_param.selected_value,
                    'options': options_data
                })
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(filter_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Exported filter info to {output_file}")
            
        except Exception as e:
            logger.error(f"JSON export error: {e}")
    
    def analyze_specific_filter(self, data_filter: str) -> Optional[FilterParameter]:
        """Analyze a specific filter in detail."""
        try:
            filters = self.extract_filter_parameters()
            
            for filter_param in filters:
                if filter_param.data_filter == data_filter:
                    logger.info(f"Details for filter '{data_filter}':")
                    logger.info(f"  Name: {filter_param.name}")
                    logger.info(f"  ID: {filter_param.id}")
                    logger.info(f"  Selected value: {filter_param.selected_value}")
                    logger.info(f"  Option count: {len(filter_param.options)}")
                    
                    return filter_param
            
            logger.warning(f"Filter '{data_filter}' was not found")
            return None
            
        except Exception as e:
            logger.error(f"Specific filter analysis error: {e}")
            return None
    
    def run_full_analysis(self, username: str, password: str, export_format: str = 'both'):
        """Run full filter analysis."""
        try:
            # Selenium setup
            if not self.setup_selenium_driver():
                return False
            
            # Login
            if not self.login_with_selenium(username, password):
                return False
            
            # Navigate to screener page
            if not self.navigate_to_screener():
                return False
            
            # Filter analysis
            filters = self.extract_filter_parameters()
            
            if not filters:
                logger.error("No filters were detected")
                return False
            
            # Output results
            if export_format in ['markdown', 'both']:
                self.export_to_markdown(filters)
            
            if export_format in ['json', 'both']:
                self.export_to_json(filters)
            
            # Show stats
            categorized = self.categorize_filters(filters)
            logger.info("=== Analysis Summary ===")
            for category, category_filters in categorized.items():
                if category_filters:
                    logger.info(f"{category}: {len(category_filters)} filters")
            
            return True
            
        except Exception as e:
            logger.error(f"Full analysis error: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()

def main():
    """Main entry point."""
    import getpass
    
    print("=== Finviz Elite Filter Analysis Tool ===")
    print()
    
    # Login credentials
    username = input("Finviz Elite username: ")
    password = getpass.getpass("Finviz Elite password: ")
    
    # Run analysis
    analyzer = FinvizEliteAnalyzer()
    
    print("\nStarting filter analysis...")
    success = analyzer.run_full_analysis(username, password, export_format='both')
    
    if success:
        print("\n✅ Analysis completed!")
        print("📄 finviz_elite_filters.md - Detailed Markdown report")
        print("📊 finviz_elite_filters.json - Structured JSON data")
    else:
        print("\n❌ Analysis failed. Check the logs for details.")

if __name__ == "__main__":
    main() 
