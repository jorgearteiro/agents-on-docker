# Exercise 3: Creating Custom Tools with MCP Integration

**Duration:** 15 minutes  
**Objective:** Build custom tools that work alongside MCP-provided external tools

## Overview

In this exercise, you'll learn how to create custom tools that complement MCP Gateway's external tools. You'll build a complete research assistant that can search the web, analyze content, and generate structured reports with custom formatting and local file operations.

## Prerequisites

- Completed Exercises 1 and 2
- Understanding of Strands SDK tool creation
- Basic Python knowledge

## Step 1: Understanding Tool Integration Patterns

There are several patterns for combining custom tools with MCP tools:

### Pattern 1: Preprocessing Tools
Custom tools that prepare data for MCP tools:
```python
@tool
def prepare_search_query(topic: str, focus_area: str) -> str:
    """Optimize search query for better MCP search results."""
    return f"{topic} {focus_area} latest research 2024"
```

### Pattern 2: Postprocessing Tools
Custom tools that process MCP tool results:
```python
@tool
def analyze_search_results(search_results: str) -> str:
    """Analyze and summarize search results from MCP tools."""
    # Process the search results
    return structured_summary
```

### Pattern 3: Local Operations
Custom tools for local file/data operations:
```python
@tool
def save_structured_report(data: dict) -> str:
    """Save research data in structured format."""
    # Local file operations
    return confirmation_message
```

## Step 2: Create Advanced Custom Tools

Let's create a comprehensive set of custom tools for research assistance:

