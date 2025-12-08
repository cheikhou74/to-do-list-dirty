#!/usr/bin/env python
"""
Generate consolidated test report from all JSON reports
"""
import json
import glob
from datetime import datetime

def read_json_file(filename):
    """Read JSON file, return empty dict/list if not found or invalid"""
    import json
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Si c'est un fichier pylint, retourne une liste vide
        if 'pylint' in filename:
            return []
        return {}

def generate_summary():
    """Generate test summary from all reports"""
    print("Generating test summary...")
    
    # Read all reports
    pylint_report = read_json_file("pylint_report.json")
    django_report = read_json_file("django_report.json")
    selenium_report = read_json_file("result_test_selenium.json")
    accessibility_report = read_json_file("accessibility_report.json")
    
    summary_lines = []
    
    # 1. Linter results
    summary_lines.append("### 📊 Code Quality (Pylint)")
    if pylint_report:
        score = pylint_report.get('score', 0)
        summary_lines.append(f"- Score: {score}/10")
        summary_lines.append(f"- Messages: {len(pylint_report.get('messages', []))}")
    else:
        summary_lines.append("- No pylint report found")
    
    # 2. Django tests
    summary_lines.append("\n### ✅ Django Unit Tests")
    if django_report and 'tests' in django_report:
        passed = sum(1 for t in django_report['tests'] if t.get('outcome') == 'passed')
        failed = sum(1 for t in django_report['tests'] if t.get('outcome') == 'failed')
        summary_lines.append(f"- Passed: {passed}")
        summary_lines.append(f"- Failed: {failed}")
        summary_lines.append(f"- Total: {len(django_report['tests'])}")
    else:
        summary_lines.append("- No Django test report found")
    
    # 3. Selenium tests
    summary_lines.append("\n### 🌐 Selenium E2E Tests")
    if selenium_report:
        passed = selenium_report.get('passed', 0)
        failed = selenium_report.get('failed', 0)
        summary_lines.append(f"- Passed: {passed}")
        summary_lines.append(f"- Failed: {failed}")
    else:
        summary_lines.append("- No Selenium report found")
    
    # 4. Accessibility tests
    summary_lines.append("\n### ♿ Accessibility Tests")
    if accessibility_report:
        violations = len(accessibility_report.get('violations', []))
        urls_tested = len(accessibility_report.get('urls_tested', []))
        summary_lines.append(f"- URLs tested: {urls_tested}")
        summary_lines.append(f"- Violations found: {violations}")
    else:
        summary_lines.append("- No accessibility report found")
    
    # 5. Overall status
    summary_lines.append("\n### 📈 Overall Status")
    
    # Determine overall status
    has_errors = False
    
    if django_report:
        failed = sum(1 for t in django_report.get('tests', []) if t.get('outcome') == 'failed')
        if failed > 0:
            has_errors = True
            summary_lines.append("- ❌ Django tests have failures")
    
    if selenium_report and selenium_report.get('failed', 0) > 0:
        has_errors = True
        summary_lines.append("- ❌ Selenium tests have failures")
    
    if not has_errors:
        summary_lines.append("- ✅ All automated tests passed!")
    
    # Manual tests reminder
    summary_lines.append("\n### 👨‍💻 Manual Tests Required")
    summary_lines.append("- Cross-browser compatibility")
    summary_lines.append("- Mobile responsiveness")
    summary_lines.append("- User acceptance testing")
    summary_lines.append("- Performance under load")
    
    # Write summary to file
    summary_text = "\n".join(summary_lines)
    with open("test_summary.txt", "w") as f:
        f.write(summary_text)
    
    print(summary_text)
    return has_errors

if __name__ == "__main__":
    import sys
    has_errors = generate_summary()
    sys.exit(1 if has_errors else 0)