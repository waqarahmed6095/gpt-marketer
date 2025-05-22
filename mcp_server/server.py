import logging
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from backend.main import MasterAgent
import pandas as pd
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("gpt-marketer-mcp")


@mcp.tool()
async def generate_email(company_data: dict):
    """
    Generate B2B emails for a company to target leads
    Args:
        company_data: The company data to generate emails for
    Returns:
        emails: html content of the email
    """
    master_agent = MasterAgent()
    try:
        master_agent.run(company_data)
        with open(os.path.join(master_agent.output_dir, "email.html"), "r") as f:
            html_content = f.read()
        logger.info(f"Emails generated: {html_content}")

        return html_content
    except Exception as e:
        logger.error(f"Error generating emails: {e}")
        return "Error generating emails"


if __name__ == "__main__":
    mcp.run(transport="sse")