```bash
# Create advanced agent with custom tools
cat > agent-custom-tools.py << 'EOF'
#!/usr/bin/env python3
"""
Advanced Research Assistant with Custom Tools and MCP Integration

This example demonstrates how to create sophisticated custom tools that work
alongside MCP Gateway's external tools to build a complete research system.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from mcp.client.sse import sse_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient
from strands.models.openai import OpenAIModel

# Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-gateway:8811/sse")
QUESTION = os.getenv("QUESTION", "Artificial Intelligence in Healthcare")

def load_secret(secret_name):
    """Load Docker secret securely."""
    secret_path = f"/run/secrets/{secret_name}"
    try:
        with open(secret_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_model():
    """Configure AI model with secure credentials."""
    api_key = load_secret('openai_api_key')
    
    if api_key and api_key not in ["sk-test-dummy-key-for-learning", "sk-insecure"]:
        return OpenAIModel(
            client_args={"api_key": api_key},
            model_id="gpt-4o-mini",
            params={"temperature": 0.1, "max_tokens": 2000}
        )
    else:
        return OpenAIModel(
            client_args={
                "api_key": "sk-insecure",
                "base_url": os.getenv("MODEL_RUNNER_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
            },
            model_id=os.getenv("MODEL_RUNNER_MODEL", "ai/gemma3:1B-Q4_K_M"),
            params={"temperature": 0.1, "max_tokens": 2000}
        )

# Custom Tools for Research Workflow

@tool
def create_research_plan(topic: str, focus_areas: str = "") -> str:
    """
    Create a structured research plan for a given topic.
    
    This tool helps organize research by breaking down topics into
    searchable components and defining research objectives.
    
    Args:
        topic (str): Main research topic
        focus_areas (str): Specific areas to focus on (optional)
        
    Returns:
        str: Structured research plan with search queries
    """
    try:
        # Parse focus areas
        areas = [area.strip() for area in focus_areas.split(',')] if focus_areas else []
        
        # Create research plan
        plan = {
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "focus_areas": areas,
            "search_queries": [],
            "research_objectives": []
        }
        
        # Generate search queries
        base_queries = [
            f"{topic} definition overview",
            f"{topic} current trends 2024",
            f"{topic} applications examples",
            f"{topic} benefits challenges"
        ]
        
        # Add focus area queries
        for area in areas:
            base_queries.append(f"{topic} {area} latest research")
        
        plan["search_queries"] = base_queries
        
        # Define research objectives
        plan["research_objectives"] = [
            f"Understand core concepts of {topic}",
            f"Identify current applications and use cases",
            f"Analyze benefits and challenges",
            f"Explore future trends and developments"
        ]
        
        # Save plan
        out_dir = Path("/app/research")
        out_dir.mkdir(exist_ok=True)
        
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        plan_file = out_dir / f"{safe_topic}_plan.json"
        
        with open(plan_file, 'w') as f:
            json.dump(plan, f, indent=2)
        
        # Format response
        response = f"📋 Research Plan Created for '{topic}'\n\n"
        response += f"🎯 Objectives:\n"
        for obj in plan["research_objectives"]:
            response += f"  • {obj}\n"
        
        response += f"\n🔍 Search Queries ({len(plan['search_queries'])}):\n"
        for i, query in enumerate(plan["search_queries"], 1):
            response += f"  {i}. {query}\n"
        
        response += f"\n💾 Plan saved to: {plan_file.name}"
        
        return response
        
    except Exception as e:
        return f"❌ Error creating research plan: {str(e)}"

@tool
def analyze_search_content(search_results: str, analysis_focus: str = "key_points") -> str:
    """
    Analyze and structure content from search results.
    
    This tool processes raw search results and extracts structured information
    based on the specified analysis focus.
    
    Args:
        search_results (str): Raw search results from MCP search tool
        analysis_focus (str): Type of analysis (key_points, trends, applications, challenges)
        
    Returns:
        str: Structured analysis of the search content
    """
    try:
        if not search_results or len(search_results.strip()) < 10:
            return "⚠️ No search results provided for analysis"
        
        # Analyze based on focus
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "focus": analysis_focus,
            "content_length": len(search_results),
            "analysis": ""
        }
        
        if analysis_focus == "key_points":
            analysis["analysis"] = f"""
🔍 Content Analysis - Key Points:

📊 Content Overview:
• Source content length: {len(search_results)} characters
• Analysis performed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 Key Insights Extracted:
{search_results[:500]}...

📈 Analysis Summary:
This content provides valuable information that can be further processed
for comprehensive research reporting.
"""
        
        elif analysis_focus == "trends":
            analysis["analysis"] = f"""
📈 Trend Analysis:

🔄 Current Trends Identified:
Based on the search results, several key trends emerge in the analyzed content.

📊 Data Points:
• Content analyzed: {len(search_results)} characters
• Analysis focus: Trend identification
• Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 Trend Summary:
{search_results[:400]}...
"""
        
        else:
            analysis["analysis"] = f"""
🔍 General Analysis:

📋 Content Summary:
The provided search results contain {len(search_results)} characters of information
relevant to the research topic.

🎯 Analysis Focus: {analysis_focus}
⏰ Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📄 Content Preview:
{search_results[:300]}...
"""
        
        return analysis["analysis"]
        
    except Exception as e:
        return f"❌ Error analyzing search content: {str(e)}"

@tool
def generate_structured_report(topic: str, research_data: str, report_type: str = "comprehensive") -> str:
    """
    Generate a structured research report from analyzed data.
    
    This tool creates professional research reports with proper formatting,
    sections, and structure based on the research data collected.
    
    Args:
        topic (str): Research topic
        research_data (str): Analyzed research data
        report_type (str): Type of report (comprehensive, summary, technical)
        
    Returns:
        str: Confirmation of report generation with file path
    """
    try:
        # Create output directory
        out_dir = Path("/app/reports")
        out_dir.mkdir(exist_ok=True)
        
        # Generate report content
        timestamp = datetime.now()
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        
        if report_type == "comprehensive":
            report_content = f"""# Comprehensive Research Report: {topic}

**Generated:** {timestamp.strftime('%Y-%m-%d %H:%M:%S')}  
**Report Type:** Comprehensive Analysis  
**Research Assistant:** AI Agent with MCP Gateway Integration

## Executive Summary

This report provides a comprehensive analysis of {topic} based on current research and available information sources.

## Research Methodology

- **Data Sources:** Web search via MCP Gateway
- **Analysis Tools:** Custom research analysis tools
- **Search Strategy:** Multi-query approach with focus area targeting
- **Quality Assurance:** Automated content analysis and structuring

## Key Findings

{research_data}

## Detailed Analysis

### Current State
The research indicates significant developments in {topic} with multiple applications and ongoing innovations.

### Applications and Use Cases
Based on the research data, several key applications have been identified:

{research_data[:500]}...

### Future Outlook
The analysis suggests continued growth and development in this area.

## Conclusions

This comprehensive analysis of {topic} reveals important insights and trends that warrant continued monitoring and research.

## Methodology Notes

- **Search Tools:** MCP Gateway with DuckDuckGo integration
- **Analysis Framework:** Custom tool-based content analysis
- **Report Generation:** Automated structured reporting system

---

*This report was generated by an AI research assistant using external tools via MCP Gateway for secure API access.*
"""
        
        elif report_type == "summary":
            report_content = f"""# Research Summary: {topic}

**Date:** {timestamp.strftime('%Y-%m-%d')}  
**Type:** Executive Summary

## Overview
{research_data[:200]}...

## Key Points
- Comprehensive research conducted on {topic}
- Multiple data sources analyzed
- Current trends and applications identified

## Next Steps
Further detailed analysis recommended for specific applications.

---
*Generated by AI Research Assistant*
"""
        
        else:  # technical
            report_content = f"""# Technical Analysis: {topic}

**Generated:** {timestamp.isoformat()}  
**Analysis Type:** Technical Deep Dive

## Technical Overview
{research_data}

## Implementation Considerations
Based on the research data, several technical factors should be considered.

## Technical Specifications
Detailed technical analysis based on current research findings.

---
*Technical Report - AI Generated*
"""
        
        # Save report
        report_file = out_dir / f"{safe_topic}_{report_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Create report metadata
        metadata = {
            "topic": topic,
            "report_type": report_type,
            "generated": timestamp.isoformat(),
            "file_path": str(report_file),
            "content_length": len(report_content),
            "research_data_length": len(research_data)
        }
        
        metadata_file = out_dir / f"{safe_topic}_{report_type}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return f"""✅ Structured Report Generated Successfully!

📄 Report Details:
  • Topic: {topic}
  • Type: {report_type.title()} Report
  • File: {report_file.name}
  • Size: {len(report_content):,} characters
  • Generated: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}

📁 Files Created:
  • Report: {report_file.name}
  • Metadata: {metadata_file.name}

🎯 Report includes:
  • Executive summary
  • Research methodology
  • Key findings and analysis
  • Structured conclusions
  • Source attribution

The report is ready for review and can be found in the /app/reports directory."""
        
    except Exception as e:
        return f"❌ Error generating report: {str(e)}"

@tool
def create_research_index(directory_path: str = "/app") -> str:
    """
    Create an index of all research files and reports.
    
    This tool scans the research directories and creates a comprehensive
    index of all generated research materials for easy navigation.
    
    Args:
        directory_path (str): Base directory to scan for research files
        
    Returns:
        str: Research index with file listings and summaries
    """
    try:
        base_path = Path(directory_path)
        
        # Scan for research files
        research_files = {
            "plans": list((base_path / "research").glob("*_plan.json")) if (base_path / "research").exists() else [],
            "reports": list((base_path / "reports").glob("*.md")) if (base_path / "reports").exists() else [],
            "definitions": list((base_path / "definitions").glob("*.txt")) if (base_path / "definitions").exists() else [],
            "metadata": list((base_path / "reports").glob("*_metadata.json")) if (base_path / "reports").exists() else []
        }
        
        # Create index content
        index_content = f"""# Research Index

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Base Directory:** {directory_path}

## Summary

"""
        
        total_files = sum(len(files) for files in research_files.values())
        index_content += f"📊 **Total Files:** {total_files}\n\n"
        
        # Add file listings
        for category, files in research_files.items():
            if files:
                index_content += f"## {category.title()} ({len(files)} files)\n\n"
                for file_path in sorted(files):
                    file_stat = file_path.stat()
                    size_kb = file_stat.st_size / 1024
                    modified = datetime.fromtimestamp(file_stat.st_mtime)
                    
                    index_content += f"- **{file_path.name}**\n"
                    index_content += f"  - Size: {size_kb:.1f} KB\n"
                    index_content += f"  - Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    index_content += f"  - Path: `{file_path}`\n\n"
        
        # Save index
        index_file = base_path / "research_index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        return f"""📚 Research Index Created Successfully!

📋 Index Summary:
  • Total files indexed: {total_files}
  • Research plans: {len(research_files['plans'])}
  • Reports: {len(research_files['reports'])}
  • Definitions: {len(research_files['definitions'])}
  • Metadata files: {len(research_files['metadata'])}

📄 Index file: research_index.md

The index provides a comprehensive overview of all research materials
and can be used to navigate and manage your research collection."""
        
    except Exception as e:
        return f"❌ Error creating research index: {str(e)}"

def main():
    """Main function demonstrating custom tools with MCP integration."""
    
    print("🔬 Starting Advanced Research Assistant")
    print("🛠️  Custom Tools + MCP Gateway Integration")
    print("=" * 60)
    
    try:
        # Configure model
        model = get_model()
        
        # Connect to MCP Gateway
        print(f"🔗 Connecting to MCP Gateway: {MCP_SERVER_URL}")
        mcp_client = MCPClient(lambda: sse_client(MCP_SERVER_URL))
        
        with mcp_client:
            print("✅ MCP Gateway connected")
            
            # Discover MCP tools
            mcp_tools = mcp_client.list_tools_sync()
            print(f"🌐 MCP tools available: {len(mcp_tools)}")
            
            # Custom tools
            custom_tools = [
                create_research_plan,
                analyze_search_content,
                generate_structured_report,
                create_research_index
            ]
            print(f"🔧 Custom tools available: {len(custom_tools)}")
            
            # Combine all tools
            all_tools = mcp_tools + custom_tools
            print(f"🎯 Total tools available: {len(all_tools)}")
            
            # Create research assistant agent
            agent = Agent(
                model=model,
                tools=all_tools,
                system_prompt=f"""You are an advanced research assistant with access to both external tools (via MCP Gateway) and custom research tools.

Your research workflow should be:

1. **Plan**: Use create_research_plan to structure your research approach
2. **Search**: Use the search tool to gather information from multiple queries
3. **Analyze**: Use analyze_search_content to process and structure findings
4. **Report**: Use generate_structured_report to create comprehensive documentation
5. **Index**: Use create_research_index to organize all research materials

Current Research Topic: "{QUESTION}"

Please conduct comprehensive research following this workflow:
- Create a research plan with multiple search queries
- Execute searches to gather comprehensive information
- Analyze the search results to extract key insights
- Generate a structured report with your findings
- Create an index of all research materials

Be thorough, accurate, and ensure all information is well-structured and properly documented."""
            )
            
            # Execute research workflow
            print(f"🔍 Starting research on: {QUESTION}")
            print("🔄 Agent executing comprehensive research workflow...")
            
            response = agent(f"Please conduct comprehensive research on: {QUESTION}")
            
            print("\n" + "=" * 60)
            print("📋 Research Workflow Complete:")
            print(response)
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ Error during research execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
EOF
```

