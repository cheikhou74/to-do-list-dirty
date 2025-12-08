#!/usr/bin/env python
"""
Accessibility tests using axe-core with Selenium
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from axe_selenium_python import Axe

def run_accessibility_test(url, driver):
    """Run accessibility test on a URL"""
    driver.get(url)
    time.sleep(2)  # Wait for page load
    
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    
    return results

def main():
    """Main function to run accessibility tests"""
    print("Starting accessibility tests...")
    
    # Setup Chrome in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Start Django server in background (in CI, it's already running)
        # For local testing, you might need to start it separately
        
        test_urls = [
            "http://localhost:8000/",
            "http://localhost:8000/create/",
            # Add more URLs as needed
        ]
        
        all_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "urls_tested": [],
            "violations": []
        }
        
        for url in test_urls:
            print(f"Testing: {url}")
            try:
                results = run_accessibility_test(url, driver)
                all_results["urls_tested"].append(url)
                
                if results.get("violations"):
                    all_results["violations"].extend(results["violations"])
                    
            except Exception as e:
                print(f"Error testing {url}: {e}")
        
        # Save results
        with open("accessibility_report.json", "w") as f:
            json.dump(all_results, f, indent=2)
            
        print(f"Found {len(all_results['violations'])} accessibility violations")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()