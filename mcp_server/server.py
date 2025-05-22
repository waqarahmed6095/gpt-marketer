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
async def email_content(company_data: dict):
    """
    Give the content of the email generated using the  company data:
    Args:
        company_data: The company data to generate emails for
    Returns:
        html_content: html content of the email
    """
    master_agent = MasterAgent()
    try:
        master_agent.run(company_data)
        with open(os.path.join(master_agent.output_dir, "email.html"), "r") as f:
            html_content = f.read()
        logger.info(f"Email content generated: {html_content}")

        return html_content
    except Exception as e:
        logger.error(f"Error generating email content: {e}")
        return "Error generating email content"


if __name__ == "__main__":
    mcp.run(transport="sse")