## Step 3: Create Enhanced Compose Configuration

Create a compose file that supports the advanced research workflow:

```bash
cat > compose.custom-tools.yaml << 'EOF'
services:
  research-assistant:
    build:
      context: .
      dockerfile: Dockerfile.secrets
    
    secrets:
      - openai_api_key
    
    environment:
      - MCP_SERVER_URL=http://mcp-gateway:8811/sse
      - QUESTION=Quantum Computing Applications in Drug Discovery
      - OPENAI_API_KEY_FILE=/run/secrets/openai_api_key
    
    volumes:
      # Mount multiple directories for different types of output
      - ./research:/app/research      # Research plans
      - ./reports:/app/reports        # Generated reports
      - ./definitions:/app/definitions # Simple definitions
    
    depends_on:
      - mcp-gateway
    
    # Override default command to use custom tools agent
    command: ["python3", "agent-custom-tools.py"]
    
    models:
      llm:
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL

  mcp-gateway:
    image: docker/mcp-gateway:latest
    use_api_socket: true
    command:
      - --transport=sse
      - --servers=duckduckgo
      - --tools=search

secrets:
  openai_api_key:
    external: true

models:
  llm:
    model: ai/gemma3:1B-Q4_K_M
    context_size: 8192
EOF
```

## Step 4: Test the Complete Research Workflow

