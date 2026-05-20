from langchain.tools import Tool

from data_input import get_email_text
from llm_extractor import extract_data
from validator import validate_data
from ui_agent import push_to_ui


# Tool 1 (extracting the emial)
email_tool = Tool(
    name="Email Extraction Tool",
    func=get_email_text,
    description="Fetches latest email and extracts raw text from body and attachments."
)

# Tool 2 (fetching the data through llm)
def llm_tool_wrapper(text):
    return extract_data(text)

llm_tool = Tool(
    name="Financial Data Extractor",
    func=llm_tool_wrapper,
    description="Extracts structured financial information from email text."
)

# Tool 3 (validating extracted JSON)
def validator_tool_wrapper(data):
    return validate_data(data)

validator_tool = Tool(
    name="Validator Tool",
    func=validator_tool_wrapper,
    description="Validates extracted financial JSON data."
)

# Tool 4 (pushing backend data to frontend)
ui_tool = Tool(
    name="UI Push Tool",
    func=push_to_ui,
    description="Pushes validated structured financial data to frontend dashboard"
)