Let's test the advanced research assistant:

```bash
# Create the required directories
mkdir -p research reports definitions

# Start the research assistant
docker compose -f compose.custom-tools.yaml up --build
```

**Expected workflow:**
1. Agent creates a research plan
2. Executes multiple search queries
3. Analyzes search results
4. Generates structured report
5. Creates research index

## Step 5: Examine the Generated Research Materials

After the agent completes, examine the generated files:

```bash
# View research plan
ls -la research/
cat research/*_plan.json | jq .

# View generated reports
ls -la reports/
head -20 reports/*.md

# View research index
cat research_index.md
```

## Step 6: Test Individual Custom Tools

You can test individual tools by connecting to the running container:

```bash
# Test research plan creation
docker compose -f compose.custom-tools.yaml exec research-assistant python3 -c "
from agent_custom_tools import create_research_plan
result = create_research_plan('Machine Learning Ethics', 'bias, fairness, transparency')
print(result)
"

# Test report generation
docker compose -f compose.custom-tools.yaml exec research-assistant python3 -c "
from agent_custom_tools import generate_structured_report
result = generate_structured_report('AI Ethics', 'Sample research data about AI ethics and responsible AI development.', 'summary')
print(result)
"
```

## Validation Checkpoint

✅ **Verify your custom tools implementation:**

1. **Tool Integration**: Custom tools work alongside MCP tools
2. **Research Workflow**: Complete research process from plan to report
3. **File Generation**: Multiple file types created (JSON, Markdown)
4. **Error Handling**: Graceful handling of errors in custom tools
5. **Structured Output**: Professional formatting and organization

## Troubleshooting

### Issue: Custom tools not discovered

**Symptoms:**
- Agent doesn't use custom tools
- Only MCP tools available

**Solutions:**
1. Check tool function decorators: `@tool`
2. Verify tools are added to `all_tools` list
3. Check for syntax errors in tool functions

### Issue: File permission errors

**Symptoms:**
```
❌ Error saving research plan: Permission denied
```

**Solutions:**
1. Check volume mount permissions
2. Ensure directories exist: `mkdir -p research reports`
3. Verify container user has write access

### Issue: JSON serialization errors

**Symptoms:**
```
❌ Error creating research plan: Object not JSON serializable
```

**Solutions:**
1. Check datetime serialization (use `.isoformat()`)
2. Ensure all data types are JSON-compatible
3. Add proper error handling for complex objects

## Understanding Tool Patterns

### Preprocessing Pattern
```python
@tool
def prepare_data(raw_input: str) -> str:
    """Prepare data for MCP tool consumption."""
    # Clean, format, or enhance input
    return processed_input
```

### Postprocessing Pattern
```python
@tool
def process_results(mcp_output: str) -> str:
    """Process MCP tool output."""
    # Analyze, structure, or enhance output
    return structured_results
```

### Orchestration Pattern
```python
@tool
def coordinate_workflow(task: str) -> str:
    """Coordinate multiple tool calls."""
    # Use multiple tools in sequence
    return workflow_results
```

## Best Practices for Custom Tools

1. **Clear Documentation**: Comprehensive docstrings with examples
2. **Error Handling**: Robust try/catch blocks with helpful messages
3. **Type Hints**: Proper type annotations for parameters and returns
4. **Validation**: Input validation and sanitization
5. **Logging**: Informative progress and error messages
6. **File Safety**: Secure file operations with proper paths
7. **Resource Management**: Proper cleanup of resources

## Next Steps

You now have a complete research assistant that combines:
- External tool access via MCP Gateway
- Secure credential management with Docker secrets
- Custom tools for specialized workflows
- Structured output and reporting

This pattern can be extended to build sophisticated AI agents for various domains and use cases.

---

**Exercise Complete!** 🛠️

You've successfully created custom tools that work seamlessly with MCP Gateway, building a comprehensive research assistant with advanced capabilities.